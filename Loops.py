# 1. Print numbers from 1 to 10
for i in range(1, 11):
    print(i)
'''
Output: 
1 
2
3
4
5
6
7
8
9
10'''
# 2. Print all even numbers from 1 to 20
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
'''Output:
2
4
6
8
10
12
14
16
18
20'''
# 3. Print each character of 'Python'
for ch in "Python":
    print(ch)
# Output:
# P
# y
# t
# h
# o
# n

# 4. Print numbers from 5 down to 1 (while loop)
i = 5
while i >= 1:
    print(i)
    i -= 1
# Output:
# 5 
# 4 
# 3 
# 2 
# 1


# 5. Sum of numbers from 1 to 50
total = 0
for i in range(1, 51):
    total += i
print(total)
# Output: 1275


# 6. Multiplication table of 5
for i in range(1, 11):
    print("5 x", i, "=", 5 * i)
# Output:
# 5 x 1 = 5
# 5 x 2 = 10
# 5 x 3 = 15
# 5 x 4 = 20
# 5 x 5 = 25
# 5 x 6 = 30
# 5 x 7 = 35
# 5 x 8 = 40
# 5 x 9 = 45
# 5 x 10 = 50
 
# 7. Count vowels in 'Programming'
text = "Programming"
count = 0
for ch in text:
    if ch.lower() in "aeiou":
        count += 1
print(count)
# Output: 3


# 8. Reverse the string 'PythonLoops'
text = "PythonLoops"
rev = ""
for ch in text:
    rev = ch + rev
print(rev)
# Output: spooLnohtyP


# 9. Print 1–10, skip 5
for i in range(1, 11):
    if i == 5:
        continue
    print(i)
# Output: 
# 1 
# 2 
# 3 
# 4 
# 6 
# 7 
# 8 
# 9 
# 10


# 10. Print 1–20, stop at 13
for i in range(1, 21):
    if i == 13:
        break
    print(i)
# Output: 
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# 11
# 12

# 11. Check if a number is prime
num = 7
c=0
for i in range(1, num+1):
    if num % i == 0:
        c+=1
if(c==2):
    print("Prime")
# Output: Prime


# 12. Count character frequency in 'mississippi'
text = "mississippi"
for ch in set(text):
    print(ch, text.count(ch))
# Output:
# m 1
# i 4
# s 4
# p 2


# 13. Pattern: *, **, ***, ****, *****
for i in range(1, 6):
    print("*" * i)
# Output:
# *
# **
# ***
# ****
# *****


# 14. Largest digit in 5847361
num = "5847361"
largest = "0"
for digit in num:
    if digit > largest:
        largest = digit
print(largest)
# Output: 8


# 15. Pattern: *****, ****, ***, **, *
for i in range(5, 0, -1):
    print("*" * i)
# Output:
# *****
# ****
# ***
# **
# *
