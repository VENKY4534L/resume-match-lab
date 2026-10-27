"""Resume and job-description text extraction and normalization."""
from pathlib import Path
import re

def extract_text_from_pdf(file_storage) -> str:
    """Extract text from a PDF uploaded through Flask using PyMuPDF."""
    import fitz
    data = file_storage.read()
    text_parts = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).strip()

def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9+#.\s/-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_terms(text: str) -> set[str]:
    """Extract terms from text. This is a transparent baseline, not an ML model."""
    normalized = normalize_text(text)
    words = re.findall(r"[a-z][a-z0-9+#.-]{1,}", normalized)
    stopwords = {
        "the","and","for","with","you","your","are","our","this","that","from",
        "have","has","will","can","all","not","but","who","what","when","where",
        "how","into","about","their","they","them","was","were","been","being",
        "job","role","work","working","using","use","used","required","preferred",
        "experience","years","year","ability","strong","good","plus","must","should"
    }
    return {w.strip(".-") for w in words if w not in stopwords and len(w.strip(".-")) > 1}
