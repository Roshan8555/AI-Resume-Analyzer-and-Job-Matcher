"""Verification script for testing PDF text extraction and code integrity."""

import os
import sys
try:
    import pymupdf as fitz
except ImportError:
    import fitz

from resume_analyzer import extract_text_from_pdf, analyze_resume
from prompt import SYSTEM_PROMPT


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
    
    # Insert text at top-left with basic formatting
    page.insert_text((50, 72), text, fontsize=11)
    doc.save(filepath)
    doc.close()
    print(f"Sample PDF created at: {filepath}")


def test_extraction(pdf_path: str):
    """Test text extraction from the sample PDF."""
    extracted = extract_text_from_pdf(pdf_path)
    print("\n--- Extracted Text Sample ---")
    print(extracted[:200] + "...")
    assert "Alex Morgan" in extracted, "Expected resume header in extracted text"
    assert "Python" in extracted, "Expected skill in extracted text"
    print("PDF Text Extraction Test PASSED!")


def test_prompt_integrity():
    """Verify system prompt is properly loaded."""
    assert "match_score" in SYSTEM_PROMPT
    assert "bullet_improvements" in SYSTEM_PROMPT
    print("Prompt Integrity Test PASSED!")


if __name__ == "__main__":
    sample_pdf_path = os.path.join(os.path.dirname(__file__), "sample_resume.pdf")
    create_sample_pdf(sample_pdf_path)
    test_extraction(sample_pdf_path)
    test_prompt_integrity()
    print("\nAll automated setup tests passed successfully!")
