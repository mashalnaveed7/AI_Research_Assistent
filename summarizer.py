
from groq import Groq


def summarize_document(text, api_key):
    """
    Summarize a research paper using Groq.
    """

    client = Groq(
        api_key=api_key
    )


    prompt = f"""
You are an academic research assistant.

Read the following research paper and summarize it.

Use this format:

Title:

Objectives:

Methodology:

Key Findings:

Conclusion:


Research Paper:

{text[:15000]}
"""


    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )


    return response.choices[0].message.content
