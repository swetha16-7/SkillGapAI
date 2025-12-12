'''7. Read sales.csv and calculate total sales (item, price, quantity).'''

import csv
total_sales = 0
with open("sales.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        total_sales += price * quantity
print("Total Sales:", total_sales)
