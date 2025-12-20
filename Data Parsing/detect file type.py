# 4. Given a file path, detect whether the file is PDF, DOCX, or TXT.
def detect_file_type(file_path):
    if file_path.endswith(".pdf"):
        print("File type: PDF")
    elif file_path.endswith(".docx"):
        print("File type: DOCX")
    elif file_path.endswith(".txt"):
        print("File type: TXT")
    else:
        print("Unknown file type")

detect_file_type("C:\\M SWETHA\\OneDrive\\Desktop\\Data parsing\\resume.txt")
