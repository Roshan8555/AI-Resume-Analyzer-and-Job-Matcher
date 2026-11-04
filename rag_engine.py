"""RAG (Retrieval-Augmented Generation) Engine for AI Resume Analyzer.

Implements:
1. Section-aware text chunking.
2. In-memory ChromaDB vector indexing.
3. Multi-query semantic retrieval with cosine similarity scoring.
4. Augmented context synthesis for LLM inference.
"""

import re
import uuid
from typing import List, Dict, Any, Tuple
import chromadb
from chromadb.config import Settings


def chunk_resume_text(resume_text: str, chunk_size: int = 350, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """Split resume text into semantic, section-aware chunks with metadata.
    
    Identifies common resume section headers (Experience, Skills, Education, etc.)
    and creates overlapping chunks preserving section context.
    """
    section_patterns = [
        r'(?:professional summary|summary|profile|about me)',
        r'(?:work experience|experience|employment history|work history)',
        r'(?:technical skills|skills|technologies|competencies)',
        r'(?:projects|key projects|personal projects)',
        r'(?:education|academic background|qualifications)',
        r'(?:certifications|licenses|courses)'
    ]
    # Non-capturing group with lookahead
    combined_pattern = re.compile(rf"\n(?={'|'.join(section_patterns)})", re.IGNORECASE)
    
    raw_sections = combined_pattern.split("\n" + resume_text)
    chunks = []
    chunk_index = 0

    for section_block in raw_sections:
        if not section_block:
            continue
        clean_block = section_block.strip()
        if not clean_block:
            continue
            
        first_line = clean_block.split("\n")[0].strip()
        current_section = "General"
        for pat in section_patterns:
            if re.search(pat, first_line, re.IGNORECASE):
                current_section = first_line.title()
                break

        words = clean_block.split()
        if not words:
            continue

        step = max(20, int(chunk_size / 6))
        overlap_step = max(5, int(chunk_overlap / 6))

        for i in range(0, len(words), step - overlap_step):
            chunk_words = words[i:i + step]
            chunk_str = " ".join(chunk_words)
            if len(chunk_str.strip()) < 25 and len(words) > 20:
                continue

            chunks.append({
                "chunk_id": f"chunk_{chunk_index:03d}",
                "section": current_section,
                "text": chunk_str
            })
            chunk_index += 1
            if i + step >= len(words):
                break

    # Fallback if no structured sections were created
    if not chunks:
        lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
        for idx, line in enumerate(lines):
            chunks.append({
                "chunk_id": f"chunk_{idx:03d}",
                "section": "General",
                "text": line
            })

    return chunks


class ResumeVectorIndex:
    """Manages ChromaDB vector indexing and semantic retrieval for a resume."""

    def __init__(self, collection_name: str = None):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False, is_persistent=False))
        self.collection_name = collection_name or f"resume_{uuid.uuid4().hex[:8]}"
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.chunks: List[Dict[str, Any]] = []

    def index_resume(self, resume_text: str) -> int:
        """Chunk resume text and index embeddings in ChromaDB."""
        self.chunks = chunk_resume_text(resume_text)
        if not self.chunks:
            return 0

        documents = [c["text"] for c in self.chunks]
        ids = [c["chunk_id"] for c in self.chunks]
        metadatas = [{"section": c["section"], "chunk_id": c["chunk_id"]} for c in self.chunks]

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        return len(self.chunks)

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Semantic search against resume vector store for a specific query."""
        if not self.chunks:
            return []

        k = min(top_k, len(self.chunks))
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        retrieved = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, dists):
                similarity = max(0.0, min(1.0, 1.0 - float(dist)))
                retrieved.append({
                    "chunk_id": meta.get("chunk_id", ""),
                    "section": meta.get("section", "General"),
                    "text": doc,
                    "similarity": round(similarity, 3)
                })

        return retrieved

    def retrieve_multiquery_context(self, job_description: str, top_k_per_query: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """Perform multi-query RAG retrieval for key job requirement dimensions."""
        queries = [
            f"Core technical skills, programming languages, and frameworks: {job_description[:200]}",
            f"Work experience, professional responsibilities, and projects: {job_description[:200]}",
            f"Tools, libraries, cloud deployment, and databases: {job_description[:200]}",
            f"Education, certifications, and domain qualifications: {job_description[:200]}"
        ]

        seen_chunk_ids = set()
        all_retrieved = []

        for q in queries:
            matches = self.retrieve(q, top_k=top_k_per_query)
            for m in matches:
                if m["chunk_id"] not in seen_chunk_ids:
                    seen_chunk_ids.add(m["chunk_id"])
                    all_retrieved.append(m)

        # Sort by similarity descending
        all_retrieved.sort(key=lambda x: x["similarity"], reverse=True)

        # Construct structured Augmented Context block
        context_lines = []
        for item in all_retrieved:
            context_lines.append(
                f"[{item['chunk_id']} | Section: {item['section']} | Relevance: {int(item['similarity'] * 100)}%]\n{item['text']}"
            )

        augmented_context_str = "\n\n".join(context_lines)
        return augmented_context_str, all_retrieved
