
"""
=========================================================
llm.py

AI Company Knowledge Assistant

LLM Module

Features
--------
✔ Google Gemini Integration
✔ Prompt Engineering
✔ Context-aware Answers
✔ Source Attribution
✔ Hallucination Prevention
✔ Error Handling
✔ Quota Handling
=========================================================
"""

import os

from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

from utils.search import retrieve_documents


# ==========================================================
# Load Environment Variables
# ==========================================================

def get_api_key():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
            
    if not api_key:
        raise Exception(
            "GEMINI_API_KEY not found. Please add it to your .env file or Streamlit secrets."
        )
        
    return api_key

# ==========================================================
# Configure Gemini
# ==========================================================

def configure_gemini():
    api_key = get_api_key()
    genai.configure(api_key=api_key)


# ==========================================================
# Load Gemini Model
# ==========================================================

MODEL = None


def initialize_model():

    """
    Initialize Gemini model.

    Tries models in order until one works.
    """

    global MODEL

    if MODEL is not None:

        return MODEL
        
    configure_gemini()

    candidate_models = [

        "gemini-2.5-flash",

        "gemini-2.0-flash",

        "gemini-1.5-flash"

    ]

    for model_name in candidate_models:

        try:

            MODEL = genai.GenerativeModel(
                model_name
            )

            print(f"Using Gemini Model : {model_name}")

            return MODEL

        except Exception:

            continue

    raise Exception(
        "No supported Gemini model available."
    )


# ==========================================================
# Prompt Builder
# ==========================================================

def build_prompt(
    question,
    context
):

    prompt = f"""
You are an AI Company Knowledge Assistant.

Use ONLY the supplied document context.

Rules:

1. Never use outside knowledge.

2. Never hallucinate.

3. If the answer is unavailable,
reply exactly:

Information not found in uploaded documents.

----------------------------

DOCUMENT CONTEXT

{context}

----------------------------

QUESTION

{question}

----------------------------

ANSWER

"""

    return prompt


# ==========================================================
# Ask Gemini
# ==========================================================

def ask_llm(prompt):

    model = initialize_model()

    response = model.generate_content(
        prompt
    )

    return response.text.strip()


# ==========================================================
# Generate Final Answer
# ==========================================================

def generate_answer(
    question,
    top_k=5
):

    retrieval = retrieve_documents(
        question,
        top_k
    )

    context = retrieval["context"]

    sources = retrieval["sources"]

    confidence = retrieval["confidence"]

    if context.strip() == "":

        return {

            "answer":
            "Information not found in uploaded documents.",

            "sources": [],

            "confidence": 0

        }

    prompt = build_prompt(
        question,
        context
    )

    try:

        answer = ask_llm(prompt)

    except Exception as e:

        error = str(e)

        # Gemini quota exceeded
        if "429" in error:

            answer = (
                "Gemini API quota exceeded.\n\n"
                "Showing retrieved document context instead:\n\n"
                + context[:1500]
            )

        else:

            answer = (
                "Gemini Error:\n\n"
                + error
            )

    return {

        "answer": answer,

        "sources": sources,

        "confidence": confidence

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    question = "What is the probation period?"

    result = generate_answer(question)

    print()

    print("=" * 80)

    print("ANSWER")

    print(result["answer"])

    print()

    print("=" * 80)

    print("SOURCES")

    print(result["sources"])

    print()

    print("=" * 80)

    print("CONFIDENCE")

    print(result["confidence"])


