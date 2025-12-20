#10. Clean the extracted text after parsing and display both raw and cleaned versions.

raw_text = """
  This   is   SAMPLE   extracted   TEXT.
  It   contains   EXTRA   spaces   and   Mixed   CASES.
"""

# Display raw text
print("RAW TEXT:")
print(raw_text)

# Clean the text
cleaned_text = raw_text.lower()
cleaned_text = " ".join(cleaned_text.split())

# Display cleaned text
print("CLEANED TEXT:")
print(cleaned_text)
