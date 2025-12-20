#8. Create a unified function load_file(path) that reads PDF, DOCX, and TXT files.

import os
import pdfplumber
import docx

def load_file(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    # TXT file
    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    # PDF file
    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    # DOCX file
    elif ext == ".docx":
        doc = docx.Document(path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        return "Unsupported file format"


content = load_file("resume.pdf")
print(content)


