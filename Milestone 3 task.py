#1. Remove duplicate skills from two given lists: resume skills and job description skills.
resume_skills = ["Python", "Data Analysis", "Machine Learning", "Python"]
job_description_skills = ["Machine Learning", "Deep Learning", "Data Analysis", "AI","AI"]
resume_skills=list(set(resume_skills))
job_description_skills=list(set(job_description_skills))
print(resume_skills)
print(job_description_skills)

#2. Convert all skills in a list to lowercase and remove extra spaces.
def normalize_skills(skills):
    return [skill.strip().lower() for skill in skills]
normalized_resume_skills = normalize_skills(resume_skills)
normalized_job_description_skills = normalize_skills(job_description_skills)
print(normalized_resume_skills)
print(normalized_job_description_skills)

#3. Store resume skills and job description skills in a single structured dictionary.
skill_data = {
    "resume_skills": normalized_resume_skills,
    "job_description_skills": normalized_job_description_skills
}
print(skill_data)

# 4. Load a pretrained Sentence-BERT model using Python.
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

#5. Generate an embedding for a single skill string and print its vector dimension.
embedding = model.encode("machine learning")
print(embedding.shape)

#6. Generate embeddings for a list of resume skills.
resume_embeddings = model.encode(resume_skills)
print(resume_embeddings)

#7. Generate embeddings for a list of job description skills.
job_description_embeddings = model.encode(job_description_skills)
print(job_description_embeddings)

#8. Compute cosine similarity between two skill embeddings.
from sklearn.metrics.pairwise import cosine_similarity
similarity_score = cosine_similarity([resume_embeddings[0]], [job_description_embeddings[0]])
print(similarity_score)

# 9. Compare one resume skill against all job description skills and print similarity scores.
similarity_scores = cosine_similarity([resume_embeddings[0]], job_description_embeddings)
print(similarity_scores)

# 10. Create a similarity matrix for all resume skills versus all job description skills.
similarity_matrix = cosine_similarity(resume_embeddings, job_description_embeddings)
print(similarity_matrix)

#11. Store the similarity matrix in a Pandas DataFrame with proper row and column labels.
import pandas as pd
similarity_df = pd.DataFrame(similarity_matrix, index=resume_skills, columns=
job_description_skills)
print(similarity_df)

# 12. For each job description skill, find the resume skill with the highest similarity score.
best_matches = similarity_df.idxmax()
print(best_matches)

# 13. Define similarity thresholds and classify skills as matched, partially matched, or missing.
matched_skills = {}
partial_skills = {}
missing_skills = []
for job_skill in similarity_df.columns:
    best_match = similarity_df[job_skill].idxmax()
    best_score = similarity_df[job_skill].max()
    if best_score >= 0.8:
        matched_skills[job_skill] = best_match
    elif best_score >= 0.5:
        partial_skills[job_skill] = best_match
    else:
        missing_skills.append(job_skill)
print("Matched Skills:", matched_skills)
print("Partially Matched Skills:", partial_skills)
print("Missing Skills:", missing_skills)

# 14. Generate a structured skill gap report containing matched, partial, and missing skills.
skill_gap_report = {
    "matched_skills": matched_skills,
    "partially_matched_skills": partial_skills,
    "missing_skills": missing_skills
}
print(skill_gap_report)

# 15. Save the skill gap report in JSON format.
import json
with open('skill_gap_report.json', 'w') as f:
    json.dump(skill_gap_report, f, indent=4)

# 16. Visualize the similarity matrix using a heatmap.
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
sns.heatmap(similarity_df, annot=True, cmap='YlGnBu')
plt.title('Skill Similarity Heatmap')
plt.show()  

#17. Add axis labels and a color legend to the heatmap.
plt.figure(figsize=(10, 6))
sns.heatmap(similarity_df, annot=True, cmap='YlGnBu')
plt.title('Skill Similarity Heatmap')
plt.xlabel('Job Description Skills')
plt.ylabel('Resume Skills')
plt.show()

#18. Highlight the highest similarity score in each column of the similarity matrix.
def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
styled_df = similarity_df.style.apply(highlight_max, axis=0)
styled_df   

#19. Handle cases where resume skills or job description skills are empty.
if not resume_skills or not job_description_skills:
    print("One of the skill lists is empty. Cannot compute similarity.")
else:
    similarity_matrix = cosine_similarity(resume_embeddings, job_description_embeddings)
    print(similarity_matrix)

#20. Normalize abbreviations such as ML, DL, and AI before generating embeddings.
abbreviation_map = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence"
}
def expand_abbreviations(skills):
    expanded_skills = []
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in abbreviation_map:
            expanded_skills.append(abbreviation_map[skill_lower])
        else:
            expanded_skills.append(skill)
    return expanded_skills
expanded_resume_skills = expand_abbreviations(resume_skills)
expanded_job_description_skills = expand_abbreviations(job_description_skills)
print(expanded_resume_skills)
print(expanded_job_description_skills)

#21. Compare similarity results using two different Sentence-BERT models.
model1 = SentenceTransformer('all-MiniLM-L6-v2')
model2 = SentenceTransformer('paraphrase-MiniLM-L3-v2')
embeddings1_resume = model1.encode(resume_skills)
embeddings1_jd = model1.encode(job_description_skills)
embeddings2_resume = model2.encode(resume_skills)
embeddings2_jd = model2.encode(job_description_skills)
similarity_matrix1 = cosine_similarity(embeddings1_resume, embeddings1_jd)
similarity_matrix2 = cosine_similarity(embeddings2_resume, embeddings2_jd)
print("Similarity Matrix from Model 1:")
print(similarity_matrix1)
print("Similarity Matrix from Model 2:")
print(similarity_matrix2)

#22. Cache embeddings so repeated skills are not embedded multiple times.
embedding_cache = {}
def get_embedding(skill, model):
    if skill not in embedding_cache:
        embedding_cache[skill] = model.encode(skill)
    return embedding_cache[skill]
cached_resume_embeddings = [get_embedding(skill, model) for skill in resume_skills]
cached_jd_embeddings = [get_embedding(skill, model) for skill in job_description_skills]
print(cached_resume_embeddings)
print(cached_jd_embeddings)

#23. Build a pipeline that takes raw resume text and job description text and outputs a skill gap report.
def skill_gap_pipeline(resume_skills, job_description_skills):
    # Normalize skills
    resume_skills = normalize_skills(resume_skills)
    job_description_skills = normalize_skills(job_description_skills)
    
    # Expand abbreviations
    resume_skills = expand_abbreviations(resume_skills)
    job_description_skills = expand_abbreviations(job_description_skills)
    
    # Generate embeddings
    resume_embeddings = [get_embedding(skill, model) for skill in resume_skills]
    jd_embeddings = [get_embedding(skill, model) for skill in job_description_skills]
    
    # Compute similarity matrix
    similarity_matrix = cosine_similarity(resume_embeddings, jd_embeddings)
    similarity_df = pd.DataFrame(similarity_matrix, index=resume_skills, columns=job_description_skills)
    
    # Identify matches
    matched_skills = {}
    partial_skills = {}
    missing_skills = []
    for job_skill in similarity_df.columns:
        best_match = similarity_df[job_skill].idxmax()
        best_score = similarity_df[job_skill].max()
        if best_score >= 0.8:
            matched_skills[job_skill] = best_match
        elif best_score >= 0.5:
            partial_skills[job_skill] = best_match
        else:
            missing_skills.append(job_skill)
    
    # Create report
    skill_gap_report = {
        "matched_skills": matched_skills,
        "partially_matched_skills": partial_skills,
        "missing_skills": missing_skills
    }
    
    return skill_gap_report
report = skill_gap_pipeline(resume_skills, job_description_skills)
print(report)

#24. Return the top three closest resume skills for each job description skill.
top_matches = {}
for job_skill in similarity_df.columns:
    top_three = similarity_df[job_skill].nlargest(3).index.tolist()
    top_matches[job_skill] = top_three
print("Top three matches per job description skill:")
print(top_matches)

#25. Apply different similarity thresholds for technical skills and soft skills.
technical_skills = {"python", "machine learning", "data analysis", "deep learning"}
def classify_with_skill_type(skill, score):
    if skill.lower() in technical_skills:
        if score >= 0.8:
            return "Matched"
        elif score >= 0.6:
            return "Partial"
        else:
            return "Missing"
    else:
        if score >= 0.7:
            return "Matched"
        elif score >= 0.5:
            return "Partial"
        else:
            return "Missing"
skill_gap_report_custom = {
    "Matched": [],
    "Partial": [],
    "Missing": []
}
for jd_skill in similarity_df.columns:
    best_resume = similarity_df[jd_skill].idxmax()
    score = similarity_df[jd_skill].max()
    skill_gap_report_custom[classify_with_skill_type(jd_skill, score)].append({
        "jd_skill": jd_skill,
        "best_resume_skill": best_resume,
        "similarity_score": round(score, 3)
    })
print(skill_gap_report_custom)  

#26. Compute an overall resume and job description alignment score.
overall_score = similarity_matrix.mean()
print("Overall Resume-JD Alignment Score:", round(overall_score, 3))

# 27. Export the skill gap report and similarity heatmap into a single file.
with open('skill_gap_report_and_heatmap.txt', 'w') as f:
    f.write("Skill Gap Report:\n")
    json.dump(skill_gap_report, f, indent=4)
    f.write("\n\nSimilarity Heatmap:\n")
    f.write(similarity_df.to_string())

# 28. Design a modular architecture separating embedding generation, similarity computation, and reporting.
def generate_embeddings(skills, model):
    return [get_embedding(skill, model) for skill in skills]
def compute_similarity_matrix(embeddings1, embeddings2):
    return cosine_similarity(embeddings1, embeddings2)
def generate_skill_gap_report(similarity_df):
    matched_skills = {}
    partial_skills = {}
    missing_skills = []
    for job_skill in similarity_df.columns:
        best_match = similarity_df[job_skill].idxmax()
        best_score = similarity_df[job_skill].max()
        if best_score >= 0.8:
            matched_skills[job_skill] = best_match
        elif best_score >= 0.5:
            partial_skills[job_skill] = best_match
        else:
            missing_skills.append(job_skill)
    return {
        "matched_skills": matched_skills,
        "partially_matched_skills": partial_skills,
        "missing_skills": missing_skills
    }
resume_embeddings = generate_embeddings(resume_skills, model)
jd_embeddings = generate_embeddings(job_description_skills, model)
similarity_matrix = compute_similarity_matrix(resume_embeddings, jd_embeddings)
similarity_df = pd.DataFrame(similarity_matrix, index=resume_skills, columns=job_description_skills)
skill_gap_report = generate_skill_gap_report(similarity_df)
print(skill_gap_report)
