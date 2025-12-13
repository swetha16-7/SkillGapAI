# Q5. Extract the first table on page 1 of your PDF

import pdfplumber

with pdfplumber.open("fed.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()
    if tables:
        print(tables[0])
    else:
        print("No table found")
