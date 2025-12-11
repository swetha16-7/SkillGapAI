'''
RESUME WORD COUNTER
Accept a paragraph of resume text.
Count total words.
Count unique words.
Identify the most repeated word.
Display results.
'''
text = 'Experienced Full Stack Web Developer with over 5 years of experience in WordPress custom theme building and editing. Proficient in web technologies and WordPress platform, with expertise in Elementor, WPBakery, and similar plugins. Known for attention to detail and excellent communication skills.'
words = text.lower().split()
print("Total words:",len(words))
print("unique_words:",len(set(words)))
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1

most_repeated = max(freq, key=freq.get)
print("Most repeated word:", most_repeated)

Output:
Total words: 42
unique_words: 34
Most repeated word: and
