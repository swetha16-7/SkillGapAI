'''JOB TITLE NORMALIZER
Input job title text.
Remove special characters.
Convert text to title case.
Print normalized job title.'''

job_titles = [
    "full-stack developer @ amazon!!!",
    "senior python engineer (remote)",
    "software developer -- java",
    "front-end engineer###",
    "data-science lead!!!"
]
print("Normalized job titles:")
for i in range(len(job_titles)):
    clean = ""
    for ch in job_titles[i]:
        if ch.isalnum() or ch.isspace():   
            clean += ch

    print(clean.title())


Output:
Normalized job titles:
Fullstack Developer  Amazon
Senior Python Engineer Remote
Software Developer  Java
Frontend Engineer
Datascience Lead
