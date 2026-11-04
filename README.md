# 📄 AI Resume Analyzer and Job Matcher

An AI-powered web application that analyzes resumes against target job descriptions using **Prompt Engineering** and the **Groq API**, built **without RAG, embeddings, or vector databases**.

---

## 🌟 Overview

The **AI Resume Analyzer and Job Matcher** is designed for job seekers and hiring professionals to quickly evaluate candidate-role alignment. By leveraging **PyMuPDF** for instant PDF text extraction, a fine-tuned **System Prompt** with strict anti-hallucination guardrails, and Groq's high-speed inference engine running **`openai/gpt-oss-120b`** in deterministic JSON mode, the app delivers comprehensive, actionable feedback in seconds.

### Key Capabilities
- 🎯 **Match Score (0–100)**: Objective scoring based on relevant job requirements.
- 🛠️ **Skill Gap Identification**: Side-by-side color-coded badges for **Matched Skills** vs. **Missing / Unverified Skills**.
- 🔍 **ATS Keyword Comparison**: Scans for exact industry terms and keywords needed to pass Applicant Tracking Systems.
- ✍️ **Bullet Point Improvements (Before vs. After)**: Rewrites up to 3 resume bullet points to emphasize quantifiable impact, action verbs, and target keywords—strictly grounded in original facts without hallucination.
- 💡 **Strategic Career Recommendations**: Tailored suggestions for certifications, portfolio additions, and phrasing tweaks.
- 📥 **One-Click Export**: Download the complete evaluation report as **Markdown (`.md`)** or **structured JSON (`.json`)**.

---

## 🏗️ How This Project Was Built

### 1. Architectural Philosophy: Why No RAG or Vector Database?
Many modern AI tutorials unnecessarily introduce Retrieval-Augmented Generation (RAG), chunking pipelines, embedding models, and vector databases (e.g., Pinecone, ChromaDB) for single-document comparison tasks. 

For resume analysis, both documents (the candidate's resume and the job description) comfortably fit within the large context window of modern LLMs (128k+ tokens). 
- **Zero Vector DB Overhead**: No embeddings to compute, index, or store.
- **Whole-Document Semantic Context**: The LLM evaluates the entire resume holistically rather than fragmented chunks.
- **Ultra-Fast Sub-Second Response Times**: Direct prompt-to-API inference via Groq's LPU acceleration.
- **Deterministic Structured JSON**: Direct schema enforcement ensures the UI renders reliably every single time.

### 2. Technology Stack

| Technology | Role | Purpose |
| :--- | :--- | :--- |
| **Python 3.12** | Core Language | Application logic, file parsing, and API orchestration |
| **Streamlit** | Frontend UI | Clean, reactive web interface with zero sidebar clutter |
| **Groq API** | LLM Inference | High-speed, low-latency API access to top open-source models |
| **`openai/gpt-oss-120b`** | LLM Model | Single best high-capacity model (120B parameters) hosted on Groq |
| **PyMuPDF (`fitz`)** | PDF Ingestion | In-memory text extraction from multi-page PDF documents |
| **python-dotenv** | Security | Secure environment configuration keeping API keys out of the frontend |

### 3. Clean Frontend / Secure Backend Separation
- **No API Key on UI**: The API key is securely loaded from `.env` in the backend. Users never have to enter credentials on the interface.
- **Single Best Model**: Instead of overwhelming users with model dropdowns or risking model deprecation errors, the application uses `openai/gpt-oss-120b`, optimized for nuanced semantic extraction and structured JSON compliance.
- **No Distracting Sample Buttons**: A clean, focused interface featuring dual input columns (Resume Upload/Paste + Job Description) and a primary action button.

---

## ⚙️ How This Project Works (Step-by-Step Pipeline)

```
+-----------------------------------+        +-----------------------------------+
|            Resume PDF             |        |          Job Description          |
|    (Uploaded via Streamlit)       |        |        (Pasted by the User)       |
+-----------------+-----------------+        +-----------------+-----------------+
                  |                                            |
                  v                                            |
      [ PyMuPDF Text Extraction ]                              |
                  |                                            |
                  +---------------------+----------------------+
                                        |
                                        v
                       +---------------------------------+
                       |    Prompt Engineering Engine    |
                       |  - System Role & Strict Grounding|
                       |  - JSON Schema Constraints      |
                       |  - Anti-Hallucination Rules     |
                       +----------------+----------------+
                                        |
                                        v
                       +---------------------------------+
                       |     Groq API (gpt-oss-120b)     |
                       |  - Temperature: 0.2 (low drift) |
                       |  - response_format: json_object |
                       +----------------+----------------+
                                        |
                                        v
                       +---------------------------------+
                       |     Structured JSON Response    |
                       |  - match_score                  |
                       |  - matched/missing skills       |
                       |  - matched/missing keywords     |
                       |  - bullet_improvements          |
                       |  - recommendations              |
                       +----------------+----------------+
                                        |
                                        v
                       +---------------------------------+
                       |      Streamlit Dashboard UI     |
                       |  - Score & Visual Progress Bar  |
                       |  - Color-Coded Skill Badges     |
                       |  - Before / After Bullet Cards  |
                       |  - Download Markdown & JSON     |
                       +---------------------------------+
```

### Step 1: Document Processing (`resume_analyzer.py`)
- Accepts PDF uploads as binary streams or file objects directly from Streamlit.
- PyMuPDF opens the in-memory stream and iterates over each page to extract clean, uncorrupted plain text while preserving headers and lists.
- Supports direct text pasting via an expandable section for maximum flexibility.

### Step 2: Prompt Engineering (`prompt.py`)
The system prompt enforces five critical guardrails:
1. **Strict Factual Grounding**: The LLM is explicitly forbidden from inventing skills, certifications, or past achievements.
2. **Missing Evidence vs. Lack of Skill**: Differentiates between skills explicitly missing vs. skills merely absent from the resume text.
3. **Structured Bullet Rewriting**: Bullet points are rewritten only using facts verifiable in the original resume, framed with strong action verbs and target metrics.
4. **Adversarial Defense**: Treats all input text as untrusted data to ignore any prompt injection attempts embedded within candidate resumes.
5. **JSON Schema Enforcement**: Guarantees output conforms to a strict dictionary format:
   ```json
   {
     "match_score": 85,
     "matched_skills": ["Python", "FastAPI", "Docker"],
     "missing_skills": ["Kubernetes", "AWS ECS"],
     "matched_keywords": ["REST APIs", "Microservices"],
     "missing_keywords": ["CI/CD Pipeline", "Redis"],
     "bullet_improvements": [
       {
         "before": "Built APIs using Python.",
         "after": "Architected high-throughput REST APIs using Python and FastAPI, reducing response latency by 20%.",
         "reason": "Incorporates target keywords and frames responsibilities into quantifiable impact."
       }
     ],
     "recommendations": ["Highlight cloud deployment experience prominently."]
   }
   ```

### Step 3: Groq LLM Inference
- Calls `client.chat.completions.create` with `model="openai/gpt-oss-120b"`.
- Sets `temperature=0.2` to eliminate hallucination and promote deterministic analytical accuracy.
- Enforces native JSON mode via `response_format={"type": "json_object"}`.

### Step 4: UI Rendering & Export (`app.py`)
- Parses the validated JSON object into dynamic Streamlit components.
- Renders green badges for matched competencies and red badges for missing requirements.
- Presents side-by-side expandable cards displaying **Before**, **After**, and the **Rationale** for each improved bullet.
- Generates downloadable Markdown and JSON files with a single click.

---

## 📁 Project Structure

```
ai_resume_analyzer/
├── app.py                 # Streamlit web application & interactive dashboard
├── resume_analyzer.py     # PDF text extraction & Groq API LLM caller
├── prompt.py              # System prompt, constraints, and JSON schema
├── requirements.txt       # Project dependencies
├── .env                   # API secrets (GROQ_API_KEY, GROQ_MODEL) - DO NOT COMMIT
├── .env.example           # Template for environment configuration
├── .gitignore             # Git ignore file protecting .env and cache
├── sample_resume.pdf      # Sample resume for quick verification
├── test_setup.py          # Automated verification script
└── README.md              # Project documentation
```

---

## 🚀 Setup & Installation Guide

### Prerequisites
- **Python 3.10+** (Tested on Python 3.12)
- A free **Groq API Key** from [console.groq.com](https://console.groq.com/)

### 1. Clone or Navigate to the Project
```bash
cd ai_resume_analyzer
```

### 2. (Optional) Create a Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

> **Security Note**: Never commit `.env` to Git. The `.gitignore` file is already set up to exclude it.

### 5. Run the Automated Test Suite
To confirm PDF extraction and prompt integrity:
```bash
python test_setup.py
```

### 6. Launch the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at:
👉 **`http://localhost:8501`**

---

## 💡 How to Use the Application

1. **Upload Resume**: Drag and drop your resume in PDF format (or paste the plain text directly).
2. **Paste Job Description**: Paste the target job posting (responsibilities, required qualifications).
3. **Click "🚀 Analyze Resume Fit"**: The app processes the resume and sends it to the Groq LLM.
4. **Review Results**:
   - Check your **Match Score**.
   - Review **Matched Skills** and **Missing Skills** to identify gaps.
   - Inspect **ATS Keywords** to align vocabulary.
   - Read the **Before vs. After Bullet Point Improvements** to see how to describe your experience with more impact.
5. **Download Report**: Click **"Download Markdown Report"** to save your personalized improvement plan.

---

## 🛡️ License & Contributing

Built as a lightweight, open-source reference project demonstrating effective Prompt Engineering, structured LLM outputs, and document analysis. Contributions and enhancements are welcome!
