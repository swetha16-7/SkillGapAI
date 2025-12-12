'''1. Create a CSV file named students.csv with columns name, age, grade and write 3 student records.'''

import csv
with open("students.csv","w",newline="") as file:
    writer=csv.writer(file)
    writer.writerow(["name","age","grade"])
    writer.writerow(["swetha","21","A"])
    writer.writerow(["John","22","B"])
    writer.writerow(["Swathi","20","C"])
