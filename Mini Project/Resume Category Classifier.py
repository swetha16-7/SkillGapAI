'''Input a list of skills.
Use simple if/elif logic to classify:
Data/ML
Web Development
Software Development
Other
Print the predicted category. simple code'''

my_skills = ["HTML","CSS","JavaScript"]
data_ml = ["Python","Machine Learning","Data"]
web = ["HTML","CSS","JavaScript"]
software = ["Java","C++","Software"]
for s in my_skills:
    if s in data_ml:
        category = "Data/ML"
    elif s in web:
        category = "Web Development"
    elif s in software:
        category = "Software Development"

print("Predicted Category:",category)

Output:
Predicted Category: Web Development
