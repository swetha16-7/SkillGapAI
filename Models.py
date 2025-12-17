import os
import sys
import json
import re
import statistics
import time


# 1. Square root using math.sqrt()
import math
print(math.sqrt(25))
# Output: 5.0


# 2. Floor and Ceil of 5.67
import math
print(math.floor(5.67))
print(math.ceil(5.67))
# Output:
# 5
# 6


# 3. Random number between 1 and 100
import random
print(random.randint(1, 100))
# Output: 42


# 4. Print 5 random integers between 10 and 20
import random
for i in range(5):
    print(random.randint(10, 20))
# Output: 16


# 5. Print today's date
import datetime
print(datetime.date.today())
# Output: 2025-12-17


# 6. Print current year, month, day
import datetime
today = datetime.date.today()
print(today.year)
print(today.month)
print(today.day)
# Output:
# 2025
# 12
# 17


# 7. Current working directory
import os
print(os.getcwd())
# Output: C:\Users\Swetha\Desktop


# 8. List all files in current directory
import os
print(os.listdir())
# Output: ['models.py']


# 9. Python version
import sys
print(sys.version)
# Output: Python 3.13.7 (tags/v3.13.7:aa7ca6a, Aug  7 2024, 10:15:42) [MSC v.1936 64 bit (AMD64)]


# 10. JSON string to dictionary
import json
json_str = '{"name":"Swetha","age":21}'
data = json.loads(json_str)
print(data)
# Output: {'name': 'Swetha', 'age': 21}


# 11. Math functions
import math
print(math.cos(0))
print(math.sin(math.radians(90)))
print(math.log(10))
# Output:
# 1.0
# 1.0
# 2.302585092994046


# 12. Roll a dice 10 
import random
dice = []
for i in range(10):
    dice.append(random.randint(1, 6))
print(dice)
# Output: [3, 6, 2, 1, 4, 5, 6, 2, 3, 1]


# 13. Days left for next birthday
import datetime
today = datetime.date.today()
birthday = datetime.date(2026, 7, 16)
if birthday < today:
    birthday = datetime.date(today.year + 1, 7, 16)
print((birthday - today).days,"days")
# Output: 222 days


# 14. Add 30 days to a date
import datetime
d= datetime.datetime.strptime("2022-05-15", "%Y-%m-%d")
new_date = d + datetime.timedelta(days=30)
print(new_date.date())
# Output: 2022-06-14


# 15. Create folder named 'backup'
import os
os.mkdir("backup")

# 16. Dictionary to JSON
import json
dict_data = {"course": "Python", "level": "Beginner"}
json_data = json.dumps(dict_data)
print(json_data)
# Output: {"course": "Python", "level": "Beginner"}


# 17. Extract digits using regex
import re
text = "Order123Amount450"
digits = re.findall(r'\d+', text)
print(digits)
# Output: ['123', '450']


# 18. Check if string starts with 'Hello'
import re
text = "Hello World"
if re.match(r"^Hello", text):
    print("Starts with Hello")
# Output: Starts with Hello


# 19. Mean, Median, 
import statistics
nums = [1, 2, 3, 3, 4, 5]
print(statistics.mean(nums))
print(statistics.median(nums))
print(statistics.mode(nums))
# Output:
# 3
# 3.0
# 3


# 20. Measure execution time of loop
import time
start = time.time()
for i in range(1000000):
    pass
end = time.time()
print(end - start)
# Output: 0.08586692810058976
