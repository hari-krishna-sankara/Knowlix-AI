from sentence_transformers import SentenceTransformer
import faiss
import streamlit as st


# --------------------------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------------------------

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


# --------------------------------------------------
# RAG ENGINE
# --------------------------------------------------

class RAGEngine:

    def __init__(self):

        self.model = load_embedding_model()

        self.index = None

        self.chunks = []


    # --------------------------------------------------
    # SPLIT TEXT
    # --------------------------------------------------

    def split_text(
        self,
        pages,
        document_name,
        chunk_size=500,
        overlap=100
    ):

        chunks = []

        for page_data in pages:

            text = page_data["text"]

            page_number = page_data["page"]

            words = text.split()

            start = 0


            while start < len(words):

                end = start + chunk_size

                chunk_text = " ".join(
                    words[start:end]
                )


                if chunk_text.strip():

                    chunks.append({

                        "text": chunk_text,

                        "page": page_number,

                        "document": document_name

                    })


                start += chunk_size - overlap


        return chunks


    # --------------------------------------------------
    # CREATE INDEX
    # --------------------------------------------------

    def create_index(self, documents):

        self.chunks = []


        for document in documents:

            pages = document["pages"]

            document_name = document["name"]


            document_chunks = self.split_text(

                pages,

                document_name

            )


            self.chunks.extend(
                document_chunks
            )


        if not self.chunks:

            raise ValueError(
                "No text found in the documents."
            )


        texts = [

            chunk["text"]

            for chunk in self.chunks

        ]


        embeddings = self.model.encode(

            texts,

            convert_to_numpy=True,

            normalize_embeddings=True

        )


        dimension = embeddings.shape[1]


        self.index = faiss.IndexFlatIP(
            dimension
        )


        self.index.add(

            embeddings.astype(
                "float32"
            )

        )


    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def search(

        self,

        question,

        top_k=5,

        threshold=0.30

    ):

        if self.index is None:

            raise ValueError(
                "No documents have been indexed."
            )


        question_embedding = self.model.encode(

            [question],

            convert_to_numpy=True,

            normalize_embeddings=True

        )


        scores, indices = self.index.search(

            question_embedding.astype(
                "float32"
            ),

            top_k

        )


        results = []


        for score, index in zip(

            scores[0],

            indices[0]

        ):

            if (

                index != -1

                and index < len(self.chunks)

                and score >= threshold

            ):

                chunk = self.chunks[index].copy()

                chunk["score"] = float(
                    score
                )

                results.append(chunk)


        return results


    # --------------------------------------------------
    # SEARCH TOP CHUNKS
    # Used for broad document questions
    # --------------------------------------------------

    def search_top_chunks(

        self,

        question,

        top_k=3

    ):

        if self.index is None:

            raise ValueError(
                "No documents have been indexed."
            )


        question_embedding = self.model.encode(

            [question],

            convert_to_numpy=True,

            normalize_embeddings=True

        )


        scores, indices = self.index.search(

            question_embedding.astype(
                "float32"
            ),

            top_k

        )


        results = []


        for score, index in zip(

            scores[0],

            indices[0]

        ):

            if (

                index != -1

                and index < len(self.chunks)

            ):

                chunk = self.chunks[index].copy()

                chunk["score"] = float(
                    score
                )

                results.append(chunk)


        return results