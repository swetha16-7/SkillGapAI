#4. Detect whether your PDF is scanned (empty text extraction).
from PyPDF2 import PdfReader
reader = PdfReader("Doc1.pdf")
text = ""

for page in reader.pages:
    text += page.extract_text() or ""

if text.strip() == "":
    print("Scanned PDF detected")
else:
    print("Text-based PDF")
