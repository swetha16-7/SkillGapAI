import re
import spacy
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer, util
from markupsafe import Markup

# ---------------- LOAD MODELS ----------------
nlp = spacy.load("en_core_web_sm")
bert_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- MASTER SKILL LIST ----------------
TECHNICAL_SKILLS = [
    "python", "java", "c", "c++", "html", "sql",
    "machine learning", "deep learning", "nlp", "data science",
    "tensorflow", "pytorch", "pandas", "numpy", "statistics",
    "data visualization", "aws", "azure", "docker", "kubernetes",
    "git", "flask", "django"
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "adaptability", "time management", "critical thinking",
    "collaboration", "decision making"
]

ALL_SKILLS = TECHNICAL_SKILLS + SOFT_SKILLS


# ---------------- spaCy EXACT MATCH ----------------
def spacy_extract(text):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in ALL_SKILLS]
    matcher.add("SKILLS", patterns)

    doc = nlp(text)
    matches = matcher(doc)

    return set(doc[start:end].text.lower() for _, start, end in matches)


# ---------------- BERT SENTENCE-LEVEL CONFIDENCE ----------------
def bert_sentence_confidence(text):
    sentences = [sent.text for sent in nlp(text).sents]
    if not sentences:
        return {}

    sentence_embs = bert_model.encode(sentences, convert_to_tensor=True)
    skill_embs = bert_model.encode(ALL_SKILLS, convert_to_tensor=True)

    sim_matrix = util.cos_sim(skill_embs, sentence_embs)

    scores = {}
    for i, skill in enumerate(ALL_SKILLS):
        max_sim = float(sim_matrix[i].max())

        # ✅ CONFIDENCE CALIBRATION (IMPORTANT)
        ui_score = 60 + (min(max_sim, 1.0) * 35)   # 60–95
        scores[skill] = round(ui_score)

    return scores


# ---------------- FINAL SKILL EXTRACTION ----------------
def extract_skills(text):
    text = text.lower()

    spacy_skills = spacy_extract(text)
    bert_scores = bert_sentence_confidence(text)

    technical = {}
    soft = {}

    for skill in spacy_skills:
        if skill in bert_scores:
            if skill in TECHNICAL_SKILLS:
                technical[skill] = bert_scores[skill]
            elif skill in SOFT_SKILLS:
                soft[skill] = bert_scores[skill]

    return {
        "technical_skills": technical,
        "soft_skills": soft
    }


# ---------------- AVG CONFIDENCE ----------------
def calculate_avg_confidence(extracted_skills):
    scores = (
        list(extracted_skills["technical_skills"].values()) +
        list(extracted_skills["soft_skills"].values())
    )
    if not scores:
        return 0
    return round(sum(scores) / len(scores))


# ---------------- HIGHLIGHTING ----------------
def format_resume_for_highlight(text, technical, soft):
    output = text

    for skill in technical:
        output = re.sub(
            rf"\b{re.escape(skill)}\b",
            f'<mark class="tech">{skill}</mark>',
            output,
            flags=re.IGNORECASE
        )

    for skill in soft:
        output = re.sub(
            rf"\b{re.escape(skill)}\b",
            f'<mark class="soft">{skill}</mark>',
            output,
            flags=re.IGNORECASE
        )

    return Markup("<p>" + "</p><p>".join(output.split("\n")) + "</p>")


# ---------------- RESUME–JD MATCH ----------------
def calculate_match_score(resume_text, jd_text):
    r_emb = bert_model.encode(resume_text, convert_to_tensor=True)
    j_emb = bert_model.encode(jd_text, convert_to_tensor=True)
    sim = util.cos_sim(r_emb, j_emb)[0][0]
    return round(float(sim) * 100, 2)


def calculate_skill_match_score(resume_skills, jd_skills):
    resume_all = {**resume_skills["technical_skills"], **resume_skills["soft_skills"]}
    jd_all = {**jd_skills["technical_skills"], **jd_skills["soft_skills"]}

    if not jd_all:
        return 0

    matched = [resume_all[s] for s in jd_all if s in resume_all]
    if not matched:
        return 0

    return round(sum(matched) / len(jd_all), 2)
