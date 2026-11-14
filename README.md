# 🧠 Knowlix AI – AI-Powered Document Intelligence Platform

**Turn Your Documents Into Knowledge.**

## 🌐 Live Demo

**Try Knowlix AI here:**

[🚀 Launch Knowlix AI](https://knowlix-ai-o7xk6wv5lpxtrocemn4oaf.streamlit.app/)

Explore the live application to upload documents, ask questions, and experience AI-powered document search.
---

## 🚀 Features

- **Multi-Format Document Upload:** Upload PDF, DOCX, and TXT files.
- **Document Processing:** Extract text from uploaded documents.
- **Semantic Search:** Find relevant document content using Sentence Transformers.
- **Vector Database:** Store and search document embeddings using FAISS.
- **AI-Powered Question Answering:** Generate contextual responses using Groq LLM.
- **Intelligent Question Routing:** Automatically classify questions into DOCUMENT, WEB, and GENERAL categories.
- **Web Search Integration:** Retrieve current information using Tavily Search API.
- **Conversation History:** Maintain chat history during the application session.
- **Source Identification:** Identify whether answers originate from documents, web search, or general knowledge.
- **Interactive Interface:** User-friendly application built using Streamlit.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Frontend and user interface |
| Groq API | Large Language Model integration |
| OpenAI GPT-OSS-20B | Default LLM model through Groq |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Tavily API | Web search integration |
| PyPDF | PDF text extraction |
| Python-docx | Word document processing |
| Python-dotenv | Environment variable management |

---

## 🏗️ System Architecture

The application follows a Retrieval-Augmented Generation (RAG) architecture combined with AI-based question routing.

```text
                 USER
                   |
                   v
             STREAMLIT UI
                   |
                   v
             USER QUESTION
                   |
                   v
             AI QUESTION ROUTER
                   |
          +--------+--------+
          |        |        |
          v        v        v
       DOCUMENT   WEB    GENERAL
          |        |        |
          v        v        |
       FAISS     TAVILY     |
       SEARCH    SEARCH     |
          |        |        |
          v        v        |
      DOCUMENT   WEB        |
      CONTEXT    CONTEXT    |
          |        |        |
          +--------+--------+
                   |
                   v
              GROQ LLM
                   |
                   v
             GENERATED ANSWER
                   |
                   v
              STREAMLIT UI
```

### How RAG works

1. The user uploads a document.
2. The document processor extracts its text.
3. The extracted text is divided into smaller chunks.
4. Sentence Transformers converts the chunks into numerical embeddings.
5. FAISS stores the embeddings for similarity search.
6. When the user asks a question, the system converts it into an embedding.
7. FAISS retrieves the most relevant document chunks.
8. Groq uses the retrieved context to generate an answer.

---

## 📂 Project Structure

```text
Knowlix-AI/
│
├── streamlit_app.py
│   └── Main Streamlit application and user interface
│
├── chatbot_engine.py
│   └── Generates AI responses using Groq LLM
│
├── router.py
│   └── Routes questions to DOCUMENT, WEB, or GENERAL
│
├── rag.py
│   └── Handles text chunking, embeddings, and FAISS search
│
├── document_processor.py
│   └── Extracts text from PDF, DOCX, and TXT files
│
├── web_search.py
│   └── Integrates Tavily web search
│
├── requirements.txt
│   └── Python project dependencies
│
├── .env
│   └── API keys and environment configuration
│
├── .gitignore
│   └── Files excluded from Git tracking
│
└── README.md
    └── Project documentation
```

---

## ⚙️ Installation and Setup

Follow these steps to run Knowlix AI locally.

### 1. Clone the repository

Open your terminal and execute:

```bash
git clone https://github.com/YOUR_USERNAME/Knowlix-AI.git
```

Navigate to the project directory:

```bash
cd Knowlix-AI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate the environment.

**Windows CMD:**

```cmd
venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` in the root project directory.

Add your API credentials:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
TAVILY_API_KEY=your_tavily_api_key
```

**Get your API keys:**

- Groq API: https://console.groq.com/
- Tavily API: https://app.tavily.com/

Replace the placeholder values with your actual API keys.

**Important:** Never upload your `.env` file or expose your API keys on GitHub.

### 5. Run the application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

Alternatively, on Windows with Anaconda:

```cmd
"C:\ProgramData\anaconda3\python.exe" -m streamlit run streamlit_app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 📦 Dependencies

The project uses the following Python packages:

| Package | Description |
|---|---|
| streamlit | Web application framework |
| groq | Groq API client |
| python-dotenv | Environment variable management |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| sentence-transformers | Text embedding generation |
| faiss-cpu | Vector similarity search |
| tavily-python | Tavily search API client |

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 💡 Example Use Cases

**1. Document Question Answering**

Upload a PDF and ask:

"What are the main topics covered in this document?"

**2. Document Summarization**

Upload a report and ask:

"Summarize this document in simple language."

**3. General Knowledge Questions**

Ask:

"What is the difference between Artificial Intelligence and Machine Learning?"

**4. Web-Based Questions**

Ask:

"What are the latest developments in Python?"

The intelligent router determines which information source should handle the question.

---

## 🔐 Security and Configuration

- Store API keys in environment variables.
- Keep `.env` excluded from Git.
- Avoid committing credentials or private documents.
- Use appropriate API access controls.
- Configure production secrets through the deployment platform.

---

## ⚠️ Current Project Limitations

- FAISS index is currently stored in memory.
- Chat history is maintained within the Streamlit session.
- User authentication is not yet implemented.
- PostgreSQL integration and persistent document storage are not yet implemented.
- Scanned PDF OCR is not currently supported.

These are potential areas for future development.

---

## 🔮 Future Enhancements

- User Registration and Authentication
- PostgreSQL Database Integration
- Persistent Document Storage
- Persistent Chat History
- User-Specific Document Management
- Advanced RAG Pipeline
- OCR Support for Scanned Documents
- Improved Dashboard and Analytics
- Cloud Deployment
- Production-Level Security and Monitoring

---

## 👨‍💻 Author

**Knowlix AI**

An AI-powered document intelligence project developed using Python, Streamlit, Groq, FAISS, Sentence Transformers, and Tavily.

---

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

⭐ If you find this project interesting, consider giving the repository a star!
