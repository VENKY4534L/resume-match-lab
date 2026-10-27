"""Transparent baseline resume-to-job matching."""
from .text_processing import extract_terms, normalize_text

# Common skill phrases are handled explicitly so multi-word skills aren't lost.
SKILL_ALIASES = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "javascript": ["javascript", "typescript"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi"],
    "rest apis": ["rest api", "rest apis", "api integration"],
    "git": ["git", "github", "gitlab"],
    "docker": ["docker", "containerization"],
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud", "vertex ai"],
    "azure": ["azure", "microsoft azure"],
    "machine learning": ["machine learning", "ml fundamentals", "scikit-learn"],
    "generative ai": ["generative ai", "genai", "llm", "large language model"],
    "prompt engineering": ["prompt engineering", "prompt design"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "langchain": ["langchain", "langgraph"],
    "nlp": ["nlp", "natural language processing"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "html/css": ["html", "css"],
    "react": ["react", "react.js"],
    "node.js": ["node.js", "nodejs"],
    "mongodb": ["mongodb", "mongo db"],
    "communication": ["communication", "collaboration"],
    "testing": ["unit testing", "pytest", "testing", "test cases"],
    "data analysis": ["data analysis", "data analytics", "data cleaning"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel", "spreadsheets"],
}

def analyze_resume(resume_text: str, job_text: str) -> dict:
    """Return a keyword-based comparison. Not a prediction of hiring outcomes."""
    resume_norm = normalize_text(resume_text)
    job_norm = normalize_text(job_text)
    if not resume_norm or not job_norm:
        raise ValueError("Both resume text and job description are required.")

    matched = []
    missing = []
    for skill, aliases in SKILL_ALIASES.items():
        job_has = any(normalize_text(alias) in job_norm for alias in aliases)
        if job_has:
            (matched if any(normalize_text(alias) in resume_norm for alias in aliases) else missing).append(skill)

    job_terms = extract_terms(job_text)
    resume_terms = extract_terms(resume_text)
    shared_terms = sorted(job_terms & resume_terms)
    missing_terms = sorted(job_terms - resume_terms)
    total_skills = len(matched) + len(missing)
    skill_coverage = round(100 * len(matched) / total_skills) if total_skills else 0
    total_terms = len(job_terms)
    term_coverage = round(100 * len(shared_terms) / total_terms) if total_terms else 0
    score = round(0.7 * skill_coverage + 0.3 * term_coverage)

    return {
        "score": score,
        "skill_coverage": skill_coverage,
        "term_coverage": term_coverage,
        "matched_skills": matched,
        "missing_skills": missing,
        "shared_terms": shared_terms[:30],
        "missing_terms": missing_terms[:40],
        "job_skill_count": total_skills,
        "matched_skill_count": len(matched),
        "note": "This is a transparent keyword-overlap estimate, not an ATS score or a prediction of hiring success."
    }
