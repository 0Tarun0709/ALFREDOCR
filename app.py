import streamlit as st
from langchain_openai import AzureChatOpenAI
from srv.imgtxt import IMG_TO_TEXT

import io
from PIL import Image
import os

# Setup
st.set_page_config(page_title="Image-to-Text OCR Assistant")
st.title("📸 Image-to-Text OCR Assistant")

# Initialize LLM
LLM = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),
)

# Session state init
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = None
if "image_data" not in st.session_state:
    st.session_state.image_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gpt_output" not in st.session_state:
    st.session_state.gpt_output = ""
if "selected_action" not in st.session_state:
    st.session_state.selected_action = "Summarize"
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

# Reset button
if st.button("🔁 Reset Image & OCR"):
    st.session_state.ocr_text = None
    st.session_state.image_data = None
    st.session_state.messages = []
    st.session_state.gpt_output = ""
    st.session_state.user_prompt = ""
    st.experimental_rerun()

# Image upload
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Store image data once
    if st.session_state.image_data is None:
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format if image.format else "PNG")
        img_bytes.seek(0)
        st.session_state.image_data = img_bytes.getvalue()

    # OCR step
    if st.session_state.ocr_text is None:
        with st.spinner("🔍 Extracting text with OCR..."):
            st.session_state.ocr_text = IMG_TO_TEXT(st.session_state.image_data)

    st.subheader("📝 Extracted Text")
    st.text_area("OCR Output", st.session_state.ocr_text, height=200)

    # --- GPT Action Selection ---
    st.subheader("🤖 AI Analysis")
    action = st.selectbox(
        "Choose what GPT should do with the extracted text:",
        ["Summarize", "Analyze", "Suggest Action", "Freeform Prompt"],
        index=["Summarize", "Analyze", "Suggest Action", "Freeform Prompt"].index(
            st.session_state.get("selected_action", "Summarize")
        )
    )
    st.session_state.selected_action = action

    # Build user prompt only if not already stored or changed
    if action != "Freeform Prompt":
        if action == "Summarize":
            user_prompt = f"Summarize the following text:\n\n{st.session_state.ocr_text}"
        elif action == "Analyze":
            user_prompt = f"Analyze this text and explain its key points or issues:\n\n{st.session_state.ocr_text}"
        elif action == "Suggest Action":
            user_prompt = f"Based on the following text, suggest any necessary actions or responses:\n\n{st.session_state.ocr_text}"
        st.session_state.user_prompt = user_prompt
    else:
        custom_prompt = st.text_area("Enter your own prompt for GPT:", height=100)
        if custom_prompt.strip():
            st.session_state.user_prompt = f"{custom_prompt}\n\nText:\n{st.session_state.ocr_text}"

    # Run GPT
    if st.button("🧠 Run GPT-4", key="run_gpt"):
        with st.spinner("Thinking..."):
            try:
                gpt_output = LLM.invoke(st.session_state.user_prompt).content
                st.session_state.messages.append({"role": "user", "content": st.session_state.user_prompt})
                st.session_state.messages.append({"role": "assistant", "content": gpt_output})
                st.session_state.gpt_output = gpt_output
            except Exception as e:
                st.error(f"Error: {e}")

# Show GPT output
if st.session_state.gpt_output:
    st.subheader("💬 GPT Response")
    st.write(st.session_state.gpt_output)

# Follow-up input
if len(st.session_state.messages) > 0:
    st.subheader("🔄 Ask a Follow-up")
    followup_input = st.text_input("Your follow-up question or instruction", key="followup_input")

    if st.button("➡️ Send Follow-up", key="followup_btn"):
        if followup_input.strip():
            with st.spinner("GPT is responding..."):
                # Append follow-up
                st.session_state.messages.append({"role": "user", "content": followup_input})

                # Format conversation into string
                conversation = ""
                for msg in st.session_state.messages:
                    speaker = "User" if msg["role"] == "user" else "Assistant"
                    conversation += f"{speaker}: {msg['content']}\n"

                # Send context-aware prompt
                followup_prompt = f"""
                                    Continue the following conversation and respond to the latest user message.

                                    {conversation}
                                    """
                try:
                    reply = LLM.invoke(followup_prompt).content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.session_state.gpt_output = reply
                    st.write(st.session_state.gpt_output)
                except Exception as e:
                    st.error(f"Error: {e}")

# Optional: Show conversation history
if st.session_state.messages:
    with st.expander("🗂️ Conversation History"):
        for msg in st.session_state.messages:
            speaker = "🧑 You" if msg["role"] == "user" else "🤖 GPT"
            st.markdown(f"**{speaker}:** {msg['content']}")
