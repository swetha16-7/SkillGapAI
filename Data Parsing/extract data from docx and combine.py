#7. Extract all paragraphs from a DOCX resume and combine into a single string
import docx

def extract_docx_text(file_path):
    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    print("Extracted DOCX Text:\n")
    print(text)

extract_docx_text("resume.docx")
