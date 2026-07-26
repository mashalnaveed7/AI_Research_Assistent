
from groq import Groq


def compare_papers(paper_a, paper_b, api_key):
    """
    Compare two research papers using Groq.
    """

    client = Groq(
        api_key=api_key
    )


    prompt = f"""
You are an academic research assistant.

Compare these two research papers.

Create a Markdown comparison table with these sections:

Objective
Dataset
Methodology
Results
Future Work
Conclusion


Paper A:

{paper_a[:10000]}


Paper B:

{paper_b[:10000]}


Return only the comparison table.
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
