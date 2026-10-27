# Resume Match Lab — AI Resume Analyzer & Job Match System

A local Flask application that compares a text-based PDF resume with a job description. It reports a transparent keyword-match estimate, mapped skills found in both texts, mapped skills to review, shared terms, and job terms missing from the resume.

> **Honest limitation:** This is a rule-based keyword/NLP baseline, not a trained machine-learning model, not a commercial ATS, and not a predictor of interview or hiring outcomes. It does not make hiring decisions.

## Features

- Upload a text-based PDF resume (max 5 MB)
- Paste a job description
- Extract PDF text with PyMuPDF
- Normalize text and compare terms
- Detect common skills with aliases (e.g. GenAI / LLM)
- Show matched skills, skill gaps, shared terms, and terms to review
- Print or save the report as PDF using the browser
- Unit tests for the matching logic
- No external API key required; no resume file is saved to disk by the app

## Tech stack

Python 3.10+, Flask, PyMuPDF, HTML, CSS, unittest.

## Run on Windows PowerShell

```powershell
cd "path\to\resume_analyzer_job_match_system"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

If PowerShell blocks activation, either use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that PowerShell window and activate again, or skip activation and run `.venv\Scripts\python.exe -m pip install -r requirements.txt` followed by `.venv\Scripts\python.exe run.py`.

Open http://127.0.0.1:5000 in your browser.

If `python` is not found, install Python 3.10+ and enable “Add Python to PATH” during installation.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Matching method

The score combines:
- 70% mapped skill coverage: mapped skills found in the resume divided by mapped skills detected in the job description.
- 30% term overlap: unique normalized job-description terms also found in the resume divided by unique normalized job-description terms.

This weighting is a project design choice, not an industry-standard formula. The skill dictionary is deliberately limited and may miss synonyms or context. A keyword's presence does not prove proficiency; review every result manually.

## Privacy and security

- Resume PDF contents are read in memory and not written to a local upload folder.
- Avoid putting real resumes, personal information, API keys, or credentials in Git.
- The development server uses Flask debug mode. It is intended for local demonstration, not public production deployment. Turn debug mode off before any deployment.
- Scanned/image-only PDFs are not OCR'd; the app will ask for a text-based PDF if extraction returns too little text.

## Repository layout

```text
resume_analyzer_job_match_system/
├── app/
│   ├── analyzer.py
│   ├── text_processing.py
│   ├── main.py
│   ├── templates/
│   └── static/
├── tests/
├── sample_data/
├── requirements.txt
├── run.py
└── README.md
```

## Resume bullet (use only after you run and verify it)

**Resume Match Lab — Python, Flask, PDF Text Extraction, NLP/Keyword Matching**
- Built a Flask web application to compare PDF resumes against job descriptions and surface matched skills, missing keywords, and transparent match metrics.
- Implemented PDF text extraction, skill-alias matching, keyword overlap scoring, and automated unit tests.

## Future improvements

- Add OCR for scanned PDFs
- Expand skill taxonomy and synonym handling
- Add optional semantic embeddings and retrieval with a clearly documented model
- Export a structured JSON report
- Add integration tests and deployment configuration
