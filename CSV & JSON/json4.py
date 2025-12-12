'''4. Write a dictionary into student.json'''

import json

student = {'name': 'Mia', 'age': 24, 'grade': 'A'}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)
