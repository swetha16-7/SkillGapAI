# 11. Simulate file upload by accepting resume and job description file paths and parsing both.

def parse_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."


resume_path = "resume.txt"
job_desc_path = "job_description.txt"
resume_text = parse_file(resume_path)
job_desc_text = parse_file(job_desc_path)

print("RESUME CONTENT:\n")
print(resume_text)

print("\nJOB DESCRIPTION CONTENT:\n")
print(job_desc_text)
