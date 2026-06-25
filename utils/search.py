
"""
=========================================================
search.py

AI Company Knowledge Assistant

Semantic Search Module

Features
--------
✔ Query Embeddings
✔ Cosine Similarity
✔ Top-K Retrieval
✔ Source Attribution
✔ Confidence Score
✔ Context Builder
=========================================================
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from utils.embedding import (
    get_model,
    load_embeddings
)


# ==========================================================
# Encode User Query
# ==========================================================

def encode_query(question: str):

    """
    Convert user question into embedding.
    """

    model = get_model()

    embedding = model.encode(

        question,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    return embedding


# ==========================================================
# Semantic Search
# ==========================================================

def semantic_search(
    question,
    top_k=5
):

    """
    Perform semantic search over document chunks.
    """

    chunk_df = load_embeddings()

    if chunk_df is None:

        raise Exception(
            "Embeddings not found.\nPlease process documents first."
        )

    if chunk_df.empty:

        raise Exception(
            "No document chunks available."
        )

    query_embedding = encode_query(question)

    embeddings = np.vstack(

        chunk_df["embedding"].values

    )

    similarity_scores = cosine_similarity(

        [query_embedding],

        embeddings

    )[0]

    results = chunk_df.copy()

    results["score"] = similarity_scores

    results = results.sort_values(

        by="score",

        ascending=False

    )

    results = results.reset_index(

        drop=True

    )

    return results.head(top_k)


# ==========================================================
# Build Context
# ==========================================================

def build_context(results):

    """
    Combine retrieved chunks into one context.
    """

    if results.empty:

        return ""

    context = []

    for _, row in results.iterrows():

        context.append(

            row["chunk"]

        )

    return "\n\n".join(context)


# ==========================================================
# Get Source Files
# ==========================================================

def get_sources(results):

    """
    Return unique source document names.
    """

    if results.empty:

        return []

    return list(

        results["filename"]

        .unique()

    )


# ==========================================================
# Confidence Score
# ==========================================================

def get_confidence(results):

    """
    Return highest similarity score.
    """

    if results.empty:

        return 0.0

    return round(

        float(

            results.iloc[0]["score"]

        ),

        4

    )


# ==========================================================
# Retrieve Documents
# ==========================================================

def retrieve_documents(
    question,
    top_k=5
):

    """
    Complete retrieval pipeline.
    """

    results = semantic_search(

        question,

        top_k

    )

    context = build_context(

        results

    )

    sources = get_sources(

        results

    )

    confidence = get_confidence(

        results

    )

    return {

        "context": context,

        "sources": sources,

        "confidence": confidence,

        "results": results

    }


# ==========================================================
# Search Statistics
# ==========================================================

def retrieval_statistics(results):

    """
    Return retrieval statistics.
    """

    if results.empty:

        return {

            "matches": 0,

            "best_score": 0

        }

    return {

        "matches": len(results),

        "best_score": get_confidence(results)

    }


# ==========================================================
# Pretty Print Results
# ==========================================================

def display_results(results):

    """
    Console display for debugging.
    """

    if results.empty:

        print("No Results Found")

        return

    print("=" * 80)

    print("TOP RETRIEVED CHUNKS")

    print("=" * 80)

    for i, (_, row) in enumerate(results.iterrows(), start=1):

        print(f"\nRank : {i}")

        print(f"File : {row['filename']}")

        print(f"Score: {row['score']:.4f}")

        print("-" * 60)

        print(row["chunk"][:400])

        print("-" * 60)


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    try:

        question = "What is the probation period?"

        output = retrieve_documents(

            question,

            top_k=5

        )

        print()

        print("=" * 80)

        print("Confidence")

        print(output["confidence"])

        print()

        print("Sources")

        print(output["sources"])

        print()

        print("Context")

        print(output["context"][:1000])

        print()

        display_results(

            output["results"]

        )

    except Exception as e:

        print(e)

