"""Generate a professional PowerPoint presentation for the RAG AI Resume Analyzer project."""

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
    
    def add_header(slide, title_text, category_text="RAG-POWERED AI RESUME ANALYZER"):
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
    p1.text = "RAG-POWERED AI RESUME ANALYZER\n& JOB MATCHER"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = PRIMARY_COLOR
    p1.space_after = Pt(16)
    
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Retrieval-Augmented Generation using ChromaDB, Dense Embeddings, Groq & Streamlit"
    p1_sub.alignment = PP_ALIGN.CENTER
    p1_sub.font.size = Pt(15)
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
    add_header(slide2, "Project Introduction & RAG Overview")
    body2 = slide2.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf2 = body2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "• An enterprise-grade Retrieval-Augmented Generation (RAG) system engineered to evaluate candidate resumes against complex job specifications using semantic vector indexing."
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(14)
    
    p = tf2.add_paragraph()
    p.text = "• Core RAG Capabilities:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(8)
    
    features = [
        "In-memory ChromaDB vector database indexing resume chunks",
        "Dense vector embeddings via all-MiniLM-L6-v2 (384-dimensional cosine space)",
        "Multi-query semantic vector search decomposing job requirements",
        "Augmented prompt synthesis providing exact evidence citations",
        "Grounded match scoring anchored to verified vector evidence",
        "Fact-based resume bullet point optimization (Before vs. After)",
        "Interactive Vector Search bar (Query Your Resume) in Streamlit",
        "Downloadable reports with RAG metadata in Markdown and JSON"
    ]
    for feat in features:
        p = tf2.add_paragraph()
        p.text = f"   • {feat}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 3: Technologies & Architecture ====================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "Technologies & RAG Architecture")
    body3 = slide3.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf3 = body3.text_frame
    tf3.word_wrap = True
    
    p = tf3.paragraphs[0]
    p.text = "• A state-of-the-art modular RAG stack designed for accuracy and high-speed execution:"
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(12)
    
    tech_stack = [
        ("ChromaDB", "Vector Database: Manages chunk indexing, HNSW index, and cosine similarity"),
        ("all-MiniLM-L6-v2", "Embedding Engine: Generates 384-dimensional dense semantic vectors"),
        ("Groq API", "High-speed inference platform executing prompt-augmented LLM completions"),
        ("openai/gpt-oss-120b", "Single top-tier 120B parameter model optimized for reasoning & JSON mode"),
        ("PyMuPDF (fitz)", "Document parsing: In-memory text extraction from multi-page PDF resumes"),
        ("Streamlit", "User Interface: Modern dashboard with dedicated RAG Knowledge Base Inspector"),
        ("python-dotenv", "Security: Backend environment configuration keeping API keys protected")
    ]
    for tech, desc in tech_stack:
        p = tf3.add_paragraph()
        p.text = f"• {tech}: {desc}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # ==================== SLIDE 4: Document Ingestion & Chunking ====================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "Document Ingestion & Section Chunking")
    body4 = slide4.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf4 = body4.text_frame
    tf4.word_wrap = True
    
    p = tf4.paragraphs[0]
    p.text = "• PyMuPDF Document Extraction:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points4_1 = [
        "Lightweight C-based extraction parsing multi-page PDF files into raw text.",
        "Processes in-memory byte buffers from Streamlit without saving temporary files.",
        "Preserves original formatting, headers, and bullet structures."
    ]
    for pt in points4_1:
        p = tf4.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf4.add_paragraph()
    p.text = "• Section-Aware Semantic Chunking (rag_engine.py):"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    points4_2 = [
        "Identifies major resume sections (Summary, Experience, Skills, Projects, Education).",
        "Creates overlapping sliding-window chunks (350 chars with 50-char overlap).",
        "Enriches each chunk with metadata: chunk_id, section name, and character bounds."
    ]
    for pt in points4_2:
        p = tf4.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 5: ChromaDB Vector Indexing ====================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "Vector Indexing & ChromaDB Storage")
    body5 = slide5.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf5 = body5.text_frame
    tf5.word_wrap = True
    
    p = tf5.paragraphs[0]
    p.text = "• Dense Embeddings Pipeline:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points5_1 = [
        "Uses all-MiniLM-L6-v2 ONNX model running locally with zero latency.",
        "Encodes text chunks into 384-dimensional dense semantic vectors.",
        "Captures contextual nuances between technical competencies and candidate projects."
    ]
    for pt in points5_1:
        p = tf5.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf5.add_paragraph()
    p.text = "• ChromaDB In-Memory Collection Management:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    points5_2 = [
        "Dynamically creates isolated collections per uploaded resume.",
        "Builds HNSW (Hierarchical Navigable Small World) index for fast approximate search.",
        "Configured with Cosine Distance space for normalized semantic similarity."
    ]
    for pt in points5_2:
        p = tf5.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 6: Multi-Query Retrieval ====================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "Multi-Query Semantic Vector Retrieval")
    body6 = slide6.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf6 = body6.text_frame
    tf6.word_wrap = True
    
    p = tf6.paragraphs[0]
    p.text = "• Requirement Query Decomposition:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points6_1 = [
        "Query 1: Core technical skills, programming languages, and frameworks.",
        "Query 2: Work experience, professional responsibilities, and key projects.",
        "Query 3: Specialized tooling, databases, CI/CD, and cloud platforms.",
        "Query 4: Academic background, certifications, and domain qualifications."
    ]
    for pt in points6_1:
        p = tf6.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf6.add_paragraph()
    p.text = "• Augmented Context Generation:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    points6_2 = [
        "Retrieves top-K candidate chunks per query, deduplicating overlapping evidence.",
        "Calculates cosine similarity confidence percentages for each chunk.",
        "Injects evidence directly into LLM prompt with section headers and chunk citations."
    ]
    for pt in points6_2:
        p = tf6.add_paragraph()
        p.text = f"   • {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 7: Grounded Match Scoring ====================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide7, "Grounded Scoring & Deterministic Anchoring")
    body7 = slide7.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf7 = body7.text_frame
    tf7.word_wrap = True
    
    p = tf7.paragraphs[0]
    p.text = "• Deterministic Formula (0 - 100):"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    score_tiers = [
        "55% Verified Skills: Proportion of required skills with direct vector evidence.",
        "25% ATS Keywords: Percentage of target keywords present in retrieved chunks.",
        "20% Qualitative Alignment: LLM assessment of seniority and project depth.",
        "Persistent Caching: SHA-256 hash ensures identical inputs yield identical scores."
    ]
    for tier in score_tiers:
        p = tf7.add_paragraph()
        p.text = f"   • {tier}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf7.add_paragraph()
    p.text = "• Categorized Gap Analysis:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    qual_points = [
        "Matched Skills: Competencies verified with direct chunk citations.",
        "Missing Skills: Job requirements where no vector evidence exists in the resume.",
        "ATS Keywords: Keyword presence vs. absence for applicant tracking systems."
    ]
    for qp in qual_points:
        p = tf7.add_paragraph()
        p.text = f"   • {qp}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # ==================== SLIDE 8: Bullet Point Optimization ====================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide8, "Fact-Grounded Bullet Point Optimization")
    body8 = slide8.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf8 = body8.text_frame
    tf8.word_wrap = True
    
    p = tf8.paragraphs[0]
    p.text = "• RAG-Driven Resume Rewriting Studio:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    points8 = [
        "Identifies up to three bullet points with high improvement potential.",
        "Grounds rewrites strictly in the retrieved resume context—zero hallucinations.",
        "Converts passive responsibility phrasing into active, impact-oriented statements.",
        "Incorporates target job keywords naturally into candidate accomplishments.",
        "Provides clear analytical rationale explaining why each rewrite improves match score."
    ]
    for pt in points8:
        p = tf8.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)
        
    p = tf8.add_paragraph()
    p.text = "• Strategic Recommendations:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(8)
    p.space_after = Pt(6)
    
    p = tf8.add_paragraph()
    p.text = "• Provides actionable guidance for certifications, portfolio additions, and phrasing refinements."
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 9: Streamlit Interface & RAG Inspector ====================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide9, "Streamlit Dashboard & RAG Inspector")
    body9 = slide9.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(8.4), Inches(4.8))
    tf9 = body9.text_frame
    tf9.word_wrap = True
    
    p = tf9.paragraphs[0]
    p.text = "• RAG Vector Knowledge Base Inspector:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)
    
    ui_points = [
        "Vector Metrics: Displays total chunks indexed, evidence retrieved, and embedding dim.",
        "Evidence Cards: Visual breakdown of retrieved chunks with cosine similarity %.",
        "Interactive Vector Search: Real-time query tool allowing users to query resume vectors.",
        "Session State Retention: Preserves vector index and analysis across user interactions."
    ]
    for uip in ui_points:
        p = tf9.add_paragraph()
        p.text = f"   • {uip}"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)
        
    p = tf9.add_paragraph()
    p.text = "• Clean, Distraction-Free UI:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_before = Pt(10)
    p.space_after = Pt(6)
    
    err_points = [
        "Zero configuration clutter on the frontend; API key loaded securely via .env.",
        "Single best model (openai/gpt-oss-120b) for fast, deterministic evaluation.",
        "One-click export of analysis report to Markdown (.md) and JSON (.json)."
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
    p.text = "• The RAG AI Resume Analyzer delivers a complete, transparent document intelligence pipeline combining vector database retrieval with structured LLM reasoning."
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
        "True RAG Implementation: ChromaDB vector store + dense embeddings + cosine search.",
        "Sub-Second Response Times: Groq hardware acceleration paired with local ONNX embeddings.",
        "100% Deterministic & Repeatable: Identical scores guaranteed via hashing and greedy decoding.",
        "Anti-Hallucination Guardrails: Safe bullet rewrites substantiated by vector evidence.",
        "Production-Grade Software Design: Clean separation of RAG engine, LLM caller, and UI."
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
