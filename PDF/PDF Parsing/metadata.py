#7.Extract PDF metadata

from PyPDF2 import PdfReader

reader = PdfReader("sample2.pdf")
meta = reader.metadata

print("Title:", meta.title)
print("Author:", meta.author)
print("Creation Date:", meta.get("/CreationDate"))
