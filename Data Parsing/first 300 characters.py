#2. Read a .txt file and display only the first 300 characters as a preview.
def display_file_preview(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read(300)
            print(content)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")


# Function call
display_file_preview("resume.txt")

