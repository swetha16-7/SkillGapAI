#18. Create a separate module that handles only parsed document preview formatting.
import pdfplumber
import logging
from preview_formatter import format_preview

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def clean_text(text):
    return " ".join(text.split())

def load_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text

resume_path = "resume.pdf"

resume_text = load_pdf(resume_path)
cleaned_resume = clean_text(resume_text)

format_preview("RESUME", cleaned_resume)
