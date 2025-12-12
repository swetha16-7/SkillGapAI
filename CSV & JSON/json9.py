'''9. Add key 'country':'India' and convert to JSON'''
import json

data = {'name': 'Sam', 'age': 28}

data['country'] = 'India'

json_str = json.dumps(data)
print(json_str)

'''
Output:
{"name": "Sam", "age": 28, "country": "India"}
'''