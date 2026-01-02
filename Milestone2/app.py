from flask import Flask, request, render_template, session, redirect, url_for
import pdfplumber
import docx
import re

from skills import (
    extract_skills,
    format_resume_for_highlight,
    calculate_match_score,
    calculate_skill_match_score,
    calculate_avg_confidence
)

from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

app = Flask(__name__)
app.secret_key = "milestone_secret_key"


# --------------------------------------------------
# CLEAR SESSION ON FIRST OPEN
# --------------------------------------------------
@app.before_request
def clear_session_on_first_open():
    if request.endpoint == "index" and request.method == "GET":
        session.clear()


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
                    full_text.append(" ".join(cells))

    return "\n".join(full_text)


# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d -]{8,}\d', '', text)
    text = re.sub(r'[^a-z\s\n]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


# ---------------- FILE PARSER ----------------
def parse_file(file):
    name = file.filename.lower()
    extracted = ""

    if name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    extracted += page.extract_text() + "\n"

    elif name.endswith(".docx"):
        extracted = read_docx(file)

    elif name.endswith(".txt"):
        extracted = file.read().decode("utf-8", errors="ignore")

    return clean_text(extracted)


# ---------------- FORMAT FOR PREVIEW ----------------
def format_text(text):
    return "".join(f"<p>{line}</p>" for line in text.split("\n") if line.strip())


# ---------------- MILESTONE 1 ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    active = request.form.get("active", session.get("active", "resume"))
    session["active"] = active

    resume = session.get("resume_preview", {"html": "", "chars": 0, "words": "", "filename": ""})
    jd = session.get("jd_preview", {"html": "", "chars": 0, "words": "", "filename": ""})

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            raw_text = parse_file(file)

            preview = {
                "html": format_text(raw_text),
                "chars": len(raw_text),
                "words": len(raw_text.split()),
                "filename": file.filename
            }

            session[f"{active}_text"] = raw_text

            if active == "resume":
                session["resume_preview"] = preview
                resume = preview
            else:
                session["jd_preview"] = preview
                jd = preview

    return render_template("index.html", resume=resume, jd=jd, active=active)

def get_top_skill(skills_dict):
    if not skills_dict:
        return None
    return max(skills_dict.items(), key=lambda x: x[1])


# ---------------- RESET ----------------
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


# ---------------- MILESTONE 2 ----------------
@app.route("/skill-extraction")
def skill_extraction():
    resume_text = session.get("resume_text")
    jd_text = session.get("jd_text")

    if not resume_text or not jd_text:
        return "Please upload both Resume and Job Description first."

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # ✅ AVG CONFIDENCE (NEW)
    resume_avg = calculate_avg_confidence(resume_skills)
    jd_avg = calculate_avg_confidence(jd_skills)

    highlighted_resume = format_resume_for_highlight(
        resume_text,
        resume_skills["technical_skills"].keys(),
        resume_skills["soft_skills"].keys()
    )

    highlighted_jd = format_resume_for_highlight(
        jd_text,
        jd_skills["technical_skills"].keys(),
        jd_skills["soft_skills"].keys()
    )

    match_score = calculate_match_score(resume_text, jd_text)
    skill_match_score = calculate_skill_match_score(resume_skills, jd_skills)

    return render_template(
        "skills.html",
        resume=resume_skills,
        jd=jd_skills,
        resume_avg_confidence=resume_avg,
        jd_avg_confidence=jd_avg,
        highlighted_resume=highlighted_resume,
        highlighted_jd=highlighted_jd,
        match_score=match_score,
        skill_match_score=skill_match_score
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
