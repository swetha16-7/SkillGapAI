# 6. Extract text from a PDF resume using a Python PDF library.
from PyPDF2 import PdfReader

def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    print("Extracted PDF Text:\n")
    print(text)

extract_pdf_text("resume.pdf")
