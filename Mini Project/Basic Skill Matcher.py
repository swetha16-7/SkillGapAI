'''
Take resume skills as comma-separated input.
Take job required skills as input.
Compare both lists.
Print matched and missing skills.'''

resume_skills=['WordPress','Elementor','WPBakery','Web Development','HTML','CSS','PHP','SQL','React','Javascript','Typescript','Docker','Kubernets','Git','MongoDB']
job_skills = ['HTML','CSS','JavaScript','React','Vue','Node.js','Python','Java','Spring','Ruby on Rails','SQL','MySQL','MongoDB','NoSQL','Git','Docker','AWS','Azure','GCP','Problem Solving','Communication','Testing','Architecture','UX/UI']
matched=[]
missing=[]
for i in job_skills:
    if i in resume_skills:
        matched.append(i)
    else:
        missing.append(i)
print(matched)
print(missing)