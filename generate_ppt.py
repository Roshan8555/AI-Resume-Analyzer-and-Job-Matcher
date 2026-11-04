"""Generate a professional PowerPoint presentation for the AI Resume Analyzer project."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def create_presentation(output_path: str):
    prs = Presentation()
    
    # 4:3 Aspect Ratio (10 x 7.5 inches)
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    PRIMARY_COLOR = RGBColor(24, 43, 73)      # Deep Navy
    SECONDARY_COLOR = RGBColor(41, 128, 185)  # Professional Blue
    DARK_TEXT = RGBColor(33, 37, 41)         # Off Black
    MUTED_TEXT = RGBColor(108, 117, 125)     # Cool Gray
    
    blank_slide_layout = prs.slide_layouts[6]
    
    def add_header(slide, title_text, category_text="AI RESUME ANALYZER & JOB MATCHER"):
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(8.4), Inches(1.1))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SECONDARY_COLOR
        p_cat.space_after = Pt(4)
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY_COLOR
        
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(1.75), Inches(8.4), Inches(0.03)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = SECONDARY_COLOR
        line.line.color.rgb = SECONDARY_COLOR

    # ==================== SLIDE 1: Title Slide ====================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(8.0), Inches(2.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "AI RESUME ANALYZER &\nJOB MATCHER"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = PRIMARY_COLOR
    p1.space_after = Pt(16)
    
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "An LLM-Powered Career Assistant using Prompt Engineering, Groq & Streamlit"
    p1_sub.alignment = PP_ALIGN.CENTER
    p1_sub.font.size = Pt(16)
    p1_sub.font.color.rgb = SECONDARY_COLOR
    
    author_box = slide1.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(8.0), Inches(1.0))
    tf_author = author_box.text_frame
    p_auth = tf_author.paragraphs[0]
    p_auth.text = "Submitted by: Roshan Kumar"
    p_auth.alignment = PP_ALIGN.CENTER
    p_auth.font.size = Pt(18)
    p_auth.font.color.rgb = MUTED_TEXT

    # ==================== SLIDE 2: Project Introduction ====================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "Project Introduction")
    body2 = slide2.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf2 = body2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "• AI Resume Analyzer and Job Matcher is a lightweight, high-performance web application designed to evaluate candidate resumes against target job descriptions using LLMs."
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(14)
    
    p = tf2.add_paragraph()
    p.text = "• The system delivers complete candidate evaluation:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(8)
    
    features = [
        "Automated PDF resume text extraction via PyMuPDF (fitz)",
        "Prompt-engineered semantic analysis against job specifications",
        "Deterministic, consistent match scoring (0 to 100)",
        "Categorization of matched technical & domain skills",
        "Identification of missing qualifications and requirement gaps",
        "ATS (Applicant Tracking System) keyword alignment analysis",
        "Grounded resume bullet point rewrites (Before vs. After)",
        "Strategic career recommendations and exportable reports"
    ]
    for feat in features:
        p = tf2.add_paragraph()
        p.text = f"   • {feat}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 3: Technologies & Architecture ====================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "Technologies & Architecture")
    body3 = slide3.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf3 = body3.text_frame
    tf3.word_wrap = True
    
    p = tf3.paragraphs[0]
    p.text = "• Built without RAG, embeddings, or vector databases for speed, simplicity, and reliability:"
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(12)
    
    tech_stack = [
        ("Python 3.12", "Core application logic, file parsing, and API orchestration"),
        ("Streamlit", "Clean, user-centric web dashboard with zero configuration clutter"),
        ("Groq API", "High-speed inference platform running our single best model"),
        ("openai/gpt-oss-120b", "Single top-tier 120B parameter model optimized for reasoning & JSON mode"),
        ("PyMuPDF (fitz)", "In-memory document parsing for multi-page PDF resumes"),
        ("Prompt Engineering", "System instructions, domain guardrails, and anti-hallucination rules"),
        ("python-dotenv", "Secure backend credential management keeping API keys off the UI")
    ]
    for tech, desc in tech_stack:
        p = tf3.add_paragraph()
        p.text = f"• {tech}: {desc}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # ==================== SLIDE 4: Resume Ingestion & PDF Extraction ====================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "Resume Ingestion & PDF Extraction")
    body4 = slide4.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf4 = body4.text_frame
    tf4.word_wrap = True
    
    p = tf4.paragraphs[0]
    p.text = "• PyMuPDF (fitz) Integration:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points4_1 = [
        "Lightweight C-based extraction library with minimal memory overhead.",
        "Processes multi-page PDF documents and extracts clean plain text.",
        "Preserves logical section ordering, headers, and bullet structures.",
        "Operates directly on in-memory byte buffers from Streamlit's file uploader."
    ]
    for pt in points4_1:
        p = tf4.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf4.add_paragraph()
    p.text = "• Flexible Input Handling:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    points4_2 = [
        "Dual input modes: direct PDF file upload OR manual text paste.",
        "Input sanitization: strips extra whitespace and normalizes character encoding.",
        "Protects against untrusted input: treats extracted text strictly as inert data."
    ]
    for pt in points4_2:
        p = tf4.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 5: Prompt Engineering & Schema Design ====================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "Prompt Engineering & Schema Design")
    body5 = slide5.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf5 = body5.text_frame
    tf5.word_wrap = True
    
    p = tf5.paragraphs[0]
    p.text = "• SYSTEM_PROMPT Core Principles:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points5_1 = [
        "Role Definition: 'Expert resume analyst and career assistant'.",
        "Strict Grounding: Never invent skills, metrics, or candidate achievements.",
        "Evidence Distinction: Differentiates missing evidence from confirmed lack of skill.",
        "Defensive Prompting: Explicitly ignores any instructions embedded inside documents."
    ]
    for pt in points5_1:
        p = tf5.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf5.add_paragraph()
    p.text = "• Enforced JSON Schema Structure:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    schema_fields = [
        "match_score: Integer (0-100) estimated match",
        "matched_skills & missing_skills: Arrays of categorized skill names",
        "matched_keywords & missing_keywords: Arrays of ATS keyword matches",
        "bullet_improvements: Array of {before, after, reason} objects",
        "recommendations: Array of high-impact strategic suggestions"
    ]
    for sf in schema_fields:
        p = tf5.add_paragraph()
        p.text = f"   • {sf}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 6: End-to-End Processing Workflow ====================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "End-to-End Processing Workflow")
    body6 = slide6.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf6 = body6.text_frame
    tf6.word_wrap = True
    
    p = tf6.paragraphs[0]
    p.text = "• Analysis Pipeline Sequence:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(8)
    
    steps = [
        "1. Ingestion: Candidate uploads resume PDF and pastes Job Description.",
        "2. Text Extraction: PyMuPDF parses document stream into structured text.",
        "3. Context Preparation: System combines SYSTEM_PROMPT with User Documents.",
        "4. Groq Inference: Sends request to openai/gpt-oss-120b with temperature 0.0 & seed 42.",
        "5. Persistent Caching: Saves SHA-256 hash to disk for 100% deterministic repeat runs.",
        "6. Dashboard Rendering: Displays metric cards, badges, and comparison boxes.",
        "7. Report Export: Enables instant download of Markdown and JSON reports."
    ]
    for step in steps:
        p = tf6.add_paragraph()
        p.text = f"• {step}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # ==================== SLIDE 7: Match Scoring & Skill Gap Analysis ====================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide7, "Match Scoring & Deterministic Anchoring")
    body7 = slide7.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf7 = body7.text_frame
    tf7.word_wrap = True
    
    p = tf7.paragraphs[0]
    p.text = "• Deterministic Match Score (0 - 100):"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    score_tiers = [
        "Score Stability: Anchored to verified skills (55%), keywords (25%), and qualitative depth (20%).",
        "Deterministic Guarantee: Greedy decoding (temperature 0.0) + persistent hashing prevents score drift.",
        "Standard Tiers: >=80 Strong Match, 55-79 Moderate Match, <55 Low Match."
    ]
    for tier in score_tiers:
        p = tf7.add_paragraph()
        p.text = f"   • {tier}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf7.add_paragraph()
    p.text = "• Qualitative Skills & ATS Keywords:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    qual_points = [
        "Matched Skills: Verified competencies found in both resume and JD.",
        "Missing Skills: Priority technologies or qualifications needed for the role.",
        "ATS Keywords: Scans for exact industry phrasing used by automated filters.",
        "Visual badges allow candidates to spot alignment gaps in seconds."
    ]
    for qp in qual_points:
        p = tf7.add_paragraph()
        p.text = f"   • {qp}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 8: Bullet Point Optimization ====================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide8, "Bullet Point Optimization (Before vs. After)")
    body8 = slide8.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf8 = body8.text_frame
    tf8.word_wrap = True
    
    p = tf8.paragraphs[0]
    p.text = "• Intelligent Resume Rewriting Studio:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points8 = [
        "Selects up to three bullet points that have high improvement potential.",
        "Transforms passive responsibility phrasing into active, impact-oriented statements.",
        "Strictly grounded: Reframes existing accomplishments without hallucinating facts.",
        "Incorporates target job keywords naturally into candidate experience.",
        "Provides a clear rationale explaining why each modification increases appeal."
    ]
    for pt in points8:
        p = tf8.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)
        
    p = tf8.add_paragraph()
    p.text = "• Strategic Career Recommendations:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(8)
    p.space_after = Pt(6)
    
    p = tf8.add_paragraph()
    p.text = "• Delivers actionable advice on portfolio additions, certifications, and phrasing improvements."
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 9: Streamlit Interface & Error Handling ====================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide9, "Streamlined Interface & Defensive Design")
    body9 = slide9.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf9 = body9.text_frame
    tf9.word_wrap = True
    
    p = tf9.paragraphs[0]
    p.text = "• Clean, Distraction-Free UI:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    ui_points = [
        "Zero UI Clutter: No API key inputs or model dropdowns on the frontend.",
        "Secure Configuration: Backend handles credentials via environment variables (.env).",
        "Focused Two-Column Layout: Resume upload/paste alongside Job Description.",
        "Session State Retention: Preserves analysis results across page interactions."
    ]
    for uip in ui_points:
        p = tf9.add_paragraph()
        p.text = f"   • {uip}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf9.add_paragraph()
    p.text = "• Defensive Error Handling & Resilience:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    err_points = [
        "Proactive Key Validation: Alerts user if GROQ_API_KEY is missing from .env.",
        "Catches corrupted or unreadable PDF files during PyMuPDF parsing.",
        "Default key seeding ensures UI never crashes if optional JSON keys are omitted.",
        "Clear in-app feedback alerts for network timeouts or API limits."
    ]
    for ep in err_points:
        p = tf9.add_paragraph()
        p.text = f"   • {ep}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 10: Conclusion & Key Takeaways ====================
    slide10 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide10, "Conclusion & Key Takeaways")
    body10 = slide10.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf10 = body10.text_frame
    tf10.word_wrap = True
    
    p = tf10.paragraphs[0]
    p.text = "• Project Summary:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    p = tf10.add_paragraph()
    p.text = "• The AI Resume Analyzer demonstrates how prompt engineering and modern LLM APIs solve real-world career workflow challenges with zero heavy infrastructure."
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(10)
    
    p = tf10.add_paragraph()
    p.text = "• Key Project Achievements:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    takeaways = [
        "Deterministic & Repeatable: Identical scores guaranteed via hashing and greedy decoding.",
        "Anti-Hallucination Guardrails: Safe, grounded bullet rewrites without fabricated claims.",
        "Ultra-Fast Inference: Sub-second response times using Groq API acceleration.",
        "Clean Separation of Concerns: Secure backend (.env), lean logic, and distraction-free UI.",
        "Instant Usability: Downloadable reports (Markdown & JSON) and responsive web interface."
    ]
    for ta in takeaways:
        p = tf10.add_paragraph()
        p.text = f"   • {ta}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")


if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI_Resume_Analyzer_Presentation.pptx")
    create_presentation(out_file)
