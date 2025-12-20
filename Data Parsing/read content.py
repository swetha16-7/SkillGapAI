#1. Read a .txt resume file and print its full content.
with open('resume.txt', 'r') as file:
    content = file.read()
    print(content)  