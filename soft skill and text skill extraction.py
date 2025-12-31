#1. Extract technical skills from a given resume text using spaCy PhraseMatcher.
import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")
TECH_SKILLS = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "nlp", "data science", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "flask", "django",
    "aws", "azure", "docker", "kubernetes", "git", "linux"
]
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in TECH_SKILLS]
matcher.add("TECH_SKILLS", patterns)
resume_text = """
Final-year Computer Science student skilled in Python, Java, ML, SQL.
  Worked with Flask, NumPy, AWS, and Git. Strong communication and teamwork skills.
"""
doc = nlp(resume_text)
matches = matcher(doc)
skills = set()
for _, start, end in matches:
    skills.add(doc[start:end].text.lower())
print("spaCy PhraseMatcher Skills:")
print(list(skills))
'''Output:
spaCy PhraseMatcher Skills:
['aws', 'flask', 'python', 'java', 'git', 'numpy', 'sql']'''

# 2. Create a predefined skill list and match it against input text using spaCy.
import spacy
nlp = spacy.load("en_core_web_sm")
SKILL_LIST = [
    "python", "sql", "machine learning",
    "data science", "flask", "numpy", "aws", "git",
    "communication", "teamwork"
]
resume_text = """
Strong communication skills.
Experienced in Python and Machine Learning using Flask.
"""
doc = nlp(resume_text)
skills = set()
for chunk in doc.noun_chunks:
    chunk_text = chunk.text.lower()
    for skill in SKILL_LIST:
        if skill in chunk_text:
            skills.add(skill)
print(list(skills))
#Output: ['python', 'machine learning', 'communication', 'flask']

#3. Use spaCy NER to identify skill-related entities from job description text.

job_description_text = job_description_text.replace("-", " ")
doc = nlp(job_description_text)
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in MASTER_SKILL_LIST]
matcher.add("MASTER_SKILLS", patterns)
identified_skills = []
for _, start, end in matcher(doc):
    identified_skills.append(doc[start:end].text.lower())
print("Final extracted skills from Job Description:")
print(identified_skills)
'''Output:
Final extracted skills from Job Description:
['python', 'java', 'aws', 'azure', 'communication', 'teamwork', 'problem solving', 'python', 'java']'''

# 4. Normalize extracted skills by converting them to lowercase and removing duplicates.
normalized_skills = sorted(list(set(identified_skills)))
print("Normalized Skills (lowercase and unique):")
print(normalized_skills)
'''Output:
Normalized Skills (lowercase and unique):
['aws', 'azure', 'communication', 'java', 'problem solving', 'python', 'teamwork']'''


# 5. Store extracted skills in a dictionary with technical_skills and soft_skills keys.
skills_dict = {
    "technical_skills": [
        skill for skill in normalized_skills if skill in TECHNICAL_SKILLS
    ],
    "soft_skills": [
        skill for skill in normalized_skills if skill in SOFT_SKILLS
    ]
}
print(skills_dict)

# Output: {'technical_skills': ['aws', 'azure', 'java', 'python'], 'soft_skills': ['communication', 'problem solving', 'teamwork']}

# 6. Merge skill outputs from spaCy Matcher and spaCy NER into a single list.

matcher_skills=['aws', 'flask', 'python', 'java', 'git', 'numpy', 'sql']
ner_skills= ['aws', 'azure', 'communication', 'java', 'problem solving', 'python', 'teamwork']

merged_skills = matcher_skills + ner_skills

print(merged_skills)
#Output: ['aws', 'flask', 'python', 'java', 'git', 'numpy', 'sql', 'aws', 'azure', 'communication', 'java', 'problem solving', 'python', 'teamwork']

# 7. Implement logic to resolve conflicts such as abbreviations and full-form skills (e.g., ML and machine learning).

skill_map = {
    "ml": "machine learning",
    "nlp": "natural language processing",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "tf": "tensorflow"
}

def resolve_skills(skills):
    final_skills = set()

    for skill in skills:
        skill = skill.lower().strip()
        final_skills.add(skill_map.get(skill, skill))

    return list(final_skills)

skills = ["ML", "Deep Learning","NLP", "Python", "TF"]
print(resolve_skills(skills))
# Output: ['tensorflow', 'python', 'machine learning', 'natural language processing', 'deep learning']

# 8. Use Sentence-BERT to calculate similarity between sentences and a master skill list.
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
skills = ["Python programming", "Data analysis", "Machine learning"]
sentences = ["I love coding in Python.", "I work with data every day."]
skill_emb = model.encode(skills, convert_to_tensor=True)
sent_emb = model.encode(sentences, convert_to_tensor=True)
sim = util.cos_sim(sent_emb, skill_emb)
for i, s in enumerate(sentences):
    print(f"\n{s}")
    best_match = skills[sim[i].argmax()]
    print(f"Best skill match: {best_match} (score={sim[i].max():.4f})")
'''Output:

I love coding in Python.
Best skill match: Python programming (score=0.7599)

I work with data every day.
Best skill match: Data analysis (score=0.4183)'''


# 9. Apply a similarity threshold to decide whether a sentence represents a valid skill.
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
skills = ["Python programming", "Data analysis", "Machine learning"]
sentences = [
    "I love coding in Python.",
    "I love machine learning approaches",
    "I enjoy painting landscapes.",
    "I work with data every day."
]

skill_emb = model.encode(skills, convert_to_tensor=True)
sent_emb = model.encode(sentences, convert_to_tensor=True)
sim = util.cos_sim(sent_emb, skill_emb)
THRESHOLD = 0.6
for i, s in enumerate(sentences):
    best_idx = sim[i].argmax()
    best_score = sim[i][best_idx].item()
    best_skill = skills[best_idx]

    print(f"\nSentence: {s}")
    if best_score >= THRESHOLD:
        print(f"Valid skill match: {best_skill} (score={best_score:.4f})")
    else:
        print(f"No valid skill found (best score={best_score:.4f})")
'''Output:

Sentence: I love coding in Python.
 Valid skill match: Python programming (score=0.7599)

Sentence: I love machine learning approaches
 Valid skill match: Machine learning (score=0.7008)

Sentence: I enjoy painting landscapes.
 No valid skill found (best score=0.1098)

Sentence: I work with data every day.
No valid skill found (best score=0.4183)'''

# 10. Categorize merged skills into technical and soft skills using a mapping approach.
skill_mapping = {
    "Python programming": "Technical",
    "Data analysis": "Technical",
    "Machine learning": "Technical",
    "Compiler design": "Technical",
    "Debugging": "Technical",
    "Simulation logic": "Technical",
    "Geometric reasoning": "Technical",
    "Communication": "Soft",
    "Teamwork": "Soft",
    "Problem solving": "Soft",
    "Leadership": "Soft",
    "Adaptability": "Soft",
    "Time management": "Soft"
}

merged_skills = [
    "Python programming",
    "Teamwork",
    "Machine learning",
    "Leadership",
    "Debugging",
    "Adaptability"
]

categorized = {"Technical": [], "Soft": []}

for skill in merged_skills:
    category = skill_mapping.get(skill, "Uncategorized")
    categorized.setdefault(category, []).append(skill)

print("Technical Skills:", categorized["Technical"])
print("Soft Skills:", categorized["Soft"])
'''Output:
Technical Skills: ['Python programming', 'Machine learning', 'Debugging']
Soft Skills: ['Teamwork', 'Leadership', 'Adaptability']'''

#11. Build a function that accepts resume text and returns a unified skill list using spaCy and BERT.
import spacy
from sentence_transformers import SentenceTransformer, util
nlp = spacy.load("en_core_web_sm")
bert_model = SentenceTransformer("all-MiniLM-L6-v2")
MASTER_SKILLS = [
    "Python programming", "Data analysis", "Machine learning",
    "Compiler design", "Debugging", "Simulation logic",
    "Geometric reasoning", "Communication", "Teamwork",
    "Problem solving", "Leadership", "Adaptability", "Time management"
]
MASTER_EMB = bert_model.encode(MASTER_SKILLS, convert_to_tensor=True)

def extract_unified_skills(resume_text, threshold=0.6):
    """
    Accepts resume text and returns a unified skill list
    using spaCy for phrase extraction and Sentence-BERT for similarity.
    """
    doc = nlp(resume_text)
    candidate_skills = [chunk.text.strip() for chunk in doc.noun_chunks]

    cand_emb = bert_model.encode(candidate_skills, convert_to_tensor=True)

    sim_matrix = util.cos_sim(cand_emb, MASTER_EMB)

    unified_skills = set()
    for i, cand in enumerate(candidate_skills):
        best_idx = sim_matrix[i].argmax()
        best_score = sim_matrix[i][best_idx].item()
        if best_score >= threshold:
            unified_skills.add(MASTER_SKILLS[best_idx])
    return list(unified_skills)
resume_text = """
Experienced software engineer with strong skills in Python, debugging,
teamwork, and machine learning. Worked on simulation logic and compiler design projects.
"""
skills = extract_unified_skills(resume_text)
print("Unified Skill List:", skills)
#Output: Unified Skill List: ['Machine learning', 'Python programming', 'Simulation logic', 'Teamwork', 'Compiler design']


#12. Handle overlapping skills detected by multiple pipelines and keep only one standardized version.
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")
MASTER_SKILLS = [
    "Python programming", "Data analysis", "Machine learning",
    "Compiler design", "Debugging", "Simulation logic",
    "Geometric reasoning", "Communication", "Teamwork",
    "Problem solving", "Leadership", "Adaptability", "Time management"
]

MASTER_EMB = model.encode(MASTER_SKILLS, convert_to_tensor=True)

def unify_skills(detected_skills, threshold=0.7):
    """
    Handle overlapping skills detected by multiple pipelines
    and return standardized skill list.
    """
    unified = set()
    cand_emb = model.encode(detected_skills, convert_to_tensor=True)
    sim_matrix = util.cos_sim(cand_emb, MASTER_EMB)

    for i, cand in enumerate(detected_skills):
        best_idx = sim_matrix[i].argmax()
        best_score = sim_matrix[i][best_idx].item()
        if best_score >= threshold:
            unified.add(MASTER_SKILLS[best_idx])
        else:
            unified.add(cand)
    return list(unified)
pipeline1_skills = ["Python", "ML", "Debugging"]
pipeline2_skills = ["Python programming", "Machine learning", "Teamwork"]
merged = pipeline1_skills + pipeline2_skills
final_skills = unify_skills(merged)
print("Unified Skill List:", final_skills)
'''Output:
Unified Skill List: ['Machine learning', 'Python programming', 'Teamwork', 'Debugging', 'ML']'''


#13. Design a pipeline that prioritizes spaCy-based skills over BERT-based skills when both detect the same skill.
import spacy
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer, util
nlp = spacy.load("en_core_web_sm")
bert = SentenceTransformer("all-MiniLM-L6-v2")

SKILLS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "python",
    "java",
    "tensorflow"
]

def spacy_skills(text):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("SKILLS", [nlp(s) for s in SKILLS])
    doc = nlp(text.lower())
    return list(set(doc[start:end].text.lower() for _, start, end in matcher(doc)))

def bert_skills(text, threshold=0.6):
    sent_emb = bert.encode(text, convert_to_tensor=True)
    skill_emb = bert.encode(SKILLS, convert_to_tensor=True)
    scores = util.cos_sim(sent_emb, skill_emb)[0]
    return [SKILLS[i] for i, s in enumerate(scores) if s > threshold]

def merge(spacy_out, bert_out):
    final = set(spacy_out)              
    final.update(s for s in bert_out if s not in final)
    return list(final)

text = "Experience with ML, NLP and Python"
text = text.lower().replace("ml","machine learning").replace("nlp","natural language processing")
print(merge(spacy_skills(text), bert_skills(text)))

#Output: ['python', 'natural language processing', 'machine learning']

# 14. Generate a final structured output and save it as final_skills.json.
import json
skill_mapping = {
    "python programming": "Technical",
    "data analysis": "Technical",
    "machine learning": "Technical",
    "compiler design": "Technical",
    "debugging": "Technical",
    "simulation logic": "Technical",
    "geometric reasoning": "Technical",
    "communication": "Soft",
    "teamwork": "Soft",
    "problem solving": "Soft",
    "leadership": "Soft",
    "adaptability": "Soft",
    "time management": "Soft",
    "python": "Technical",
    "java": "Technical",
    "aws": "Technical",
    "azure": "Technical",
    "docker": "Technical",
    "kubernetes": "Technical",
    "tensorflow": "Technical",
    "pytorch": "Technical",
    "pandas": "Technical",
    "numpy": "Technical",
    "data science": "Technical"
}
categorized_output = {
    "technical_skills": [],
    "soft_skills": []
}
for skill in resolved_skills:
    skill_lower = skill.lower()
    category = skill_mapping.get(skill_lower)
    if category == "Technical":
        categorized_output["technical_skills"].append(skill)
    elif category == "Soft":
        categorized_output["soft_skills"].append(skill)
final_categorized_output = {
    "technical_skills": sorted(set(categorized_output["technical_skills"])),
    "soft_skills": sorted(set(categorized_output["soft_skills"]))
}
with open("final_skills.json", "w", encoding="utf-8") as f:
    json.dump(final_categorized_output, f, indent=4)

print("final_skills.json saved successfully.")

'''Output:
final_skills.json saved successfully.
{
    "technical_skills": [
        "aws",
        "data science",
        "docker",
        "java",
        "kubernetes",
        "machine learning",
        "numpy",
        "pandas",
        "python",
        "tensorflow"
    ],
    "soft_skills": [
        "adaptability",
        "communication",
        "problem solving",
        "teamwork",
        "time management"
    ]
}
'''

# 15. Compare the results of spaCy-only, BERT-only, and combined pipelines for skill extraction accuracy.

import spacy
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
bert_model = SentenceTransformer("all-MiniLM-L6-v2")

MASTER_SKILLS = [
    "python", "java", "machine learning", "deep learning",
    "natural language processing", "sql", "tensorflow", "pytorch"
]

SKILL_MAP = {
    "ml": "machine learning",
    "nlp": "natural language processing"
}
def extract_spacy_matcher_skills(text):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp(skill) for skill in MASTER_SKILLS]
    matcher.add("SKILLS", patterns)

    doc = nlp(text)
    matches = matcher(doc)

    return set(doc[start:end].text.lower() for _, start, end in matches)

def extract_bert_skills(text, threshold=0.6):
    processed = text.lower()
    for abbr, full in SKILL_MAP.items():
        processed = processed.replace(abbr, full)

    sent_emb = bert_model.encode(processed, convert_to_tensor=True)
    skill_embs = bert_model.encode(MASTER_SKILLS, convert_to_tensor=True)

    scores = util.cos_sim(sent_emb, skill_embs)[0]

    return {
        MASTER_SKILLS[i]
        for i, score in enumerate(scores)
        if score >= threshold
    }


def extract_skills_pipeline(text, threshold=0.6):
    spacy_skills = extract_spacy_matcher_skills(text)
    bert_skills = extract_bert_skills(text, threshold)

    combined = sorted(set(spacy_skills) | set(bert_skills))

    return combined, spacy_skills, bert_skills


def compare_pipelines(text):
    spacy_only = extract_spacy_matcher_skills(text)
    bert_only = extract_bert_skills(text)
    combined, _, _ = extract_skills_pipeline(text)

    return {
        "spacy_only": list(spacy_only),
        "bert_only": list(bert_only),
        "combined": combined
    }

text = "Experience with ML, NLP and Python-based model deployment"
print(compare_pipelines(text))
#  Output: {'spacy_only': ['python'], 'bert_only': [], 'combined': ['python']}