# 1. Function to print a message
def welcome():
    print("Welcome to Python!")

welcome()
# Output: Welcome to Python!


# 2. Function with parameter (name)
def greet(name):
    print("Hello", name)

greet("Swetha")
# Output: Hello Swetha


# 3. Function to find square of a number
def square(n):
    print(n * n)

square(5)
# Output: 25


# 4. Function to calculate sum of two numbers
def calculate(a, b):
    print(a + b,a-b,a*b)

calculate(10, 2)
# Output: 12 8 20

# 5. Function to print country name
def country(name="India"):
    print("I am from", name)

country()
# Output: I am from India


# 6. Function to find total of list elements
def total(*nums):
    print(sum(nums))

nums=[1, 2, 3, 4]
total(*nums)
# Output: 10


# 7. Function using dictionary
def student_info(**data):
    for key, value in data.items():
        print(key, ":", value)
data={"A": 20, "B": 30, "C": 40}
student_info(**data)
# Output:
# A : 20
# B : 30
# C : 40


# 8. Write a function count_vowels(text) that returns the number of vowels in the string.
def count_vowels(text):
    vowels = 'aeiouAEIOU'
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count
print(count_vowels("Hello World"))
# Output: 3

#9. Write a lambda function to return the cube of a number.
cube = lambda x: x ** 3
print(cube(4))

#output: 64

#10. Write a function unique_letters(text) that returns unique letters in the order they appear.

def unique_letters(text):
    r=[]
    for i in text:
        if i not in r:
            r.append(i)
    print(*r)
unique_letters("mississippi")
# Output: m i s p
