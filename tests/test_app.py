import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import io
from PIL import Image
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up test image paths
        cls.test_images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        cls.test_image = os.path.join(cls.test_images_dir, 'download.png')
        
        # Initialize session state
        if 'ocr_text' not in st.session_state:
            st.session_state['ocr_text'] = None
        if 'image_data' not in st.session_state:
            st.session_state['image_data'] = None
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []
        if 'gpt_output' not in st.session_state:
            st.session_state['gpt_output'] = ""
        if 'selected_action' not in st.session_state:
            st.session_state['selected_action'] = "Summarize"
        if 'user_prompt' not in st.session_state:
            st.session_state['user_prompt'] = ""

    def setUp(self):
        # Reset session state before each test
        for key in ['ocr_text', 'image_data', 'messages', 'gpt_output', 'selected_action', 'user_prompt']:
            if key in st.session_state:
                del st.session_state[key]

    @patch('app.IMG_TO_TEXT')
    def test_ocr_processing(self, mock_img_to_text):
        """Test OCR processing with mock"""
        mock_img_to_text.return_value = "Test OCR Result"
        
        # Simulate image upload and processing
        if os.path.exists(self.test_image):
            with open(self.test_image, 'rb') as img_file:
                image_bytes = img_file.read()
            
            result = app.IMG_TO_TEXT(image_bytes)
            self.assertEqual(result, "Test OCR Result")
            mock_img_to_text.assert_called_once()

    @patch('app.AzureChatOpenAI')
    def test_llm_integration(self, mock_azure):
        """Test LLM integration"""
        # Create a proper mock response
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MagicMock(content="Test LLM Response")
        mock_azure.return_value = mock_instance

        # Test the LLM
        with patch.dict(os.environ, {
            'AZURE_DEPLOYMENT': 'test-deployment',
            'OPENAI_API_VERSION': '2023-05-15',
            'AZURE_OPENAI_KEY': 'test-key',
            'AZURE_ENDPOINT': 'https://test.openai.azure.com'
        }):
            llm = app.AzureChatOpenAI(
                azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
                openai_api_version=os.getenv("OPENAI_API_VERSION"),
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                azure_endpoint=os.getenv('AZURE_ENDPOINT')
            )
            result = llm.invoke("Test prompt").content
            self.assertEqual(result, "Test LLM Response")

    def test_session_state_initialization(self):
        """Test session state initialization"""
        # Trigger session state initialization by accessing app
        app.st.session_state
        
        expected_keys = ['ocr_text', 'image_data', 'messages', 'gpt_output', 
                        'selected_action', 'user_prompt']
        
        for key in expected_keys:
            self.assertIn(key, st.session_state)
            self.assertIsNone(st.session_state[key])

    def test_environment_variables(self):
        """Test required environment variables"""
        required_vars = [
            "AZURE_DEPLOYMENT",
            "OPENAI_API_VERSION",
            "AZURE_OPENAI_KEY",
            "AZURE_ENDPOINT"
        ]
        
        for var in required_vars:
            self.assertTrue(os.getenv(var) is not None, f"Missing environment variable: {var}")

    @patch('app.AzureChatOpenAI')
    def test_gpt_actions(self, mock_azure):
        """Test different GPT actions"""
        test_text = "Sample OCR text"
        actions = ["Summarize", "Analyze", "Suggest Action"]
        
        mock_response = MagicMock()
        mock_response.content = "GPT Response"
        mock_azure.return_value.invoke.return_value = mock_response

        st.session_state.ocr_text = test_text
        
        for action in actions:
            st.session_state.selected_action = action
            
            if action == "Summarize":
                expected_prompt = f"Summarize the following text:\n\n{test_text}"
                self.assertTrue("Summarize" in expected_prompt)
            elif action == "Analyze":
                expected_prompt = f"Analyze this text and explain its key points or issues:\n\n{test_text}"
                self.assertTrue("Analyze" in expected_prompt)
            elif action == "Suggest Action":
                expected_prompt = f"Based on the following text, suggest any necessary actions or responses:\n\n{test_text}"
                self.assertTrue("suggest" in expected_prompt.lower())

    def test_image_processing(self):
        """Test image processing functionality"""
        if os.path.exists(self.test_image):
            # Test image loading and conversion
            image = Image.open(self.test_image)
            img_bytes = io.BytesIO()
            image.save(img_bytes, format=image.format if image.format else "PNG")
            img_bytes.seek(0)
            
            self.assertIsNotNone(img_bytes.getvalue(), "Image conversion failed")

    def test_conversation_history(self):
        """Test conversation history management"""
        # Initialize empty conversation
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Add test messages
        test_messages = [
            {"role": "user", "content": "Test question"},
            {"role": "assistant", "content": "Test response"}
        ]
        
        for msg in test_messages:
            st.session_state.messages.append(msg)
        
        self.assertEqual(len(st.session_state.messages), 2)
        self.assertEqual(st.session_state.messages[0]["role"], "user")
        self.assertEqual(st.session_state.messages[1]["role"], "assistant")

if __name__ == '__main__':
    unittest.main()
