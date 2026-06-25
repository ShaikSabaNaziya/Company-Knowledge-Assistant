"""
=========================================================
embedding.py

AI Company Knowledge Assistant

Handles:
    ✔ Text Chunking
    ✔ Embedding Generation
    ✔ Pandas Storage
    ✔ Save Chunks
    ✔ Save Embeddings
=========================================================
"""

import os
import pickle

import pandas as pd
from sentence_transformers import SentenceTransformer


# ==========================================================
# Configuration
# ==========================================================

DATA_FOLDER = "data"

DOCUMENT_FILE = os.path.join(
    DATA_FOLDER,
    "documents.pkl"
)

CHUNK_FILE = os.path.join(
    DATA_FOLDER,
    "chunks.pkl"
)

EMBEDDING_FILE = os.path.join(
    DATA_FOLDER,
    "embeddings.pkl"
)

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


# ==========================================================
# Load Sentence Transformer
# ==========================================================

def get_model():

    global _model

    if _model is None:

        print("Loading embedding model...")

        _model = SentenceTransformer(
            MODEL_NAME
        )

    return _model


# ==========================================================
# Text Chunking
# ==========================================================

def chunk_text(
    text,
    chunk_size=500,
    overlap=100
):

    chunks = []

    if text is None:
        return chunks

    text = str(text).strip()

    if text == "":
        return chunks

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:

            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ==========================================================
# Create Chunk DataFrame
# ==========================================================

def create_chunk_dataframe(documents):

    rows = []

    for document in documents:

        filename = document["filename"]

        content = document["content"]

        chunks = chunk_text(content)

        for index, chunk in enumerate(chunks):

            rows.append({

                "filename": filename,

                "chunk_id": index,

                "chunk": chunk

            })

    chunk_df = pd.DataFrame(rows)

    return chunk_df


# ==========================================================
# Generate Embeddings
# ==========================================================

def generate_embeddings(chunk_df):

    if chunk_df.empty:

        raise Exception(
            "Chunk DataFrame is empty."
        )

    model = get_model()

    embeddings = model.encode(

        chunk_df["chunk"].tolist(),

        show_progress_bar=True,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    chunk_df = chunk_df.copy()

    chunk_df["embedding"] = list(
        embeddings
    )

    return chunk_df


# ==========================================================
# Save Files
# ==========================================================

def save_documents(documents):

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )

    df = pd.DataFrame(documents)

    df.to_pickle(
        DOCUMENT_FILE
    )


def save_chunks(chunk_df):

    chunk_df.to_pickle(
        CHUNK_FILE
    )


def save_embeddings(chunk_df):

    with open(

        EMBEDDING_FILE,

        "wb"

    ) as file:

        pickle.dump(

            chunk_df,

            file

        )


# ==========================================================
# Load Embeddings
# ==========================================================

def load_embeddings():

    if not os.path.exists(
        EMBEDDING_FILE
    ):

        return None

    with open(

        EMBEDDING_FILE,

        "rb"

    ) as file:

        return pickle.load(file)


# ==========================================================
# Main Processing
# ==========================================================

def process_documents(documents):

    if len(documents) == 0:

        raise Exception(
            "No readable documents found."
        )

    save_documents(documents)

    chunk_df = create_chunk_dataframe(
        documents
    )

    if chunk_df.empty:

        raise Exception(
            "No chunks generated."
        )

    chunk_df = generate_embeddings(
        chunk_df
    )

    save_chunks(chunk_df)

    save_embeddings(chunk_df)

    return chunk_df


# ==========================================================
# Statistics
# ==========================================================

def get_statistics():

    stats = {

        "documents": 0,

        "chunks": 0

    }

    if os.path.exists(DOCUMENT_FILE):

        docs = pd.read_pickle(
            DOCUMENT_FILE
        )

        stats["documents"] = len(docs)

    embeddings = load_embeddings()

    if embeddings is not None:

        stats["chunks"] = len(
            embeddings
        )

    return stats


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print(get_statistics())
    