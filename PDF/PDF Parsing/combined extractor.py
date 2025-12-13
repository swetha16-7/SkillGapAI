'''
10. Create a combined extractor:
- Try PyPDF2
- If empty → try pdfplumber
- If still empty → print 'Scanned PDF detected'
'''

from PyPDF2 import PdfReader
import pdfplumber

file_path = "sample.pdf"
text = ""

# Step 1: Try extracting text using PyPDF2
try:
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
except:
    pass

# Step 2: If PyPDF2 fails, try pdfplumber
if not text.strip():
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except:
        pass

# Step 3: If both fail, detect scanned PDF
if not text.strip():
    print("Scanned PDF detected")
else:
    print(text)
