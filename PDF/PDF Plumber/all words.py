# Q7. Extract all words along with their bounding-box coordinates

import pdfplumber

with pdfplumber.open("fed.pdf") as pdf:
    words = pdf.pages[0].extract_words()
    for word in words:
        print(word)
