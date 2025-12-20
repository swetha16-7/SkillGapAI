#5. Load two text files (resume and job description) and confirm successful loading.
def load_files(resume_path, job_path):
    try:
        with open(resume_path, 'r', encoding='utf-8') as resume:
            resume_text = resume.read()

        with open(job_path, 'r', encoding='utf-8') as job:
            job_text = job.read()

        print("Resume file loaded successfully.")
        print("Job description file loaded successfully.")

    except FileNotFoundError:
        print("One or both files not found.")

load_files("resume.txt", "job_description.txt")