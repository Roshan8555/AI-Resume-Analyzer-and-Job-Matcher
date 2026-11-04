"""Core RAG analysis module: PDF text extraction, ChromaDB vector indexing, and Groq LLM integration."""

import os
import json
import hashlib
from typing import Any, Dict, Union, Tuple, List
from dotenv import load_dotenv

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # Fallback

from groq import Groq
from prompt import RAG_SYSTEM_PROMPT
from rag_engine import ResumeVectorIndex

# Locate and load .env from the project folder
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ENV_PATH = os.path.join(_CURRENT_DIR, ".env")
load_dotenv(dotenv_path=_ENV_PATH)

# Single best high-capacity model on Groq
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Persistent cache file
_CACHE_FILE = os.path.join(_CURRENT_DIR, ".analysis_cache.json")


def _load_persistent_cache() -> Dict[str, Dict[str, Any]]:
    """Load persistent disk cache of previous analyses."""
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_persistent_cache(cache: Dict[str, Dict[str, Any]]) -> None:
    """Save persistent disk cache safely."""
    try:
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def extract_text_from_pdf(pdf_input: Union[str, bytes, Any]) -> str:
    """Extract text from a PDF file path, raw bytes, or Streamlit UploadedFile.
    
    Args:
        pdf_input: File path (str), raw bytes (bytes), or file-like object with .read()
        
    Returns:
        Extracted text string from all PDF pages.
    """
    if isinstance(pdf_input, str):
        doc = fitz.open(pdf_input)
    elif isinstance(pdf_input, bytes):
        doc = fitz.open(stream=pdf_input, filetype="pdf")
    elif hasattr(pdf_input, "read"):
        content_bytes = pdf_input.read()
        if hasattr(pdf_input, "seek"):
            pdf_input.seek(0)
        doc = fitz.open(stream=content_bytes, filetype="pdf")
    else:
        raise ValueError("Unsupported PDF input type.")

    pages_text = []
    with doc:
        for page in doc:
            page_text = page.get_text()
            if page_text:
                pages_text.append(page_text.strip())

    return "\n\n".join(pages_text).strip()


def _compute_input_hash(resume_text: str, job_description: str, model: str) -> str:
    """Generate a SHA-256 hash for the normalized input texts and model."""
    normalized = f"{resume_text.strip()}|||{job_description.strip()}|||{model.strip()}".lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def calculate_deterministic_score(
    llm_raw_score: int,
    matched_skills: list,
    missing_skills: list,
    matched_keywords: list,
    missing_keywords: list
) -> int:
    """Compute a strictly deterministic, grounded match score based on retrieved evidence."""
    total_skills = len(matched_skills) + len(missing_skills)
    skill_ratio = len(matched_skills) / total_skills if total_skills > 0 else 1.0

    total_kw = len(matched_keywords) + len(missing_keywords)
    kw_ratio = len(matched_keywords) / total_kw if total_kw > 0 else 1.0

    bounded_raw = max(0, min(100, llm_raw_score))
    calculated = (skill_ratio * 55.0) + (kw_ratio * 25.0) + ((bounded_raw / 100.0) * 20.0)
    return max(0, min(100, int(round(calculated))))


def analyze_resume_rag(
    resume_text: str,
    job_description: str,
    model: str = DEFAULT_MODEL,
    use_cache: bool = True
) -> Tuple[Dict[str, Any], ResumeVectorIndex, List[Dict[str, Any]]]:
    """Execute the full RAG pipeline:
    
    1. Chunk resume and generate vector embeddings into ChromaDB.
    2. Multi-query semantic search to retrieve top relevant resume evidence.
    3. Synthesize Augmented Context for the LLM.
    4. Call Groq API with RAG_SYSTEM_PROMPT in JSON mode.
    5. Cache and return the structured evaluation alongside the vector index.
    
    Returns:
        (result_dict, vector_index_instance, retrieved_evidence_list)
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Please ensure your Groq API key is set in your .env file."
        )

    # 1. Build Vector Store Index in ChromaDB
    vector_index = ResumeVectorIndex()
    total_chunks = vector_index.index_resume(resume_text)

    # 2. Semantic Vector Retrieval across job dimensions
    augmented_context_str, retrieved_evidence = vector_index.retrieve_multiquery_context(job_description)

    # Check cache for identical input
    cache_key = _compute_input_hash(resume_text, job_description, model)
    cache = _load_persistent_cache()

    if use_cache and cache_key in cache:
        cached_result = cache[cache_key]
        cached_result["rag_meta"] = {
            "total_chunks_indexed": total_chunks,
            "retrieved_chunks_count": len(retrieved_evidence),
            "retrieved_evidence": retrieved_evidence
        }
        return cached_result, vector_index, retrieved_evidence

    # 3. Augment LLM prompt with retrieved vector evidence
    client = Groq(api_key=api_key)
    user_prompt = (
        f"RETRIEVED RESUME EVIDENCE (FROM VECTOR DATABASE):\n"
        f"{augmented_context_str}\n\n"
        f"FULL RESUME TEXT FOR REFERENCE:\n{resume_text}\n\n"
        f"TARGET JOB DESCRIPTION:\n{job_description}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        seed=42,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content
    result = json.loads(raw_content)

    matched_skills = result.get("matched_skills", [])
    missing_skills = result.get("missing_skills", [])
    matched_keywords = result.get("matched_keywords", [])
    missing_keywords = result.get("missing_keywords", [])
    raw_score = int(result.get("match_score", 0))

    final_score = calculate_deterministic_score(
        llm_raw_score=raw_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords
    )

    result["match_score"] = final_score
    result.setdefault("bullet_improvements", [])
    result.setdefault("recommendations", [])

    # Attach RAG metadata
    result["rag_meta"] = {
        "total_chunks_indexed": total_chunks,
        "retrieved_chunks_count": len(retrieved_evidence),
        "retrieved_evidence": retrieved_evidence
    }

    if use_cache:
        cache[cache_key] = result
        _save_persistent_cache(cache)

    return result, vector_index, retrieved_evidence


# Backward-compatible alias
def analyze_resume(resume_text: str, job_description: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    res, _, _ = analyze_resume_rag(resume_text, job_description, model=model)
    return res
