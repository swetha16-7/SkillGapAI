'''6. Update dictionary and convert to JSON'''

import json

data = {'name': 'Raj', 'age': 45}

data['age'] = 50   # update age

json_str = json.dumps(data)
print(json_str)

'''
Output:
{"name": "Raj", "age": 50}
'''