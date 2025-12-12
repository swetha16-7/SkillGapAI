'''1.Convert the JSON string {'name': 'Alex', 'age': 22, 'city': 'Chennai'} into a Python dictionary.'''

import json
json_str = "{'name': 'Alex', 'age': 22, 'city': 'Chennai'}"
json_str = json_str.replace("'", '"')  
data = json.loads(json_str)
print(data)

'''
Output:
{'name': 'Alex', 'age': 22, 'city': 'Chennai'}
'''