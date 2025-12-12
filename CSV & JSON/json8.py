'''8. Print all user names from JSON list'''

data = {'users': [{'id':1,'name':'Alex'}, {'id':2,'name':'Mia'}]}

for user in data['users']:
    print(user['name'])

'''
Output:
Alex
Mia
'''