'''10. Create items.json and print total cost'''
import json

items = [
    {'item': 'Pen', 'price': 10},
    {'item': 'Book', 'price': 50},
    {'item': 'Bag', 'price': 700}
]
with open("items.json", "w") as file:
    json.dump(items, file, indent=4)
total = sum(item['price'] for item in items)
print("Total Cost:", total)

'''Output:
Total Cost: 760
'''