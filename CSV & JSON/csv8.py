'''8. Convert a list of lists into a CSV file (id, name).'''

import csv
data = [
    [1, "Arun"],
    [2, "Meera"],
    [3, "David"]
]
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name"])  # header
    writer.writerows(data)
