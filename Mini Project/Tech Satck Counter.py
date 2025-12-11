'''TECH STACK COUNTER
Input a list of tools/technologies.
Program counts how many items belong to:
Programming Languages
Databases
Frameworks
Print a summary.'''

tech = ["Python","MySQL","React","Java","MongoDB","Django"]
languages = ["Python","Java","C","C++","JavaScript"]
databases = ["MySQL","MongoDB","PostgreSQL","SQLServer"]
frameworks = ["React","Angular","Django","Laravel","Spring"]
lang_count = 0
db_count = 0
fw_count = 0
for t in tech:
    if t in languages:
        lang_count += 1
    elif t in databases:
        db_count += 1
    elif t in frameworks:
        fw_count += 1
print("Languages:", lang_count)
print("Databases:", db_count)
print("Frameworks:", fw_count)


Output:
Languages: 2
Databases: 2
Frameworks: 2
