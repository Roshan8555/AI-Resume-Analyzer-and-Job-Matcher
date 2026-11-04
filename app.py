"""Streamlit Web Application for AI Resume Analyzer and Job Matcher."""

import os
import json
import streamlit as st
from dotenv import load_dotenv

from resume_analyzer import extract_text_from_pdf, analyze_resume

# Load environment variables from .env
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling, badges, and comparison cards
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 16px;
        margin: 4px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .badge-matched {
        background-color: #e6f4ea;
        color: #137333;
        border: 1px solid #ceead6;
    }
    .badge-missing {
        background-color: #fce8e6;
        color: #c5221f;
        border: 1px solid #fad2cf;
    }
    /* Bullet Improvement Boxes */
    .bullet-box {
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .bullet-before {
        background-color: #fff9e6;
        border-left: 5px solid #fbc02d;
    }
    .bullet-after {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- MAIN HEADER -----------------
st.title("📄 AI Resume Analyzer and Job Matcher")
st.markdown(
    "Evaluate candidate resumes against any job description using Prompt Engineering and LLM API. "
    "Get an instant match score, skill gap identification, ATS keyword alignment, and grounded bullet point rewrites."
)
st.markdown("---")

# Session state initialization for analysis results
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

# ----------------- INPUT SECTION -----------------
col_input1, col_input2 = st.columns(2)

with col_input1:
    st.subheader("1. Resume")
    resume_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        help="Upload a PDF resume to automatically extract text.",
        key="pdf_uploader"
    )
    
    with st.expander("Or paste resume text directly", expanded=(resume_file is None)):
        manual_resume_text = st.text_area(
            "Resume Plain Text",
            height=200,
            placeholder="Paste your resume content here if you don't have a PDF file...",
            key="resume_text_area"
        )

with col_input2:
    st.subheader("2. Target Job Description")
    job_description = st.text_area(
        "Job Description & Requirements",
        height=280,
        placeholder="Paste the target job description, key responsibilities, and required qualifications here...",
        key="jd_text_area"
    )

# ----------------- ACTION BUTTON -----------------
st.markdown("---")
analyze_btn = st.button("🚀 Analyze Resume Fit", type="primary", use_container_width=True)

if analyze_btn:
    # Check API key in environment
    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "⚠️ **API Key Missing**: `GROQ_API_KEY` is not configured in your `.env` file. "
            "Please add `GROQ_API_KEY=your_key_here` to the `.env` file in the project folder to run analysis."
        )
    else:
        # Resolve resume text source
        resume_text_to_process = ""
        if resume_file is not None:
            try:
                with st.spinner("📄 Extracting text from uploaded PDF..."):
                    resume_text_to_process = extract_text_from_pdf(resume_file)
            except Exception as e:
                st.error(f"Failed to read PDF file: {e}")
        elif manual_resume_text.strip():
            resume_text_to_process = manual_resume_text.strip()

        # Validate inputs
        if not resume_text_to_process:
            st.warning("⚠️ Please upload a resume PDF or paste resume text.")
        elif not job_description.strip():
            st.warning("⚠️ Please provide the target job description.")
        else:
            try:
                with st.spinner("🤖 Analyzing alignment with LLM..."):
                    result = analyze_resume(
                        resume_text=resume_text_to_process,
                        job_description=job_description.strip()
                    )
                    st.session_state["analysis_result"] = result
                st.success("Analysis complete!")
            except Exception as err:
                st.error(f"Error during analysis: {err}")

# ----------------- RESULTS DASHBOARD -----------------
analysis = st.session_state.get("analysis_result")

if analysis:
    st.markdown("## 📊 Analysis Dashboard")
    
    score = int(analysis.get("match_score", 0))
    
    # 1. Match Score Card
    score_col, status_col = st.columns([1, 2])
    with score_col:
        st.metric(label="Overall Match Score", value=f"{score} / 100")
        st.progress(score / 100.0)
    
    with status_col:
        if score >= 80:
            st.success("🌟 **Strong Match**: The candidate profile closely aligns with the core requirements of this role.")
        elif score >= 55:
            st.info("⚖️ **Moderate Match**: Transferable skills are present, but important requirements or keywords are missing.")
        else:
            st.warning("⚠️ **Low Match**: Significant skill gaps or missing critical qualifications detected.")

    st.markdown("---")

    # 2. Skills Comparison
    st.subheader("🛠️ Skills Comparison")
    skills_col1, skills_col2 = st.columns(2)
    
    with skills_col1:
        st.markdown("#### ✅ Matched Skills")
        matched_skills = analysis.get("matched_skills", [])
        if matched_skills:
            badges_html = " ".join([f'<span class="skill-badge badge-matched">✓ {skill}</span>' for skill in matched_skills])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.write("No direct skill matches identified.")

    with skills_col2:
        st.markdown("#### ❌ Missing / Unverified Skills")
        missing_skills = analysis.get("missing_skills", [])
        if missing_skills:
            badges_html = " ".join([f'<span class="skill-badge badge-missing">✗ {skill}</span>' for skill in missing_skills])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.write("No critical missing skills identified.")

    st.markdown("---")

    # 3. ATS Keywords Comparison
    st.subheader("🔍 ATS Keywords Analysis")
    kw_col1, kw_col2 = st.columns(2)
    
    with kw_col1:
        st.markdown("#### 🎯 Matched Keywords")
        matched_kw = analysis.get("matched_keywords", [])
        if matched_kw:
            badges_html = " ".join([f'<span class="skill-badge badge-matched">{kw}</span>' for kw in matched_kw])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.write("None detected.")

    with kw_col2:
        st.markdown("#### 📌 Missing Target Keywords")
        missing_kw = analysis.get("missing_keywords", [])
        if missing_kw:
            badges_html = " ".join([f'<span class="skill-badge badge-missing">{kw}</span>' for kw in missing_kw])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.write("All key terms present.")

    st.markdown("---")

    # 4. Bullet Point Improvements
    st.subheader("✍️ Bullet Point Improvements (Before vs. After)")
    st.caption("Rewritten to emphasize quantifiable impact, active verbs, and target keywords based strictly on original facts.")
    
    bullet_improvements = analysis.get("bullet_improvements", [])
    if bullet_improvements:
        for idx, item in enumerate(bullet_improvements, 1):
            with st.expander(f"Bullet Improvement #{idx}", expanded=True):
                col_b, col_a = st.columns(2)
                with col_b:
                    st.markdown("**Original:**")
                    st.markdown(f'<div class="bullet-box bullet-before">{item.get("before", "")}</div>', unsafe_allow_html=True)
                with col_a:
                    st.markdown("**Improved Version:**")
                    st.markdown(f'<div class="bullet-box bullet-after">{item.get("after", "")}</div>', unsafe_allow_html=True)
                
                st.markdown(f"**💡 Rationale:** {item.get('reason', '')}")
    else:
        st.info("No bullet point rewrites generated.")

    st.markdown("---")

    # 5. Recommendations
    st.subheader("💡 Strategic Recommendations")
    recommendations = analysis.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            st.markdown(f"- {rec}")
    else:
        st.write("No specific recommendations provided.")

    st.markdown("---")

    # 6. Export / Download
    st.subheader("📥 Export Analysis Report")
    
    # Prepare Markdown Report
    md_report = f"""# AI Resume Analysis Report

## Overall Match Score: {score}/100

### Matched Skills
{', '.join(analysis.get('matched_skills', []))}

### Missing Skills
{', '.join(analysis.get('missing_skills', []))}

### Matched Keywords
{', '.join(analysis.get('matched_keywords', []))}

### Missing Keywords
{', '.join(analysis.get('missing_keywords', []))}

### Bullet Point Improvements
"""
    for idx, b in enumerate(bullet_improvements, 1):
        md_report += f"\n#### Improvement #{idx}\n- **Before:** {b.get('before')}\n- **After:** {b.get('after')}\n- **Why:** {b.get('reason')}\n"

    md_report += "\n### Recommendations\n"
    for r in recommendations:
        md_report += f"- {r}\n"

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            label="📄 Download Markdown Report",
            data=md_report,
            file_name="resume_analysis_report.md",
            mime="text/markdown",
            use_container_width=True
        )
    with dl_col2:
        st.download_button(
            label="💾 Download JSON Data",
            data=json.dumps(analysis, indent=2),
            file_name="resume_analysis_data.json",
            mime="application/json",
            use_container_width=True
        )
