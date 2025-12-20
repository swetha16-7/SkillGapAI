#15. Parse multiple resumes of different formats and store their cleaned text in a list.


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

def load_file(path):
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

def parse_multiple_resumes(paths):
    cleaned_resumes = []

    for path in paths:
        text = load_file(path)
        cleaned_resumes.append(clean_text(text))

    return cleaned_resumes

resume_files = [
    "resume1.pdf",
    "resume2.docx",
    "resume3.txt"
]

cleaned_resume_list = parse_multiple_resumes(resume_files)

for i, resume in enumerate(cleaned_resume_list, start=1):
    print(resume)
