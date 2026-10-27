from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from .analyzer import analyze_resume
from .text_processing import extract_text_from_pdf

ALLOWED_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/analyze")
    def analyze():
        uploaded = request.files.get("resume")
        job_description = request.form.get("job_description", "").strip()
        if not uploaded or not uploaded.filename:
            return render_template("index.html", error="Please upload a PDF resume.")
        if not uploaded.filename.lower().endswith(".pdf"):
            return render_template("index.html", error="Only PDF resumes are supported.")
        if not job_description:
            return render_template("index.html", error="Paste a job description.")
        try:
            resume_text = extract_text_from_pdf(uploaded)
            if len(resume_text.strip()) < 30:
                return render_template("index.html", error="No readable text found. If this is a scanned PDF, run OCR first.")
            result = analyze_resume(resume_text, job_description)
            return render_template("results.html", result=result, filename=secure_filename(uploaded.filename))
        except Exception as exc:
            app.logger.exception("Resume analysis failed")
            return render_template("index.html", error=f"Could not analyze this PDF. Check that it is a valid, text-based PDF. ({type(exc).__name__})"), 400

    @app.errorhandler(413)
    def too_large(_error):
        return render_template("index.html", error="File is too large. Maximum size is 5 MB."), 413

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
