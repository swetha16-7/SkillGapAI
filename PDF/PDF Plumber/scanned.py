# 4. Detect whether your PDF is scanned (no extractable text)

import pdfplumber

text = ""

with pdfplumber.open("fed.pdf") as pdf:
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()

if not text.strip():
    print("Scanned PDF detected")
else:
    print("Text-based PDF")
