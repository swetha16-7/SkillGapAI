#9.Using the unified loader, display the resume preview (first 500 characters) and job description
#preview (first 500 characters).

import os
def load_file(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        import pdfplumber
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif ext == ".docx":
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        return ""

resume_text = load_file("resume.txt")
job_text = load_file("job_description.txt")

print("RESUME PREVIEW (First 500 Characters):\n")
print(resume_text[:500])

print("\nJOB DESCRIPTION PREVIEW (First 500 Characters):\n")
print(job_text[:500])
