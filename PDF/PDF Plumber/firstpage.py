# 1. Extract all text from the first page using pdfplumber

import pdfplumber

with pdfplumber.open("fed.pdf") as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    print(text)
