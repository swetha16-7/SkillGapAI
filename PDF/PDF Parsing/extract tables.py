#6.Extract tables from your PDF using pdfplumber.

import pdfplumber
pdf = pdfplumber.open("sample.pdf")
for page in pdf.pages:
    table = page.extract_table()
    if table:
        for row in table:
            print(row)

pdf.close()
