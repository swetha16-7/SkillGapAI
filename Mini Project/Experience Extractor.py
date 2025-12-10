'''EXPERIENCE EXTRACTOR

Input: sentence like
“I have 3 years of experience in Python.”

Extract the number of years using string
methods.

Output:
“Experience Detected: X Years”'''

text="Experienced Full Stack Web Developer with over 5 years of experience "
year=""
for i in text:
    if i.isdigit():
        print(i)