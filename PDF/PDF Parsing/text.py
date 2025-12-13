#8.Save extracted text into a text file
from PyPDF2 import PdfReader

reader = PdfReader("sample.pdf")

text = ""
for page in reader.pages:
    text = text + page.extract_text()

file = open("output.txt", "w")
file.write(text)
file.close()
