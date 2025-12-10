'''SKILL FREQUENCY CHECKER

Take a paragraph of resume text.

Take a skill from the user.

Count how many times the skill appears.

Print:
“Skill appears X times.”'''

text = "Managed WordPress development and custom theme creation.Managed multiple large-scale projects, delivering all on time and within budget.Used WordPress, Elementor, WPBakery, and other plugins to build and edit custom themes, improving website performance by 30%.Collaborated with a team of developers, contributing to a 20% increase in team productivity. Used WordPress, Elementor, WPBakery, and other plugins to build and edit custom themes, contributing to a 20% increase in website performance."
skill = "wordpress"
para = text.lower()
para = para.replace(".", " ").replace(",", " ")
para = para.split()
count = 0
for i in para:
    if i == skill:
        count += 1
print("Skill",skill,"appears",count,"times")
