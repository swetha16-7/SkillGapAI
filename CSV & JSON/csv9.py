'''9. Filter and print rows from people.csv where age > 30.'''

import csv
with open("people.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if int(row["age"]) > 30:
            print(row)
