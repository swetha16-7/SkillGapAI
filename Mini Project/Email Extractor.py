'''SIMPLE EMAIL EXTRACTOR (NO REGEX)
Input a text block.
Find the word containing “@”.
Print the extracted email.
If not found → print “No email detected.”'''

texts = [
    "My email is john@gmail.com",
    "Contact: ram@yahoo.com",
    "No email here",
    "Support mail: help@company.com",
    "Reach us at info@service.in"
]

for text in texts:
    words = text.split()
    email = ""
    for w in words:
        if "@" in w:
            email = w
            break
    
    if email != "":
        print("Email found:", email)
    else:
        print("No email detected.")
