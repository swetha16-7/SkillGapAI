# 1. Create a Python list containing five technical skills and print the list.
technical_skills = ["Python", "SQL", "Java", "JavaScript", "C++"]
print("Technical Skills:", technical_skills)

# 2. Create a Python list containing five soft skills and print the list.
soft_skills = ["Communication", "Teamwork", "Problem-solving", "Adaptability", "Time Management"]
print("Soft Skills:", soft_skills)

#3. Convert the following resume text to lowercase using Python: 'Experienced in Python and SQL'.
resume_text = 'Experienced in Python and SQL'
print("Lowercase Resume Text:", resume_text.lower())

#4. Check whether the word 'python' exists in a given resume text.
if 'python' in resume_text.lower():
    print("'python' exists in the resume text.")
else:
    print("'python' does not exist in the resume text.")    

#5. Store technical skills and soft skills in two separate Python lists and print them using a loop.
print("Technical Skills:")
for i in range(len(technical_skills)):
    print(technical_skills[i])
print("Soft Skills:")
for i in range(len(soft_skills)):
    print(soft_skills[i])

#6. Extract technical skills from a resume text using a predefined Python skill list.
resume_text = 'Experienced in Python and SQL'
predefined_skills = ["python", "sql", "java", "javascript", "c++", "html", "css"]
extracted_skills = []
for skill in predefined_skills:
    if skill in resume_text.lower():
        extracted_skills.append(skill)
print("Extracted Technical Skills from Resume:", extracted_skills)

#7. Extract soft skills from a job description text using a predefined Python skill list.
job_description_text = 'We are looking for candidates with excellent communication and teamwork skills.'
predefined_soft_skills = ["communication", "teamwork", "problem-solving", "adaptability", "time management"]
extracted_soft_skills = []
for skill in predefined_soft_skills:
    if skill in job_description_text.lower():
        extracted_soft_skills.append(skill)
print("Extracted Soft Skills from Job Description:", extracted_soft_skills) 

#8. Read skills from a CSV file (skills.csv) and print only the technical skills.
import csv

with open("skills.csv", newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['skill_type'] == 'Technical':
            print(row['skill_name'])
  

#9. Compare resume text and job description text to find common skills.
resume_text = 'Experienced in Python, SQL, and Java.'
job_description_text = 'Looking for expertise in Java, JavaScript, and Python.'
predefined_skills = ["python", "sql", "java", "javascript", "c++"]
common_skills=[]
for skill in predefined_skills:
    if skill in resume_text.lower() and skill in job_description_text.lower():
        common_skills.append(skill)
print("Common Skills between Resume and Job Description:", common_skills)

#10. Store extracted skills in a Python list without duplicates.
all_extracted_skills = extracted_skills + extracted_soft_skills + common_skills
unique_skills = list(set(all_extracted_skills))
print("Unique Extracted Skills:", unique_skills)


#11. Store extracted skills in a Python dictionary with skill categories as keys.
skills_dict = {
    "Technical": list(set(extracted_skills + common_skills)),
    "Soft": extracted_soft_skills
}
print("Skills Dictionary:", skills_dict)


#12. Compare resume skills with job description skills and identify missing skills.
resume_skills = []
job_skills = []

for skill in predefined_skills:
    if skill in resume_text.lower():
        resume_skills.append(skill)
    if skill in job_description_text.lower():
        job_skills.append(skill)

missing_skills = list(set(job_skills) - set(resume_skills))
print("Missing Skills from Resume:", missing_skills)


#13. Count how many times each skill appears in the resume text.
skill_count = {}
for skill in predefined_skills:
    skill_count[skill] = resume_text.lower().count(skill)

print("Skill Frequency in Resume:", skill_count)


#14. Load skills from a CSV file and perform case-insensitive skill matching.
matched_skills = []

with open("skills.csv", newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['skill_name'].lower() in resume_text.lower():
            matched_skills.append(row['skill_name'].lower())

print("CSV Matched Skills (Case-Insensitive):", matched_skills)


#15. Save the extracted skills into a new CSV file.
with open("extracted_skills.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Skill"])
    for skill in unique_skills:
        writer.writerow([skill])

print("Extracted skills saved to extracted_skills.csv")
