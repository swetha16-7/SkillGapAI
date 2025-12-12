'''5. Add a new row to marks.csv with columns name, subject, marks.'''

import csv
new_row = ["Swetha", "Maths", 95]
with open("marks.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(new_row)
