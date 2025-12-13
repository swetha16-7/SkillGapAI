#3. Count the total number of pages in your PDF
from PyPDF2 import PdfReader
reader = PdfReader("CNS LAB EXTERNAL.pdf")
print("Total pages:", len(reader.pages))
