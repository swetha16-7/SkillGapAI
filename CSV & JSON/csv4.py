'''4. Read a CSV using DictReader and print all key-value pairs for each row.'''

import csv
with open("students.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for key, value in row.items():
            print(f"{key}: {value}")
        print()
