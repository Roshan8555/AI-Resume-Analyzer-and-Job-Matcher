"""Verification script for testing PDF text extraction, RAG vector indexing, and prompt integrity."""

import os
import sys

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from resume_analyzer import extract_text_from_pdf
from rag_engine import ResumeVectorIndex
from prompt import RAG_SYSTEM_PROMPT


def create_sample_pdf(filepath: str):
    """Generate a sample resume PDF using PyMuPDF for testing."""
    doc = fitz.open()
    page = doc.new_page()
    
    text = (
        "Alex Morgan - Full Stack Python Developer\n\n"
        "Summary:\n"
        "Experienced software engineer with 5 years in Python, Django, and React.\n\n"
        "Experience:\n"
        "- Developed REST APIs with Django Rest Framework for high-traffic apps.\n"
        "- Optimized PostgreSQL queries resulting in a 25% speed improvement.\n"
        "- Deployed microservices using Docker and CI/CD pipelines.\n\n"
        "Skills:\n"
        "Python, Django, React, PostgreSQL, Docker, Git"
    )
    
    page.insert_text((50, 72), text, fontsize=11)
    doc.save(filepath)
    doc.close()
    print(f"Sample PDF created at: {filepath}")


def test_extraction(pdf_path: str):
    """Test text extraction from the sample PDF."""
    extracted = extract_text_from_pdf(pdf_path)
    assert "Alex Morgan" in extracted, "Expected resume header in extracted text"
    assert "Python" in extracted, "Expected skill in extracted text"
    print("PDF Text Extraction Test PASSED!")
    return extracted


def test_rag_vector_pipeline(resume_text: str):
    """Test ChromaDB chunking, vector embedding, and multi-query semantic retrieval."""
    v_index = ResumeVectorIndex()
    count = v_index.index_resume(resume_text)
    assert count > 0, "Vector index failed to create chunks!"
    print(f"ChromaDB Indexing Test PASSED! Indexed {count} chunks.")

    # Test retrieval
    matches = v_index.retrieve("Python and Django APIs", top_k=2)
    assert len(matches) > 0, "Vector search returned no results!"
    assert matches[0]["similarity"] > 0.0, "Similarity score is invalid!"
    print(f"ChromaDB Vector Retrieval Test PASSED! Top match similarity: {matches[0]['similarity']}")


def test_prompt_integrity():
    """Verify system prompt is properly loaded."""
    assert "match_score" in RAG_SYSTEM_PROMPT
    assert "bullet_improvements" in RAG_SYSTEM_PROMPT
    assert "Retrieval-Augmented Generation" in RAG_SYSTEM_PROMPT
    print("RAG Prompt Integrity Test PASSED!")


if __name__ == "__main__":
    sample_pdf_path = os.path.join(os.path.dirname(__file__), "sample_resume.pdf")
    create_sample_pdf(sample_pdf_path)
    text = test_extraction(sample_pdf_path)
    test_rag_vector_pipeline(text)
    test_prompt_integrity()
    print("\nAll automated RAG setup tests passed successfully!")
