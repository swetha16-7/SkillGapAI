#1. Install spaCy & load model
import spacy
nlp = spacy.load("en_core_web_sm")

#2. Extract Python & SQL using PhraseMatcher
from spacy.matcher import PhraseMatcher

matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp("Python"), nlp("SQL")]
matcher.add("SKILLS", patterns)

doc = nlp("I have experience in Python and SQL.")
skills = [doc[start:end].text for _, start, end in matcher(doc)]
print(skills)

#3. Convert list of skills into PhraseMatcher patterns
skills = ["Python", "SQL", "NLP", "Machine Learning", "Data Analysis"]
patterns = [nlp(skill) for skill in skills]

#4. Convert extracted skills to lowercase
lower_skills = [skill.lower() for skill in skills]
print(lower_skills)

#5. Remove duplicate skills
skills = ["python", "sql", "python", "nlp"]
unique_skills = list(set(skills))
print(unique_skills)

#6. Extract skills from sentence

matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp("Python"), nlp("NLP"), nlp("Machine Learning"), nlp("SQL")]
matcher.add("TECH", patterns)

doc = nlp("Experience in Python, NLP, and Machine Learning with SQL.")
print([doc[start:end].text for _, start, end in matcher(doc)])

#7. Identify soft skills using token comparison
soft_skills = ["communication", "teamwork", "leadership"]

doc = nlp("Strong communication and teamwork skills.")
found = [t.text for t in doc if t.text.lower() in soft_skills]
print(found)

#8. Case-insensitive PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql")])

doc = nlp("Experienced in PYTHON and Sql")
print([doc[start:end].text for _, start, end in matcher(doc)])

#9. Store skills in JSON
skills_json = {
    "technical_skills": ["python", "sql"],
    "soft_skills": ["communication"]
}
print(skills_json)

#10. Remove duplicates from repeated mentions

doc = nlp("Python Python SQL SQL NLP")
skills = ["python", "sql", "nlp", "python"]
print(list(set(skills)))

#11. Handle punctuation
doc = nlp("Python, SQL; NLP.")
matcher = PhraseMatcher(nlp.vocab)
matcher.add("TECH", [nlp("Python"), nlp("SQL"), nlp("NLP")])
print([doc[start:end].text for _, start, end in matcher(doc)])


#12. Combine technical + soft skill extraction
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql")])

soft_skills = ["communication", "teamwork"]
doc = nlp("Python developer with communication skills")

tech = [doc[start:end].text.lower() for _, start, end in matcher(doc)]
soft = [t.text.lower() for t in doc if t.text.lower() in soft_skills]

print({"technical_skills": tech, "soft_skills": soft})

#13. Extract from multiple sentences
text = "Python developer. Experience with SQL. Good communication."
doc = nlp(text)

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql")])

tech = list(set([doc[start:end].text.lower() for _, start, end in matcher(doc)]))
soft = ["communication"] if "communication" in text.lower() else []

print({"technical_skills": tech, "soft_skills": soft})

#14. Match SQL but NOT NoSQL
doc = nlp("Experience in SQL and NoSQL databases")

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("sql")])

skills = []
for _, start, end in matcher(doc):
    if doc[start:end].text.lower() == "sql" and "nosql" not in doc.text.lower():
        skills.append("sql")

print(skills)

# 15. Resume vs Job Description extraction**
def extract(text):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("TECH", [nlp("python"), nlp("sql"), nlp("nlp")])

    doc = nlp(text)
    return list(set([doc[start:end].text.lower() for _, start, end in matcher(doc)]))

resume = "Python developer with NLP experience"
job = "Looking for Python and SQL skills"

print("Resume Skills:", extract(resume))
print("Job Skills:", extract(job))
