'''3. From products.csv, print only the first column (product names).'''

import csv
with open("products.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row[0])
