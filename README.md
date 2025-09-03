## 🖼️ Image-to-Text OCR Assistant

This project is a Streamlit web app that allows users to upload images, extract text using OCR (EasyOCR), and interact with the extracted text using Azure OpenAI (via LangChain). The app can summarize, analyze, or suggest actions based on the text, and supports conversational follow-ups.

### 📸 Application
![Streamlit App Interface](./images/Streamlit.png)

---

### 🚀 Features
- Upload images (PNG, JPG, JPEG)
- Extract text from images using EasyOCR
- Summarize, analyze, or suggest actions on the extracted text with Azure OpenAI
- Freeform prompt support for custom AI queries
- Conversation history and follow-up questions

---

### 🛠️ Installation & Setup
1. **Clone the repository**
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Set environment variables:**
	- `AZURE_DEPLOYMENT`, `OPENAI_API_VERSION`, `AZURE_OPENAI_KEY`, `AZURE_ENDPOINT`
	- (Optional) `LANGUAGE` for OCR
4. **Run the app:**
	```bash
	streamlit run app.py
	```

---

### 🏗️ Architecture Diagram (Mermaid)
```mermaid
flowchart TD
    A["User Uploads Image"] --> B["Streamlit UI (app.py)"]
    B --> C["EasyOCR (imgtxt.py)"]
    C --> D["Extracted Text"]
    D --> E["Azure OpenAI (LangChain)"]
    E --> F["AI Output (Summary/Analysis/Action)"]
    F --> G["Display in Streamlit"]
    G --> H["User Follow-up"]
    H --> E

```

---

### 🔄 Sequence Flow Diagram (Mermaid)
```mermaid
sequenceDiagram
	 participant U as User
	 participant S as Streamlit App
	 participant O as EasyOCR
	 participant L as Azure OpenAI (LangChain)

	 U->>S: Upload Image
	 S->>O: Pass image for OCR
	 O-->>S: Return extracted text
	 S->>L: Send text & prompt
	 L-->>S: Return AI response
	 S->>U: Display result
	 U->>S: Ask follow-up
	 S->>L: Send conversation context
	 L-->>S: Return follow-up response
	 S->>U: Display follow-up
```

---

### 📝 Example Usage
1. Upload an image containing text.
2. Wait for OCR to extract the text.
3. Choose an action (Summarize, Analyze, Suggest Action, or Freeform Prompt).
4. View the AI's response and ask follow-up questions as needed.
