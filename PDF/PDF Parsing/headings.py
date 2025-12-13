#5. Extract headings (lines in uppercase or bold-like text).
from PyPDF2 import PdfReader

reader = PdfReader("sample.pdf")

for page in reader.pages:
    lines = page.extract_text().split("\n")
    for line in lines:
        if line.isupper():
            print(line)

