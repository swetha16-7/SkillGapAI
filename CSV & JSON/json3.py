'''3. Read data.json and print all key-value pairs'''

import json

with open("data.json", "r") as file:
    data = json.load(file)
for key, value in data.items():
    print(key, ":", value)

'''
Output:
name : Swetha
age : 21
city : Hyderabad
course : Computer Science
marks : 92
'''