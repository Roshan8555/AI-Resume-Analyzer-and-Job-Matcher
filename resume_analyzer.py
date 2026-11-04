"""Core analysis module: PDF text extraction, persistent caching, and Groq LLM integration."""

import os
import json
import hashlib
from typing import Any, Dict, Union
from dotenv import load_dotenv

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # Fallback

from groq import Groq
from prompt import SYSTEM_PROMPT

# Locate and load .env from the project folder
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ENV_PATH = os.path.join(_CURRENT_DIR, ".env")
load_dotenv(dotenv_path=_ENV_PATH)

# Single best high-capacity model on Groq
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Persistent cache directory
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
    """Compute a strictly deterministic, grounded match score.
    
    Combines skill coverage (55%), keyword coverage (25%), and LLM depth evaluation (20%)
    anchored to verified discrete items so identical profiles never fluctuate.
    """
    total_skills = len(matched_skills) + len(missing_skills)
    skill_ratio = len(matched_skills) / total_skills if total_skills > 0 else 1.0

    total_kw = len(matched_keywords) + len(missing_keywords)
    kw_ratio = len(matched_keywords) / total_kw if total_kw > 0 else 1.0

    # Ensure llm_raw_score is within bounds
    bounded_raw = max(0, min(100, llm_raw_score))

    # Deterministic weighted calculation:
    # 55% Skill alignment + 25% Keyword alignment + 20% LLM qualitative assessment
    calculated = (skill_ratio * 55.0) + (kw_ratio * 25.0) + ((bounded_raw / 100.0) * 20.0)
    return max(0, min(100, int(round(calculated))))


def analyze_resume(
    resume_text: str,
    job_description: str,
    model: str = DEFAULT_MODEL,
    use_cache: bool = True
) -> Dict[str, Any]:
    """Send resume and job description to Groq LLM with prompt engineering instructions.
    
    Guarantees deterministic scoring via:
    1. Persistent SHA-256 caching across application restarts.
    2. Greedy decoding (temperature=0.0) with fixed seed (42).
    3. Mathematical score anchoring based on verified skills and keywords.
    
    Args:
        resume_text: Plain text of the resume.
        job_description: Plain text of the target job description.
        model: Single best LLM model name (defaults to openai/gpt-oss-120b).
        use_cache: Whether to use persistent disk caching for identical inputs.
        
    Returns:
        Structured dictionary matching the required JSON schema.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Please ensure your Groq API key is set in your .env file."
        )

    cache_key = _compute_input_hash(resume_text, job_description, model)
    cache = _load_persistent_cache()

    if use_cache and cache_key in cache:
        return cache[cache_key]

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"RESUME:\n{resume_text}\n\n"
                    f"JOB DESCRIPTION:\n{job_description}"
                ),
            },
        ],
        temperature=0.0,
        seed=42,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content
    result = json.loads(raw_content)

    # Ensure all expected keys exist
    matched_skills = result.get("matched_skills", [])
    missing_skills = result.get("missing_skills", [])
    matched_keywords = result.get("matched_keywords", [])
    missing_keywords = result.get("missing_keywords", [])
    raw_score = int(result.get("match_score", 0))

    # Calculate deterministic anchored score
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

    # Save to persistent cache
    if use_cache:
        cache[cache_key] = result
        _save_persistent_cache(cache)

    return result
