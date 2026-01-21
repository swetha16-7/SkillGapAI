import spacy
import re
from collections import defaultdict

class SkillExtractor:
    def __init__(self):
        try:
            # Try to load spaCy model, fallback to basic if not available
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Using basic extraction.")
            self.nlp = None
        
        self.programming_languages = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'go', 'rust', 'kotlin',
            'swift', 'php', 'ruby', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash',
        }

        # Common technical skills database (excluding programming languages)
        self.technical_skills = {
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'spring', 'asp.net', 'laravel', 'rails', 'jquery', 'bootstrap', 'sass', 'less',
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sqlite', 'redis', 'cassandra',
            'elasticsearch', 'dynamodb', 'neo4j',
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
            'terraform', 'ansible', 'chef', 'puppet', 'linux', 'unix',
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'data analysis',
            # Other Technologies
            'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'devops', 'git',
            'api development', 'web services', 'json', 'xml'
        }
        
        # Common soft skills
        self.soft_skills = {
            'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking',
            'time management', 'project management', 'collaboration', 'adaptability',
            'creativity', 'analytical thinking', 'attention to detail', 'multitasking',
            'negotiation', 'presentation', 'public speaking', 'mentoring', 'coaching'
        }
    
    def extract_skills(self, text):
        """Extract technical and soft skills from text"""
        if not text:
            return {'technical': [], 'soft': []}

        # Normalize text
        text_lower = text.lower()
        text_hash = hash(text_lower) % 10000  # Simple hash for debugging

        print(f"Extracting skills from text (hash: {text_hash}), length: {len(text)}")

        # Extract technical skills
        technical_found = set()
        for skill in self.technical_skills:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                technical_found.add(skill.title())

        # Extract programming languages
        programming_languages_found = set()
        for skill in self.programming_languages:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                programming_languages_found.add(skill.title())

        # Combine programming languages with technical skills for the final output
        all_technical_found = technical_found.union(programming_languages_found)

        # Extract soft skills
        soft_found = set()
        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                soft_found.add(skill.title())

        print(f"Found {len(all_technical_found)} technical skills: {list(all_technical_found)[:5]}...")
        print(f"Found {len(soft_found)} soft skills: {list(soft_found)[:5]}...")
        
        # Use NLP for additional skill extraction if available
        if self.nlp:
            doc = self.nlp(text)
            # Extract noun phrases that might be skills
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower().strip()
                if len(chunk_text.split()) <= 3:  # Skills are usually short phrases
                    # Check if it looks like a skill (contains tech keywords)
                    tech_keywords = ['development', 'programming', 'framework', 'database', 
                                   'tool', 'platform', 'system', 'software', 'language']
                    if any(keyword in chunk_text for keyword in tech_keywords):
                        all_technical_found.add(chunk.text.strip().title())
        
        return {
            'technical': sorted(list(all_technical_found)),
            'soft': sorted(list(soft_found))
        }
