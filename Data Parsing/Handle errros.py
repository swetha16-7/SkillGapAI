#12. Handle error cases such as unsupported file types, empty files, and invalid file paths.

import os
def load_file(path):
    if not os.path.exists(path):
        print("Error: Invalid file path.")
        return None

    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext not in ['.txt', '.pdf', '.docx']:
        print("Error: Unsupported file type.")
        return None
    if ext == '.txt':
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()

    if not text.strip():
        print("Error: File is empty.")
        return None

    print("File loaded successfully.")
    return text

icontent = load_file("sample.txt")
