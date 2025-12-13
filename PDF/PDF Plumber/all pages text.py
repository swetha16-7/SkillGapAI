# 2. Extract text from all pages in your PDF

import pdfplumber

with pdfplumber.open("sample2.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
