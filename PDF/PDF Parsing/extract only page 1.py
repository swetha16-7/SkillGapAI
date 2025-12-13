#2. Extract text only from Page 1 of your PDF
from PyPDF2 import PdfReader
reader = PdfReader("CNS LAB EXTERNAL.pdf")
text = reader.pages[0].extract_text() 
print(text)                           
