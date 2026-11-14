import os

from dotenv import load_dotenv
from groq import Groq


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
# GENERATE ANSWER
# --------------------------------------------------

def get_answer(
    question,
    retrieved_chunks,
    chat_history=None,
    web_results=None,
    route=None
):

    # --------------------------------------------------
    # DOCUMENT CONTEXT
    # --------------------------------------------------

    context_parts = []


    for chunk in retrieved_chunks:

        document = chunk["document"]

        page = chunk["page"]

        text = chunk["text"]


        if page is not None:

            source = (
                f"{document}, Page {page}"
            )

        else:

            source = document


        context_parts.append(

            f"[Source: {source}]\n{text}"

        )


    document_context = "\n\n".join(
        context_parts
    )


    # --------------------------------------------------
    # WEB CONTEXT
    # --------------------------------------------------

    web_context_parts = []


    if web_results:

        for result in web_results:

            title = result["title"]

            url = result["url"]

            content = result["content"]


            web_context_parts.append(

                f"[Web Source: {title}]\n"
                f"URL: {url}\n"
                f"{content}"

            )


    web_context = "\n\n".join(
        web_context_parts
    )


    # --------------------------------------------------
    # CONVERSATION HISTORY
    # --------------------------------------------------

    history_text = ""


    if chat_history:

        history_parts = []


        for message in chat_history:

            role = message["role"]

            content = message["content"]


            if role == "user":

                history_parts.append(
                    f"User: {content}"
                )

            elif role == "assistant":

                history_parts.append(
                    f"Assistant: {content}"
                )


        history_text = "\n".join(
            history_parts
        )


    # --------------------------------------------------
    # ROUTE
    # --------------------------------------------------

    if route is None:

        route = "GENERAL"


    # --------------------------------------------------
    # PROMPT
    # --------------------------------------------------

    prompt = f"""
You are an intelligent AI assistant.

The AI routing agent selected:

{route}


AVAILABLE INFORMATION:

DOCUMENT CONTEXT:

{document_context}


WEB SEARCH CONTEXT:

{web_context}


CONVERSATION HISTORY:

{history_text}


CURRENT USER QUESTION:

{question}


IMPORTANT RULES:

1. Follow the selected route.

2. If the route is DOCUMENT:

   Use the uploaded document context
   to answer the question.

   Do not invent information that is
   not supported by the document.

3. If the route is WEB:

   Use the web search results to answer
   the question.

   Do not invent information that is
   not supported by the web results.

4. If the route is GENERAL:

   Answer using your general knowledge.

5. Use conversation history to understand
   follow-up questions and references.

6. Do not claim that web information came
   from the uploaded document.

7. Do not claim that general knowledge came
   from the uploaded document.

8. If the route is DOCUMENT, include:

   📄 Source: Document

9. If the route is WEB, include:

   🌐 Source: Web

10. If the route is GENERAL, include:

    🤖 Source: General Knowledge

11. If the available information is
    insufficient, clearly say so.

12. Give a clear and direct answer.

ANSWER:
"""


    # --------------------------------------------------
    # GROQ REQUEST
    # --------------------------------------------------

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[

            {
                "role":
                    "user",

                "content":
                    prompt

            }

        ],

        temperature=0

    )


    return response.choices[0].message.content