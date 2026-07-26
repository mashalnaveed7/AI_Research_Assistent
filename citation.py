
from groq import Groq


def generate_citation(text, api_key):
    """
    Generate APA 7 citation from research paper text using Groq.
    """

    client = Groq(
        api_key=api_key
    )


    prompt = f"""
You are an academic citation assistant.

Read the research paper information below and generate an APA 7th edition citation.

Find these details:

- Author(s)
- Paper title
- Publication year
- Journal name

Output format:

Author(s). (Year).
Title of paper.
Journal Name.


If any information cannot be identified, write:
"Not Available"


Research Paper:

{text[:8000]}
"""


    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )


    return response.choices[0].message.content
