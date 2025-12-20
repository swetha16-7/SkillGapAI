#19. Replicate the complete Milestone-1 output including file upload simulation, parsed document
#preview, and cleaned text generation.

import os
import json
import logging
import pdfplumber
import docx
from preview_formatter import format_preview

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def clean_text(text):
    return " ".join(text.split())

def detect_file_type(path):
    _, ext = os.path.splitext(path)
    return ext.lower()

def load_file(path):
    ext = detect_file_type(path)

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text

    elif ext == ".docx":
        doc = docx.Document(path)
        return " ".join(p.text for p in doc.paragraphs)

    elif ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file type")

def simulate_upload(resume_path, jd_path):
    resume_text = load_file(resume_path)
    jd_text = load_file(jd_path)
    return resume_text, jd_text

def save_to_json(resume, jd, filename="milestone_1_output.json"):
    data = {
        "resume_cleaned": resume,
        "job_description_cleaned": jd
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def milestone_1(resume_path, jd_path):
    resume, jd = simulate_upload(resume_path, jd_path)

    format_preview("RESUME", resume)
    format_preview("JOB DESCRIPTION", jd)

    resume_clean = clean_text(resume)
    jd_clean = clean_text(jd)

    save_to_json(resume_clean, jd_clean)

milestone_1("resume.pdf", "job_description.txt")
