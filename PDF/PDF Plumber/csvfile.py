# Q10. Extract a table from the PDF and save it as a CSV file

import pdfplumber
import csv

with pdfplumber.open("fed.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()

    if tables:
        with open("table.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in tables[0]:
                writer.writerow(row)
        print("Table saved as table.csv")
    else:
        print("No table found")
