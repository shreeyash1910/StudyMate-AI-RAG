import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


PROJECT_ROOT = Path(__file__).resolve().parents[3]

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        f"GROQ_API_KEY is not set. "
        f"Expected .env file at: {ENV_FILE}"
    )


client = Groq(
    api_key=api_key
)


def generate_answer(
    question: str,
    context: str
):

    prompt = f"""
You are a helpful study assistant.

Your job is to answer the student's question
using ONLY the provided study material.

Rules:

1. Use the provided study material.
2. Do not invent facts.
3. If the answer is not present in the
   study material, say:

"I could not find the answer in your
uploaded study material."

4. Explain the answer in simple language.
5. For technical questions, use examples
   when appropriate.

STUDY MATERIAL:
{context}

STUDENT QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant "
                    "that answers questions from "
                    "uploaded study material."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_tokens=800
    )

    return response.choices[0].message.content