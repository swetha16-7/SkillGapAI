#16. Build a universal parser that detects file type, extracts text, cleans text, and displays a preview.

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

def universal_parser(path):
    text = safe_load(path)
    cleaned = clean_text(text)
    print(cleaned)

    return cleaned
universal_parser("resume1.pdf")
