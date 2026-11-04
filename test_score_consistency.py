"""Test score determinism and consistency across multiple runs."""

import os
import sys

# Ensure local module is found
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from resume_analyzer import extract_text_from_pdf, analyze_resume

def test_determinism():
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

    print("--- Testing API Determinism (Bypassing cache, 3 distinct API calls) ---")
    api_scores = []
    for i in range(1, 4):
        res = analyze_resume(resume_text, job_desc, use_cache=False)
        score = res["match_score"]
        api_scores.append(score)
        print(f"Run {i} (Direct API call): Match Score = {score}")

    assert len(set(api_scores)) == 1, f"API scores fluctuated! Got: {api_scores}"
    print(f"SUCCESS: Direct API calls are 100% deterministic! Score = {api_scores[0]}")

    print("\n--- Testing Cache Determinism (3 cached calls) ---")
    cached_scores = []
    for i in range(1, 4):
        res = analyze_resume(resume_text, job_desc, use_cache=True)
        score = res["match_score"]
        cached_scores.append(score)
        print(f"Run {i} (Cached call): Match Score = {score}")

    assert len(set(cached_scores)) == 1, f"Cached scores fluctuated! Got: {cached_scores}"
    assert cached_scores[0] == api_scores[0], "Cache score differs from API score!"
    print(f"SUCCESS: Cached calls are 100% identical! Score = {cached_scores[0]}")

    print("\nAll consistency tests passed successfully!")

if __name__ == "__main__":
    test_determinism()
