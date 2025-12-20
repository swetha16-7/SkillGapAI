#20. Create an end-to-end script that performs file loading, parsing, cleaning, preview display, and
#saving parsed output.

import os
import json
import logging
import pdfplumber
import docx

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def clean_text(text):
    return " ".join(text.split())

def detect_file_type(path):
    _, ext = os.path.splitext(path)
    return ext.lower()

def safe_load(path):
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

def format_preview(title, text, length=500):
    print(f"\n--- {title} PREVIEW ---")
    print(text[:length])

def save_to_json(resume, jd, filename="parsed_output.json"):
    data = {
        "resume_cleaned": clean_text(resume),
        "job_description_cleaned": clean_text(jd)
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def main():
    resume_path = "resume.pdf"
    jd_path = "job_description.txt"

    resume_text = safe_load(resume_path)
    jd_text = safe_load(jd_path)

    format_preview("RESUME", resume_text, 500)
    format_preview("JOB DESCRIPTION", jd_text, 500)

    save_to_json(resume_text, jd_text)

if __name__ == "__main__":
    main()
