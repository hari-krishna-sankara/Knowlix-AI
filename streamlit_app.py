import streamlit as st

from document_processor import extract_text
from rag import RAGEngine
from chatbot_engine import get_answer
from web_search import search_web
from router import route_question


# --------------------------------------------------
# STREAMLIT PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Knowlix AI",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🧠 Knowlix AI")

st.subheader(
    "Intelligent Document Management & Retrieval Platform"
)

st.markdown(
    "*Turn Your Documents Into Knowledge.*"
)

st.write(
    "Upload your documents, ask questions, "
    "and discover information with AI-powered search."
)

st.divider()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "rag" not in st.session_state:
    st.session_state.rag = RAGEngine()


if "documents" not in st.session_state:
    st.session_state.documents = []


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# DOCUMENT UPLOADER
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload your documents",
    type=[
        "pdf",
        "docx",
        "txt"
    ],
    accept_multiple_files=True
)


# --------------------------------------------------
# PROCESS UPLOADED DOCUMENTS
# --------------------------------------------------

if uploaded_files:

    uploaded_names = sorted(
        file.name
        for file in uploaded_files
    )

    existing_names = sorted(
        document["name"]
        for document in st.session_state.documents
    )

    if uploaded_names != existing_names:

        with st.spinner("Reading documents..."):

            try:

                documents = []

                for uploaded_file in uploaded_files:

                    pages = extract_text(
                        uploaded_file
                    )

                    has_text = any(
                        page["text"].strip()
                        for page in pages
                    )

                    if has_text:

                        documents.append({
                            "name": uploaded_file.name,
                            "pages": pages
                        })

                if not documents:

                    st.error(
                        "No readable text found."
                    )

                else:

                    st.session_state.documents = documents

                    st.session_state.rag.create_index(
                        documents
                    )

                    st.session_state.chat_history = []

                    st.success(
                        f"{len(documents)} document(s) loaded."
                    )

            except Exception as e:

                st.error(
                    f"Error processing documents: {e}"
                )


# --------------------------------------------------
# DISPLAY UPLOADED DOCUMENTS
# --------------------------------------------------

if st.session_state.documents:

    st.subheader("📚 Uploaded Documents")

    for document in st.session_state.documents:

        st.write(
            f"📄 {document['name']}"
        )


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask a question..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if question:

    # --------------------------------------------------
    # DISPLAY USER QUESTION
    # --------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            question
        )


    # --------------------------------------------------
    # SAVE USER QUESTION
    # --------------------------------------------------

    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })


    # --------------------------------------------------
    # AI ROUTER
    # --------------------------------------------------

    with st.spinner(
        "Understanding your question..."
    ):

        try:

            route = route_question(
                question,
                has_documents=bool(
                    st.session_state.documents
                )
            )

        except Exception as e:

            st.warning(
                f"Router failed: {e}"
            )

            route = "GENERAL"


    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------
    # If there are no documents but the router
    # accidentally selects DOCUMENT, use GENERAL.

    if (
        route == "DOCUMENT"
        and not st.session_state.documents
    ):

        route = "GENERAL"


    # --------------------------------------------------
    # VARIABLES
    # --------------------------------------------------

    relevant_chunks = []

    web_results = []


    # --------------------------------------------------
    # DOCUMENT ROUTE
    # --------------------------------------------------

    if route == "DOCUMENT":

        with st.spinner(
            "Searching documents..."
        ):

            try:

                relevant_chunks = (
                    st.session_state.rag.search_top_chunks(
                        question,
                        top_k=5
                    )
                )

            except Exception as e:

                st.warning(
                    f"Document search failed: {e}"
                )

                relevant_chunks = []


    # --------------------------------------------------
    # WEB ROUTE
    # --------------------------------------------------

    elif route == "WEB":

        with st.spinner(
            "Searching the web..."
        ):

            try:

                web_results = search_web(
                    question,
                    max_results=5
                )

            except Exception as e:

                st.warning(
                    f"Web search failed: {e}"
                )

                web_results = []


    # --------------------------------------------------
    # GENERAL ROUTE
    # --------------------------------------------------

    elif route == "GENERAL":

        relevant_chunks = []

        web_results = []


    # --------------------------------------------------
    # GENERATE ANSWER
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Generating answer..."
        ):

            try:

                # Use previous conversation history,
                # without duplicating the current question.

                previous_chat_history = (
                    st.session_state.chat_history[:-1]
                )

                answer = get_answer(
                    question,
                    relevant_chunks,
                    previous_chat_history,
                    web_results,
                    route
                )

            except Exception as e:

                answer = (
                    f"Error generating answer: {e}"
                )


        st.markdown(answer)


        # --------------------------------------------------
        # DOCUMENT SOURCES
        # --------------------------------------------------

        if "📄 Source: Document" in answer:

            sources = []

            for chunk in relevant_chunks:

                document = chunk["document"]

                page = chunk["page"]

                if page is not None:

                    source = (
                        f"{document} — Page {page}"
                    )

                else:

                    source = document

                sources.append(source)


            sources = sorted(
                set(sources)
            )


            if sources:

                with st.expander(
                    "📄 Sources"
                ):

                    for source in sources:

                        st.write(
                            f"• {source}"
                        )


        # --------------------------------------------------
        # WEB SOURCES
        # --------------------------------------------------

        if "🌐 Source: Web" in answer:

            if web_results:

                with st.expander(
                    "🌐 Web Sources"
                ):

                    for result in web_results:

                        title = result["title"]

                        url = result["url"]


                        st.markdown(
                            f"**{title}**"
                        )


                        st.markdown(
                            url
                        )


    # --------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })