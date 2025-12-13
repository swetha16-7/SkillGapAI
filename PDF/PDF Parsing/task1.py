#1. Extract all text from a PDF using PyPDF2
from PyPDF2 import PdfReader
reader = PdfReader("CNS LAB EXTERNAL.pdf")
text = ""
for page in reader.pages:
    text = text + page.extract_text()

print(text)
