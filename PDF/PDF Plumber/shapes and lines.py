# Q9. Extract all lines and shapes (vector objects) from the PDF

import pdfplumber

with pdfplumber.open("shapes.pdf") as pdf:
    page = pdf.pages[0]
    print("Lines:", len(page.lines))
    print("Rectangles:", len(page.rects))
