"""Test score determinism and consistency across multiple runs for the RAG pipeline."""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from resume_analyzer import extract_text_from_pdf, analyze_resume_rag

def test_rag_consistency():
    pdf_path = os.path.join(current_dir, "sample_resume.pdf")
    if not os.path.exists(pdf_path):
        from test_setup import create_sample_pdf
        create_sample_pdf(pdf_path)
        
    resume_text = extract_text_from_pdf(pdf_path)
    job_desc = (
        "Looking for a Full Stack Python Developer with 3+ years experience. "
        "Must have strong skills in Python, Django, PostgreSQL, and Docker containerization. "
        "Experience building high-traffic REST APIs is required."
    )

    print("--- Testing RAG Pipeline Determinism (3 runs with cache) ---")
    cached_scores = []
    for i in range(1, 4):
        res, v_idx, evidence = analyze_resume_rag(resume_text, job_desc, use_cache=True)
        score = res["match_score"]
        cached_scores.append(score)
        print(f"Run {i}: Match Score = {score} | Evidence Chunks Retrieved = {len(evidence)}")

    assert len(set(cached_scores)) == 1, f"Scores fluctuated! Got: {cached_scores}"
    print(f"SUCCESS: RAG pipeline is 100% deterministic! Score = {cached_scores[0]}")

if __name__ == "__main__":
    test_rag_consistency()
