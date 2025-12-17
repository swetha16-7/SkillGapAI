text = "PythonProgramming"
print(text[6:])          # Output: Programming

s = "Hello Python Hello World"
print(s.count("Hello"))  # Output: 2

word = "Development"
print(word[::-1])        # Output: tnemepoleveD

sentence = "Python is awesome"
if "Python" in sentence:
    sentence = sentence.replace("awesome", "powerful")
print(sentence)          # Output: Python is powerful

text = "aaabbbccaa"
print(text.count("aa"))  # Output: 2

email = "username@example.com"
username, domain = email.split("@")
print(username, domain)  # Output: username example.com

line = "The price is 1500 rupees"
for ch in line:
    if ch.isdigit():
        print(ch, end="")
print()                  # Output: 1500

words = "python-is-simple-and-powerful"
words = words.replace("-", " ")
print(words)             # Output: python is simple and powerful

text = "hello123world45python"
for ch in text:
    if ch.isalpha():
        print(ch, end="")
print()                  # Output: helloworldpython

text = "Mississippi"
seen = ""

for ch in text:
    if ch in seen:
        print(ch)    # Output: s
        break
    seen += ch
