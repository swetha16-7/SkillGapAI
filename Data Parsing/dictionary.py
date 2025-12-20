#13. Store parsed resume and job description text in a structured dictionary.

import os

def load_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")

def store_parsed_data(resume_path, jd_path):
    data = {}

    try:
        resume_text = load_file(resume_path)
        jd_text = load_file(jd_path)

        data["resume"] = {
            "raw_text": resume_text
        }
        data["job_description"] = {
            "raw_text": jd_text
        }

        print("Files uploaded and parsed successfully.")

    except Exception as e:
        print("Error:", e)

    return data


resume_file = "resume.txt"
job_desc_file = "job_description.txt"

parsed_data = store_parsed_data(resume_file, job_desc_file)

print("\nStructured Dictionary Output:\n")
print(parsed_data)
