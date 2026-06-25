
"""
=========================================================
AI Powered Company Knowledge Assistant

Main Streamlit Application

Features
--------
✔ Document Upload
✔ Document Processing
✔ Semantic Search
✔ Gemini AI
✔ Analytics Dashboard
✔ Query History
=========================================================
"""

import os
import shutil
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from utils.pdf_reader import (
    extract_all_documents,
    get_document_statistics
)

from utils.embedding import (
    process_documents,
    get_statistics
)

from utils.llm import (
    generate_answer
)

# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(

    page_title="AI Company Knowledge Assistant",

    page_icon="🤖",

    layout="wide"

)

# ==========================================================
# Project Folders
# ==========================================================

DOCUMENT_FOLDER = "documents"

DATA_FOLDER = "data"

HISTORY_FILE = "query_history.csv"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)

os.makedirs(
    DATA_FOLDER,
    exist_ok=True
)

# ==========================================================
# Query History Initialization
# ==========================================================

if not os.path.exists(HISTORY_FILE):

    history = pd.DataFrame(

        columns=[

            "Question",

            "Answer",

            "Source",

            "Confidence",

            "ResponseTime",

            "Timestamp"

        ]

    )

    history.to_csv(

        HISTORY_FILE,

        index=False

    )

# ==========================================================
# Helper Functions
# ==========================================================

def save_uploaded_files(uploaded_files):

    """
    Save uploaded documents.
    """

    saved = 0

    for uploaded_file in uploaded_files:

        save_path = os.path.join(

            DOCUMENT_FOLDER,

            uploaded_file.name

        )

        with open(

            save_path,

            "wb"

        ) as file:

            file.write(

                uploaded_file.getbuffer()

            )

        saved += 1

    return saved


def clear_documents():

    """
    Delete all uploaded documents.
    """

    if os.path.exists(DOCUMENT_FOLDER):

        shutil.rmtree(DOCUMENT_FOLDER)

    os.makedirs(
        DOCUMENT_FOLDER,
        exist_ok=True
    )


def load_history():

    """
    Read query history.
    """

    return pd.read_csv(
        HISTORY_FILE
    )


def save_history(

        question,

        answer,

        source,

        confidence,

        response_time

):

    """
    Save query history.
    """

    history = load_history()

    history.loc[len(history)] = [

        question,

        answer,

        source,

        confidence,

        response_time,

        datetime.now()

    ]

    history.to_csv(

        HISTORY_FILE,

        index=False

    )


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title(
    "📚 Company Knowledge Assistant"
)

page = st.sidebar.radio(

    "Navigation",

    [

        "📂 Document Upload",

        "💬 Ask Questions"

    ]

)

st.sidebar.divider()

stats = get_statistics()

st.sidebar.metric(

    "📂 Documents",

    stats["documents"]

)

st.sidebar.metric(

    "🧩 Chunks",

    stats["chunks"]

)

st.sidebar.metric(

    "❓ Queries",

    len(load_history())

)

st.sidebar.divider()

st.sidebar.info(

    """
Supported Files

• PDF

• DOCX

• TXT
"""

)

st.sidebar.caption(

    "AI Powered Company Knowledge Assistant"

)


# ==========================================================
# PAGE 1 : DOCUMENT UPLOAD
# ==========================================================

if page == "📂 Document Upload":

    st.title("📂 Document Upload")

    st.markdown(
        """
Upload company documents for AI-powered question answering.

### Supported File Types
- PDF
- DOCX
- TXT
"""
    )

    uploaded_files = st.file_uploader(
        "Choose Documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    # ======================================================
    # Display Uploaded Files
    # ======================================================

    if uploaded_files:

        st.subheader("📄 Uploaded Files")

        uploaded_df = pd.DataFrame({

            "File Name": [

                file.name

                for file in uploaded_files

            ],

            "Size (KB)": [

                round(file.size / 1024, 2)

                for file in uploaded_files

            ]

        })

        st.dataframe(

            uploaded_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No documents uploaded.")

    st.divider()

    # ======================================================
    # Buttons
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        save_btn = st.button(

            "💾 Save Documents",

            use_container_width=True

        )

    with col2:

        process_btn = st.button(

            "⚙ Process Documents",

            use_container_width=True

        )

    with col3:

        clear_btn = st.button(

            "🗑 Clear Documents",

            use_container_width=True

        )

    # ======================================================
    # Save Documents
    # ======================================================

    if save_btn:

        if not uploaded_files:

            st.warning(
                "Please upload at least one document."
            )

        else:

            saved = save_uploaded_files(

                uploaded_files

            )

            st.success(

                f"{saved} document(s) saved successfully."

            )

    # ======================================================
    # Clear Documents
    # ======================================================

    if clear_btn:

        clear_documents()

        st.success(
            "All uploaded documents removed."
        )

    # ======================================================
    # Process Documents
    # ======================================================

    if process_btn:

        try:

            docs = extract_all_documents(

                DOCUMENT_FOLDER

            )

            if len(docs) == 0:

                st.error(
                    """
No readable documents found.

Possible reasons:

• Documents not saved

• Empty document

• Scanned PDF (contains images only)

Please upload readable documents.
"""
                )

                st.stop()

            progress = st.progress(0)

            status = st.empty()

            status.info("Extracting text...")

            progress.progress(20)

            time.sleep(0.5)

            status.info("Creating text chunks...")

            progress.progress(40)

            time.sleep(0.5)

            status.info("Generating embeddings...")

            chunk_df = process_documents(

                docs

            )

            progress.progress(80)

            time.sleep(0.5)

            progress.progress(100)

            status.success(
                "Processing Completed Successfully."
            )

            st.success(

                f"{len(chunk_df)} chunks generated."

            )

        except Exception as e:

            st.exception(e)

    # ======================================================
    # Statistics
    # ======================================================

    st.divider()

    st.subheader("📊 Document Statistics")

    total_documents = len(

        os.listdir(

            DOCUMENT_FOLDER

        )

    )

    pages = 0

    try:

        docs = extract_all_documents(

            DOCUMENT_FOLDER

        )

        stats = get_document_statistics(

            docs

        )

        pages = stats["pages"]

    except:

        pass

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "📂 Total Uploaded Documents",

            total_documents

        )

    with col2:

        st.metric(

            "📄 Total Processed Pages",

            pages

        )

    st.divider()

    st.subheader("📁 Saved Documents")

    saved_files = os.listdir(

        DOCUMENT_FOLDER

    )

    if len(saved_files) == 0:

        st.info(
            "No saved documents."
        )

    else:

        for file in saved_files:

            st.success(file)

# ==========================================================
# PAGE 2 : ASK QUESTIONS
# ==========================================================

elif page == "💬 Ask Questions":

    st.title("💬 Ask Questions")

    st.markdown(
        """
Ask questions about the uploaded company documents.

The AI retrieves the most relevant document chunks and
generates an answer using Google Gemini.
"""
    )

    # ======================================================
    # Check Embeddings
    # ======================================================

    embedding_file = os.path.join(
        DATA_FOLDER,
        "embeddings.pkl"
    )

    if not os.path.exists(embedding_file):

        st.warning(
            """
No processed documents found.

Please go to **Document Upload**
and click **Process Documents** first.
"""
        )

        st.stop()

    # ======================================================
    # Question Input
    # ======================================================

    question = st.text_area(

        "Enter your question",

        placeholder="Example:\nWhat is the probation period?",

        height=120

    )

    col1, col2 = st.columns([1, 1])

    with col1:

        ask_button = st.button(

            "🤖 Generate Answer",

            use_container_width=True

        )

    with col2:

        clear_button = st.button(

            "🗑 Clear Question",

            use_container_width=True

        )

    if clear_button:

        st.rerun()

    # ======================================================
    # Generate Answer
    # ======================================================

    if ask_button:

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

            st.stop()

        with st.spinner(

            "Searching documents and generating answer..."

        ):

            start_time = time.time()

            result = generate_answer(question)

            response_time = round(

                time.time() - start_time,

                2

            )

            answer = result["answer"]

            sources = result["sources"]

            confidence = result["confidence"]

        # ==================================================
        # Answer
        # ==================================================

        st.divider()

        st.subheader("🤖 AI Generated Answer")

        st.success(answer)

        # ==================================================
        # Sources
        # ==================================================

        st.subheader("📄 Source Documents")

        if len(sources) == 0:

            st.warning(
                "No source document found."
            )

        else:

            for source in sources:

                st.info(source)

        # ==================================================
        # Metrics
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Confidence Score",

                confidence

            )

        with col2:

            st.metric(

                "Response Time",

                f"{response_time} sec"

            )

        # ==================================================
        # Save Query History
        # ==================================================

        save_history(

            question=question,

            answer=answer,

            source=",".join(sources),

            confidence=confidence,

            response_time=response_time

        )

        st.success(
            "Query saved successfully."
        )

        # ==================================================
        # Download Answer
        # ==================================================

        st.download_button(

            label="📥 Download Answer",

            data=answer,

            file_name="answer.txt",

            mime="text/plain"

        )


    # ======================================================
    # ANALYTICS DASHBOARD
    # ======================================================

    st.divider()

    st.header("📊 Document Analytics Dashboard")

    history = load_history()

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    total_documents = len(os.listdir(DOCUMENT_FOLDER))

    total_queries = len(history)

    average_response_time = 0

    if total_queries > 0:

        average_response_time = round(

            history["ResponseTime"].mean(),

            2

        )

    total_pages = 0

    try:

        docs = extract_all_documents(

            DOCUMENT_FOLDER

        )

        stats = get_document_statistics(

            docs

        )

        total_pages = stats["pages"]

    except:

        pass

    # ------------------------------------------------------
    # Dashboard Metrics
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "📂 Total Uploaded Documents",

            total_documents

        )

    with col2:

        st.metric(

            "📄 Total Processed Pages",

            total_pages

        )

    col3, col4 = st.columns(2)

    with col3:

        st.metric(

            "❓ Total Queries",

            total_queries

        )

    with col4:

        st.metric(

            "⚡ Average Response Time",

            f"{average_response_time} sec"

        )

    # ------------------------------------------------------
    # Most Searched Topics
    # ------------------------------------------------------

    st.divider()

    st.subheader("🔥 Most Searched Topics")

    if total_queries > 0:

        words = []

        stop_words = {

            "what",
            "who",
            "where",
            "when",
            "why",
            "how",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "of",
            "to",
            "for",
            "in",
            "on",
            "at",
            "with",
            "does",
            "do",
            "did",
            "please"

        }

        for question in history["Question"]:

            question = str(question)

            for word in question.lower().split():

                word = word.strip(".,?!()[]{}")

                if (

                    len(word) > 2

                    and word not in stop_words

                ):

                    words.append(word)

        if len(words) > 0:

            topic_df = (

                pd.Series(words)

                .value_counts()

                .head(10)

            )

            st.bar_chart(topic_df)

        else:

            st.info(

                "No searchable topics available."

            )

    else:

        st.info(

            "No questions have been asked yet."

        )

    # ------------------------------------------------------
    # Query History
    # ------------------------------------------------------

    st.divider()

    st.subheader("🕒 Query History")

    if total_queries == 0:

        st.info(

            "No query history found."

        )

    else:

        st.dataframe(

            history,

            use_container_width=True,

            hide_index=True,

            height=350

        )

    # ------------------------------------------------------
    # Download Query History
    # ------------------------------------------------------

    if total_queries > 0:

        csv = history.to_csv(

            index=False

        ).encode("utf-8")

        st.download_button(

            label="📥 Download Query History",

            data=csv,

            file_name="query_history.csv",

            mime="text/csv"

        )

    # ------------------------------------------------------
    # Footer
    # ------------------------------------------------------

    st.divider()

    st.markdown(

        """
---
### 🤖 AI Powered Company Knowledge Assistant

**Technology Stack**

- Streamlit
- Google Gemini
- Sentence Transformers
- Pandas
- Scikit-Learn
- PyPDF2
- Python-Docx

---

**Assignment Features**

✅ PDF Upload

✅ DOCX Upload

✅ TXT Upload

✅ Document Processing

✅ Pandas Storage

✅ Text Chunking

✅ Embeddings

✅ Semantic Search

✅ Gemini Integration

✅ Source Attribution

✅ Error Handling

✅ Analytics Dashboard

✅ Query History

✅ Streamlit Deployment Ready

---

Made for **Company Knowledge Assistant Assignment**
"""
    )

