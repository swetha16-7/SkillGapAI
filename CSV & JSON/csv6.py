'''6. Count how many rows exist in data.csv (excluding the header).'''

import csv
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader) 
    count = sum(1 for row in reader)
print("Total rows:", count)
