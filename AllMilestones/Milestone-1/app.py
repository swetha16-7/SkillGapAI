# ======================================================
# IMPORTS
# ======================================================
from flask import (
    Flask, request, render_template, session,
    redirect, url_for
)
import pdfplumber
import docx
import re
import os
import json
import csv

from skills import (
    extract_skills,
    format_resume_for_highlight,
    calculate_match_score,
    calculate_skill_match_score,
    calculate_avg_confidence,
    build_similarity_matrix
)

from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


# ======================================================
# APP CONFIG
# ======================================================
app = Flask(__name__)
app.secret_key = "milestone_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ======================================================
# CLEAR SESSION ON FIRST LOAD
# ======================================================
@app.before_request
def clear_session_on_first_open():
    if request.endpoint == "index" and request.method == "GET":
        session.clear()


# ======================================================
# DOCX PARSER
# ======================================================
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


# ======================================================
# TEXT CLEANING
# ======================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d -]{8,}\d', '', text)
    text = re.sub(r'[^a-z\s\n]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


# ======================================================
# FILE PARSER
# ======================================================
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


# ======================================================
# FORMAT FOR PREVIEW
# ======================================================
def format_text(text):
    return "".join(f"<p>{line}</p>" for line in text.split("\n") if line.strip())


# ======================================================
# MILESTONE 1 – UPLOAD & PARSE
# ======================================================
@app.route("/", methods=["GET", "POST"])
def index():
    active = request.form.get("active", session.get("active", "resume"))
    session["active"] = active

    resume = session.get("resume_preview", {"html": "", "chars": 0, "words": 0, "filename": ""})
    jd = session.get("jd_preview", {"html": "", "chars": 0, "words": 0, "filename": ""})

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


# ======================================================
# MILESTONE 2 – SKILL EXTRACTION
# ======================================================
@app.route("/skill-extraction")
def skill_extraction():
    resume_text = session.get("resume_text")
    jd_text = session.get("jd_text")

    if not resume_text or not jd_text:
        return redirect(url_for("index"))

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    return render_template(
        "skills.html",
        resume=resume_skills,
        jd=jd_skills,
        resume_avg_confidence=calculate_avg_confidence(resume_skills),
        jd_avg_confidence=calculate_avg_confidence(jd_skills),
        highlighted_resume=format_resume_for_highlight(
            resume_text,
            resume_skills["technical_skills"].keys(),
            resume_skills["soft_skills"].keys()
        ),
        highlighted_jd=format_resume_for_highlight(
            jd_text,
            jd_skills["technical_skills"].keys(),
            jd_skills["soft_skills"].keys()
        ),
        match_score=calculate_match_score(resume_text, jd_text),
        skill_match_score=calculate_skill_match_score(resume_skills, jd_skills)
    )


# ======================================================
# MILESTONE 3 – SKILL GAP + EXPORT
# ======================================================
@app.route("/milestone3")
def milestone3():
    resume_text = session.get("resume_text")
    jd_text = session.get("jd_text")

    if not resume_text or not jd_text:
        return redirect(url_for("index"))

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    resume_all = list(set(resume_skills["technical_skills"]) | set(resume_skills["soft_skills"]))
    jd_all = list(set(jd_skills["technical_skills"]) | set(jd_skills["soft_skills"]))

    matrix, resume_labels, jd_labels = build_similarity_matrix(resume_all, jd_all)

    # ---- FILTER WEAK SIMILARITIES ----
    FILTER_THRESHOLD = 0.45
    filtered_matrix = [
        [v if v >= FILTER_THRESHOLD else None for v in row]
        for row in matrix
    ]

    matched = sum(1 for row in matrix for v in row if v >= 0.8)
    partial = sum(1 for row in matrix for v in row if 0.5 <= v < 0.8)
    missing = len(set(jd_all) - set(resume_all))
    overall = int(calculate_match_score(resume_text, jd_text))

    return render_template(
        "milestone3.html",
        matrix=filtered_matrix,        # ✅ REQUIRED
        resume_labels=resume_labels,   # ✅ REQUIRED
        jd_labels=jd_labels,           # ✅ REQUIRED
        matched=matched,
        partial=partial,
        missing=missing,
        overall=overall,
        missing_skills=sorted(set(jd_all) - set(resume_all))
    )



# ======================================================
# ✅ MILESTONE 4 – DASHBOARD + UPSKILLING
# ======================================================
@app.route("/milestone4")
def milestone4():
    json_path = os.path.join(OUTPUT_DIR, "skill_gap.json")

    if not os.path.exists(json_path):
        return redirect(url_for("milestone3"))

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    skill_scores = {
        skill: (100 if skill in data["resume_skills"] else 30)
        for skill in data["jd_skills"]
    }

    RECOMMENDATIONS = {
        "python": "Complete Python for Data Science (Coursera / Udemy)",
        "data science": "IBM / Google Data Science Professional Certificate",
        "machine learning": "Machine Learning by Andrew Ng",
        "deep learning": "Deep Learning Specialization",
        "sql": "SQL for Data Analysis",
        "git": "Git & GitHub Essentials",
        "aws": "AWS Cloud Practitioner",
        "docker": "Docker for Developers",
        "flask": "Flask Web Development Bootcamp",

        "communication": "Business Communication Skills Training",
        "collaboration": "Team Collaboration & Agile Practices",
        "problem solving": "Problem Solving & Critical Thinking Course",
        "time management": "Time Management & Productivity Training",
        "leadership": "Leadership & People Management Program"
    }

    upskilling = []
    for skill in data["missing_skills"]:
        key = skill.lower()
        upskilling.append({
            "skill": skill,
            "recommendation": RECOMMENDATIONS.get(
                key,
                "Relevant professional course or certification"
            )
        })

    return render_template(
        "Milestone4.html",
        overall=data["overall_match"],
        matched=data["matched"],
        missing=data["missing"],
        skill_scores=skill_scores,
        upskilling=upskilling,
        job_seeker=[80, 70, 65, 75, 60],
        recruiter=[95, 85, 80, 85, 75]
    )


# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)
