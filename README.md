# 🔍 RAG-Powered AI Resume Analyzer and Job Matcher

An enterprise-grade **Retrieval-Augmented Generation (RAG)** application that semantically indexes resume documents into a **ChromaDB Vector Database**, performs **Multi-Query Semantic Vector Retrieval**, and uses **Groq LLM** with structured prompt engineering to evaluate candidate fit, identify skill gaps, and rewrite bullet points with grounded evidence citations.

---

## 🌟 Overview

The **RAG AI Resume Analyzer and Job Matcher** transforms static resume evaluation into an intelligent, vector-backed knowledge retrieval system. Instead of merely feeding raw text to an LLM, the application:
1. Chunks multi-page PDF resumes into semantic, section-aware document units.
2. Embeds and stores chunks in a local **ChromaDB Vector Database** using dense embeddings (`all-MiniLM-L6-v2`, 384-dimensional cosine space).
3. Breaks down target Job Descriptions into multi-dimensional requirement queries (Technical Skills, Past Experience, Specialized Tools/Databases, Domain Qualifications).
4. Performs **Cosine Vector Search** to retrieve the most relevant evidence chunks with similarity confidence scores.
5. Injects the retrieved evidence as **Augmented Context** into Groq's high-speed inference engine (`openai/gpt-oss-120b`) in deterministic JSON mode.
6. Presents an interactive **RAG Knowledge Base & Retrieval Inspector** allowing users and recruiters to visually inspect retrieved evidence or perform semantic queries directly against the candidate's vector store.

---

## 🏗️ System Architecture (RAG Pipeline)

```
                       +---------------------------------------+
                       |           Candidate Resume            |
                       |       (PDF Upload or Raw Text)        |
                       +-------------------+-------------------+
                                           |
                                           v
                             [ PyMuPDF Text Extractor ]
                                           |
                                           v
                           [ Section-Aware Text Chunking ]
                        (Summary, Experience, Skills, Projects)
                                           |
                                           v
                       +---------------------------------------+
                       |       ChromaDB Vector Database        |
                       |  - Model: all-MiniLM-L6-v2 (384d)     |
                       |  - Metric: Cosine Similarity          |
                       +-------------------+-------------------+
                                           |
    +-----------------------------+        |
    |   Target Job Description    |        |
    +--------------+--------------+        |
                   |                       |
                   v                       |
   [ Multi-Query Decomposition ]           |
   - Technical Stack Requirements          |
   - Experience & Seniority Depth          |
   - ATS Keywords & Tooling                |
                   |                       |
                   +-----------> [ Semantic Vector Search ] <-----------+
                                (Top-K KNN Cosine Retrieval)
                                           |
                                           v
                             +---------------------------+
                             | Retrieved Evidence Chunks |
                             | (with Similarity Scores)  |
                             +-------------+-------------+
                                           |
                                           v
                             +---------------------------+
                             | Augmented Prompt Synthesis|
                             |  - System Prompt          |
                             |  - Retrieved Evidence     |
                             |  - Job Requirements       |
                             +-------------+-------------+
                                           |
                                           v
                             +---------------------------+
                             |    Groq LLM Inference     |
                             |  - openai/gpt-oss-120b    |
                             |  - Temperature: 0.0       |
                             |  - JSON Mode              |
                             +-------------+-------------+
                                           |
                                           v
                             +---------------------------+
                             |   Evaluation Dashboard    |
                             |  - Grounded Match Score   |
                             |  - Verified Skill Badges  |
                             |  - RAG Vector Inspector   |
                             |  - Interactive Resume QA  |
                             |  - Before/After Rewrites  |
                             +---------------------------+
```

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Vector Database** | **ChromaDB** | High-performance in-memory vector store indexing chunk embeddings |
| **Embedding Model** | **`all-MiniLM-L6-v2`** | 384-dimensional dense semantic sentence embeddings (ONNX runtime) |
| **LLM Inference** | **Groq API** | Sub-second inference engine hosting open-source LLMs |
| **LLM Model** | **`openai/gpt-oss-120b`** | 120B parameter model optimized for complex reasoning & JSON output |
| **Document Parsing** | **PyMuPDF (`fitz`)** | Fast in-memory parsing for multi-page PDF documents |
| **Application UI** | **Streamlit** | Modern, reactive dashboard with interactive RAG vector search |
| **Environment** | **python-dotenv** | Secure local environment credential management |

---

## 🚀 Key Features

### 1. Multi-Query Semantic Vector Retrieval
The Job Description is decomposed into distinct analytical queries:
- **Core Skills**: Evaluates programming languages and primary frameworks.
- **Experience Alignment**: Retrieves project duties and workplace contributions.
- **Tools & Infrastructure**: Scans for databases, CI/CD, and cloud platforms.
- **Domain & Education**: Checks degree qualifications and domain certifications.

### 2. Grounded, Deterministic Scoring
- Greedy decoding (`temperature=0.0`) and fixed seed (`seed=42`).
- Score is calculated mathematically based on retrieved evidence:
  - **55%** Verified Skills Evidence.
  - **25%** ATS Keywords Coverage.
  - **20%** Qualitative Experience Alignment.
- Persistent SHA-256 disk caching guarantees that the same resume and job description always produce the exact same score.

### 3. Interactive RAG Vector Inspector & Resume QA
- **Evidence Cards**: Inspect the exact chunks retrieved from the vector store with their cosine similarity percentages.
- **Query Your Resume**: A built-in search tool allowing recruiters or candidates to run semantic vector queries against the candidate's resume (e.g. *"Show experience with Docker containerization"*).

### 4. Fact-Grounded Bullet Rewriting (Before vs. After)
- Rewrites up to 3 resume bullet points to emphasize quantifiable impact, action verbs, and target keywords.
- Strictly grounded in the retrieved resume context—the model is forbidden from inventing unverified claims.

### 5. Instant Report Export
- Download comprehensive evaluation reports in **Markdown (`.md`)** or structured **JSON (`.json`)** format.

---

## 📁 Project Structure

```
ai_resume_analyzer/
├── app.py                             # Streamlit web interface & RAG Inspector
├── rag_engine.py                      # ChromaDB vector store, chunking & semantic search
├── resume_analyzer.py                 # RAG orchestration, caching, & Groq LLM API caller
├── prompt.py                          # RAG system prompt & JSON schema constraints
├── requirements.txt                   # Project dependencies (ChromaDB, Groq, PyMuPDF, etc.)
├── .env                               # Local secrets (GROQ_API_KEY, GROQ_MODEL) - Ignored by Git
├── .env.example                       # Configuration template
├── .gitignore                         # Protects .env, caches, and bytecode
├── sample_resume.pdf                  # Sample resume for verification
├── test_setup.py                      # Automated test script for vector indexing & PDF extraction
├── test_score_consistency.py          # Determinism and consistency test script
├── generate_ppt.py                    # PowerPoint presentation generator
└── AI_Resume_Analyzer_Presentation.pptx # 10-slide PowerPoint presentation
```

---

## 🏁 Setup & Installation Guide

### Prerequisites
- **Python 3.10+** (Tested on Python 3.12)
- A free **Groq API Key** from [console.groq.com](https://console.groq.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/Roshan8555/AI-Resume-Analyzer-and-Job-Matcher.git
cd AI-Resume-Analyzer-and-Job-Matcher
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 4. Run Automated RAG Verification
```bash
python test_setup.py
```
*Expected Output: ChromaDB Indexing Test PASSED! ChromaDB Vector Retrieval Test PASSED!*

### 5. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 💡 How to Use the Application

1. **Upload Resume**: Upload your resume PDF or paste the text directly.
2. **Paste Job Description**: Paste target job requirements and responsibilities.
3. **Click "🚀 Run RAG Analysis"**:
   - The app chunks and indexes your resume into ChromaDB.
   - It performs semantic vector retrieval to gather grounded evidence.
   - Groq LLM evaluates alignment and generates bullet rewrites.
4. **Explore the RAG Inspector**:
   - View the retrieved chunks and cosine similarity scores.
   - Use the **Interactive Vector Search** bar to ask questions about your resume.
5. **Download Report**: Export your customized report in Markdown or JSON format.

---

## 🛡️ License

Built as an open-source reference implementation of Retrieval-Augmented Generation (RAG) for document intelligence and career tech workflows.
