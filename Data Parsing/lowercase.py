#3. Given extracted text, convert it to lowercase and remove extra spaces.
with open("resume.txt", "r", encoding="utf-8") as file:
    extracted_text = file.read()
extracted_text = extracted_text.lower()
extracted_text = " ".join(extracted_text.split())
print(extracted_text)

