'''2. Write a Python program to read and print each row from employees.csv.'''

import csv
with open("employees.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
