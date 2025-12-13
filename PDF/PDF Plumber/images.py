# Q8. Extract all embedded images from a page

import pdfplumber

with pdfplumber.open("fed.pdf") as pdf:
    images = pdf.pages[0].images
    print("Total images:", len(images))
