#17. Parse multiple resumes along with one job description and generate previews for each resume.

import os
import pdfplumber
import docx

def clean_text(text):
    return " ".join(text.split())

def detect_file_type(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext == ".pdf":
        return "PDF"
    elif ext == ".docx":
        return "DOCX"
    elif ext == ".txt":
        return "TXT"
    else:
        return "UNSUPPORTED"

def safe_load(path):
    file_type = detect_file_type(path)

    if file_type == "PDF":
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text

    elif file_type == "DOCX":
        doc = docx.Document(path)
        return " ".join(para.text for para in doc.paragraphs)

    elif file_type == "TXT":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file type: {path}")

def universal_parser(path, preview_chars=300):
    text = safe_load(path)
    cleaned = clean_text(text)
    print(f"\n--- Preview for {os.path.basename(path)} ---")
    print(cleaned[:preview_chars])
    return cleaned

def parse_resumes_with_jd(resume_paths, jd_path):
    jd = universal_parser(jd_path)
    resumes = []
    for path in resume_paths:
        resumes.append(universal_parser(path))
    return resumes, jd

resume_files = ["resume1.pdf", "resume3.txt", "resume2.docx"]
job_description_file = "job_description.txt"

parsed_resumes, parsed_jd = parse_resumes_with_jd(resume_files, job_description_file)
