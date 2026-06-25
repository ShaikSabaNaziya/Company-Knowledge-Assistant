````markdown
# 🤖 AI Powered Company Knowledge Assistant

An intelligent Retrieval-Augmented Generation (RAG) application that allows users to upload company documents and ask questions using Google Gemini AI. The system retrieves relevant document content through semantic search and generates accurate answers with source attribution.

---

# 📌 Project Overview

This project implements an enterprise-style Company Knowledge Assistant using Retrieval-Augmented Generation (RAG). Users can upload organizational documents (PDF, DOCX, TXT), which are processed into vector embeddings using Sentence Transformers. When a question is asked, the system retrieves the most relevant document chunks using semantic search and sends them to Google Gemini to generate an answer based only on the uploaded documents.

---

# 🚀 Features

## Mandatory Features

- ✅ Upload PDF Documents
- ✅ Upload DOCX Documents
- ✅ Upload TXT Documents
- ✅ Document Processing
- ✅ Pandas Data Storage
- ✅ Text Chunking
- ✅ Sentence Transformer Embeddings
- ✅ Semantic Search
- ✅ Google Gemini Integration
- ✅ AI Generated Answers
- ✅ Source Document Attribution
- ✅ Error Handling
- ✅ Streamlit Interface
- ✅ Streamlit Cloud Deployment Ready

---

## Bonus Features

- 📊 Document Analytics Dashboard
- 📂 Total Uploaded Documents
- 📄 Total Processed Pages
- ❓ Query History
- 🔥 Most Searched Topics
- ⚡ Average Response Time
- 📥 Download Query History
- 📈 Interactive Charts

---

# 🏗️ Project Architecture

```
               User Uploads Documents
                        │
                        ▼
             PDF / DOCX / TXT Reader
                        │
                        ▼
               Text Extraction
                        │
                        ▼
              Pandas DataFrame Storage
                        │
                        ▼
               Text Chunking
                        │
                        ▼
         Sentence Transformer Embeddings
                        │
                        ▼
               Vector Embeddings
                        │
                        ▼
                Semantic Search
                        │
                        ▼
              Top Relevant Chunks
                        │
                        ▼
                 Google Gemini
                        │
                        ▼
          AI Generated Answer + Source
```

---

# 📂 Project Structure

```
company-knowledge-assistant/
│
├── app.py
├── requirements.txt
├── documents/
├── data/
├── utils/
│   ├── pdf_reader.py
│   ├── embedding.py
│   ├── search.py
│   └── llm.py
├── README.md
└── .env
```

---

# 💻 Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| LLM | Google Gemini |
| Embeddings | Sentence Transformers |
| Vector Search | Cosine Similarity |
| Data Storage | Pandas |
| PDF Processing | PyPDF2 |
| DOCX Processing | python-docx |
| ML | Scikit-Learn |

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/company-knowledge-assistant.git
```

---

## Change Directory

```bash
cd company-knowledge-assistant
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📖 How It Works

### Step 1

Upload company documents.

### Step 2

Click **Process Documents**.

### Step 3

Embeddings are generated.

### Step 4

Ask any question.

### Step 5

Semantic search retrieves relevant chunks.

### Step 6

Gemini generates an answer.

### Step 7

Source document is displayed.

---

# 📊 Dashboard

The dashboard provides:

- Total Uploaded Documents
- Total Processed Pages
- Query History
- Most Searched Topics
- Average Response Time
- Download Query History

---

# 📸 Screenshots

Add screenshots here.

```
screenshots/

upload_page.png

ask_questions.png

analytics_dashboard.png
```

---

# 🌐 Deployment

Deploy on Streamlit Community Cloud.

1. Push project to GitHub.
2. Login to Streamlit Community Cloud.
3. Create a new app.
4. Connect GitHub repository.
5. Add `GEMINI_API_KEY` as a secret.
6. Deploy.

---

# 📋 Git Commit History

Recommended commits:

```text
Initial project setup

Added document extraction module

Implemented text chunking

Generated embeddings

Implemented semantic search

Integrated Gemini API

Developed Streamlit UI

Added analytics dashboard

Added query history

Improved error handling

Updated README

Deployed application
```

---

# 🔮 Future Enhancements

- OCR Support for Scanned PDFs
- FAISS Vector Database
- ChromaDB Integration
- Multi-user Authentication
- Chat History Persistence
- Document Summarization
- Speech-to-Text Queries
- Voice Responses
- Multi-language Support
- Docker Deployment

---

# 🧪 Testing Checklist

- Upload PDF ✔
- Upload DOCX ✔
- Upload TXT ✔
- Process Documents ✔
- Generate Embeddings ✔
- Ask Questions ✔
- Display Source ✔
- Dashboard ✔
- Query History ✔
- Deployment ✔

---

# 📚 Learning Outcomes

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Large Language Model Integration
- Semantic Search
- Vector Embeddings
- Document Intelligence
- Streamlit Development
- Prompt Engineering
- Data Processing with Pandas
- Machine Learning Fundamentals

---

# 👩‍💻 Author

**Saba Naziya**

POSITION : TEAM LEAD at SPIRIT DATA SOLUTIONS 
ROLE : AI & Python Developer

---

# ⭐ Acknowledgements

- Google Gemini
- Sentence Transformers
- Streamlit
- Scikit-Learn
- PyPDF2
- python-docx
- Hugging Face

---

## ⭐ If you found this project useful, consider giving it a star on GitHub.
````
