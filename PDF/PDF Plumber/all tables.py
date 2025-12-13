# Q6. Extract all tables from your entire PDF

import pdfplumber

all_tables = []

with pdfplumber.open("fed.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        if tables:
            all_tables.extend(tables)

print("Total tables found:", len(all_tables))
