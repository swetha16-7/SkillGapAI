#14. Save cleaned resume and job description text into a JSON file.

import json

def clean_text(text):
    return " ".join(text.split())

def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_to_json(resume_txt_path, job_description_text, filename="parsed_data.json"):
    resume_text = read_txt_file(resume_txt_path)

    data = {
        "resume": clean_text(resume_text),
        "job_description": clean_text(job_description_text)
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Data saved successfully in {filename}")

# -------- Example Run --------
resume_file = "resume.txt"
job_description = "job_description.txt"

save_to_json(resume_file, job_description)

