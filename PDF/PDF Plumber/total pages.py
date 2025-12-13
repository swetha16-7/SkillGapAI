# 3. Count the total number of pages in your PDF

import pdfplumber

with pdfplumber.open("fed.pdf") as pdf:
    print("Total pages:", len(pdf.pages))
