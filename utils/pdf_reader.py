"""
=========================================================
pdf_reader.py

AI Company Knowledge Assistant

Handles:
    • PDF
    • DOCX
    • TXT

Features:
    ✔ Extract document text
    ✔ Extract metadata
    ✔ Estimate pages
    ✔ Read entire documents folder
    ✔ Error handling
=========================================================
"""

import os
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


SUPPORTED_FILES = [
    ".pdf",
    ".docx",
    ".txt"
]


# ==========================================================
# PDF
# ==========================================================

def read_pdf(file_path):

    text = ""

    try:

        reader = PdfReader(file_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    except Exception as e:

        print(f"PDF Error : {e}")

    return text.strip()


# ==========================================================
# DOCX
# ==========================================================

def read_docx(file_path):

    text = ""

    try:

        document = Document(file_path)

        for para in document.paragraphs:

            if para.text:

                text += para.text + "\n"

    except Exception as e:

        print(f"DOCX Error : {e}")

    return text.strip()


# ==========================================================
# TXT
# ==========================================================

def read_txt(file_path):

    try:

        with open(

            file_path,

            "r",

            encoding="utf-8",

            errors="ignore"

        ) as file:

            return file.read().strip()

    except Exception as e:

        print(f"TXT Error : {e}")

        return ""


# ==========================================================
# Detect File Type
# ==========================================================

def extract_document(file_path):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":

        return read_pdf(file_path)

    elif extension == ".docx":

        return read_docx(file_path)

    elif extension == ".txt":

        return read_txt(file_path)

    return ""


# ==========================================================
# Estimate Pages
# ==========================================================

def estimate_pages(text):

    characters_per_page = 3000

    return max(

        1,

        len(text) // characters_per_page

    )


# ==========================================================
# Metadata
# ==========================================================

def get_metadata(file_path, text):

    return {

        "filename":

            os.path.basename(file_path),

        "extension":

            Path(file_path).suffix.lower(),

        "size_kb":

            round(

                os.path.getsize(file_path) / 1024,

                2

            ),

        "pages":

            estimate_pages(text)

    }


# ==========================================================
# Read Entire Folder
# ==========================================================

def extract_all_documents(folder="documents"):

    documents = []

    os.makedirs(folder, exist_ok=True)

    files = sorted(os.listdir(folder))

    for filename in files:

        path = os.path.join(

            folder,

            filename

        )

        if not os.path.isfile(path):

            continue

        extension = Path(path).suffix.lower()

        if extension not in SUPPORTED_FILES:

            continue

        print(f"Reading {filename}")

        text = extract_document(path)

        if len(text.strip()) == 0:

            print(

                f"Skipped : {filename} (No readable text)"

            )

            continue

        metadata = get_metadata(

            path,

            text

        )

        documents.append({

            "filename":

                metadata["filename"],

            "extension":

                metadata["extension"],

            "pages":

                metadata["pages"],

            "size_kb":

                metadata["size_kb"],

            "content":

                text

        })

    print()

    print("=" * 50)

    print(

        f"Documents Loaded : {len(documents)}"

    )

    print("=" * 50)

    return documents


# ==========================================================
# Statistics
# ==========================================================

def get_document_statistics(documents):

    total_pages = 0

    total_size = 0

    for doc in documents:

        total_pages += doc["pages"]

        total_size += doc["size_kb"]

    return {

        "documents":

            len(documents),

        "pages":

            total_pages,

        "size_mb":

            round(

                total_size / 1024,

                2

            )

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    docs = extract_all_documents("documents")

    stats = get_document_statistics(docs)

    print()

    print(stats)

    print()

    for doc in docs:

        print("-" * 50)

        print(doc["filename"])

        print(f"Pages : {doc['pages']}")

        print(f"Size  : {doc['size_kb']} KB")

        print(doc["content"][:500])

        print()
        