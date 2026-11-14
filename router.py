import os

from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# --------------------------------------------------
# AI ROUTER
# --------------------------------------------------

def route_question(
    question,
    has_documents=True
):

    if has_documents:

        document_status = """
Uploaded documents are available.
The user may be asking about them.
"""

    else:

        document_status = """
No documents are currently available.
"""


    prompt = f"""
You are an AI routing agent.

Your job is to decide which source should
handle the user's question.

Available routes:

DOCUMENT
WEB
GENERAL


DOCUMENT:

Choose DOCUMENT when the user is asking
about uploaded documents, PDFs, notices,
files, their contents, summaries,
explanations, or information that should
come from the uploaded documents.


WEB:

Choose WEB when the question requires
current, recent, live, real-time, or
up-to-date information.

Examples:

- latest news
- today's weather
- current price
- latest software version
- recent events
- current stock price


GENERAL:

Choose GENERAL when the question is a
stable general-knowledge question and
does not require uploaded documents or
current web information.


{document_status}


USER QUESTION:

{question}


Return ONLY ONE of these words:

DOCUMENT
WEB
GENERAL

Do not return explanations.
Do not return punctuation.
"""


    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0

    )


    route = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .upper()
    )


    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------

    if route not in [
        "DOCUMENT",
        "WEB",
        "GENERAL"
    ]:

        route = "GENERAL"


    return route