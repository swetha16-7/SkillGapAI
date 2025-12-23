from flask import Flask, request, render_template
import pdfplumber
import docx
import re

from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

app = Flask(__name__)

# ---------------- DOCX PARSING ----------------
def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Invalid parent type")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def read_docx(file):
    doc = docx.Document(file)
    full_text = []

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph) and block.text.strip():
            full_text.append(block.text)
        elif isinstance(block, Table):
            for row in block.rows:
                cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if cells:
                    full_text.append(" | ".join(cells))

    return "\n".join(full_text)

# ---------------- TXT CLEANING ----------------
def clean_and_normalize_text(text):
    text = text.lower()
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d -]{8,}\d', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# ---------------- FILE PARSER ----------------
def parse_file(file):
    name = file.filename.lower()
    extracted = ""

    if name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    extracted += t + "\n"

    elif name.endswith(".docx"):
        extracted = read_docx(file)

    elif name.endswith(".txt"):
        extracted = file.read().decode("utf-8", errors="ignore")

    return extracted

# ---------------- TEXT FORMATTING ----------------
def format_text(text):
    formatted = ""

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        formatted += f"<p style='font-weight: normal;'>{line}</p>"

    return formatted

# ---------------- MAIN ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    active = request.form.get("active", "resume")

    resume = {"html": "", "chars": 0, "words": 0, "filename": ""}
    jd = {"html": "", "chars": 0, "words": 0, "filename": ""}

    if request.method == "POST":
        file = request.files.get("file")

        if file:
            raw_text = parse_file(file)
            formatted_html = format_text(raw_text)

            chars = len(raw_text)
            words = len(raw_text.split())

            if active == "resume":
                resume.update(
                    html=formatted_html,
                    chars=chars,
                    words=words,
                    filename=file.filename
                )
            else:
                jd.update(
                    html=formatted_html,
                    chars=chars,
                    words=words,
                    filename=file.filename
                )

    return render_template(
        "index.html",
        resume=resume,
        jd=jd,
        active=active
    )

if __name__ == "__main__":
    app.run(debug=True)
