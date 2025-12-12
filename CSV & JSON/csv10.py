'''10. Copy all contents from source.csv to copy.csv.'''

import csv

with open("source.csv", "r") as src, open("copy.csv", "w", newline="") as dst:
    reader = csv.reader(src)
    writer = csv.writer(dst)

    for row in reader:
        writer.writerow(row)
