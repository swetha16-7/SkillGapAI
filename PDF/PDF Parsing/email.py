#9. Extract only email IDs (basic regex)

import re
from PyPDF2 import PdfReader

reader = PdfReader("Abstract.pdf")

text = ""
for page in reader.pages:
    text = text + page.extract_text()

emails = re.findall(r"\S+@\S+", text)
print(emails)
