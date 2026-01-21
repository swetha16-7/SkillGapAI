try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence_transformers not available. Install it with: pip install sentence-transformers")

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SkillGapAnalyzer:
    def __init__(self):
        self.model = None
        self.similarity_threshold = 0.7
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                # Load BERT-based model for semantic similarity
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                print("BERT model loaded successfully for semantic matching.")
            except Exception as e:
                print(f"Warning: Could not load SentenceTransformer model: {e}")
                print("Using basic matching without semantic similarity.")
                self.model = None
        else:
            print("Warning: SentenceTransformer not available. Using basic matching.")
    
    def analyze(self, resume_skills, jd_skills):
        """Analyze skill gap between resume and job description"""
        resume_tech = set(skill.lower() for skill in resume_skills.get('technical', []))
        resume_soft = set(skill.lower() for skill in resume_skills.get('soft', []))
        
        jd_tech = set(skill.lower() for skill in jd_skills.get('technical', []))
        jd_soft = set(skill.lower() for skill in jd_skills.get('soft', []))
        
        # Exact matches
        matched_tech = resume_tech.intersection(jd_tech)
        matched_soft = resume_soft.intersection(jd_soft)
        
        # Missing skills
        missing_tech = jd_tech - resume_tech
        missing_soft = jd_soft - resume_soft
        
        # Skills in resume but not in JD
        extra_tech = resume_tech - jd_tech
        extra_soft = resume_soft - jd_soft
        
        # Semantic matching for partial matches
        partially_matched_tech = []
        partially_matched_soft = []
        
        if self.model:
            # Technical skills semantic matching
            unmatched_jd_tech = list(missing_tech)
            unmatched_resume_tech = list(extra_tech)
            
            if unmatched_jd_tech and unmatched_resume_tech:
                jd_embeddings = self.model.encode(unmatched_jd_tech)
                resume_embeddings = self.model.encode(unmatched_resume_tech)
                
                similarity_matrix = cosine_similarity(jd_embeddings, resume_embeddings)
                
                for i, jd_skill in enumerate(unmatched_jd_tech):
                    max_sim_idx = np.argmax(similarity_matrix[i])
                    max_similarity = similarity_matrix[i][max_sim_idx]
                    
                    if 0.5 <= max_similarity < 0.85:  # Partial match threshold
                        resume_skill = unmatched_resume_tech[max_sim_idx]
                        partially_matched_tech.append({
                            'jd_skill': jd_skill.title(),
                            'resume_skill': resume_skill.title(),
                            'similarity': float(max_similarity)
                        })
                        # Remove from missing/extra lists
                        missing_tech.discard(jd_skill)
                        extra_tech.discard(resume_skill)
            
            # Soft skills semantic matching
            unmatched_jd_soft = list(missing_soft)
            unmatched_resume_soft = list(extra_soft)
            
            if unmatched_jd_soft and unmatched_resume_soft:
                jd_embeddings = self.model.encode(unmatched_jd_soft)
                resume_embeddings = self.model.encode(unmatched_resume_soft)
                
                similarity_matrix = cosine_similarity(jd_embeddings, resume_embeddings)
                
                for i, jd_skill in enumerate(unmatched_jd_soft):
                    max_sim_idx = np.argmax(similarity_matrix[i])
                    max_similarity = similarity_matrix[i][max_sim_idx]
                    
                    if 0.5 <= max_similarity < 0.85:
                        resume_skill = unmatched_resume_soft[max_sim_idx]
                        partially_matched_soft.append({
                            'jd_skill': jd_skill.title(),
                            'resume_skill': resume_skill.title(),
                            'similarity': float(max_similarity)
                        })
                        missing_soft.discard(jd_skill)
                        extra_soft.discard(resume_skill)
        
        # Calculate match percentage
        total_jd_skills = len(jd_tech) + len(jd_soft)
        total_matched = len(matched_tech) + len(matched_soft)
        
        match_percentage = (total_matched / total_jd_skills * 100) if total_jd_skills > 0 else 0
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched': {
                'technical': [skill.title() for skill in matched_tech],
                'soft': [skill.title() for skill in matched_soft]
            },
            'partially_matched': {
                'technical': partially_matched_tech,
                'soft': partially_matched_soft
            },
            'missing': {
                'technical': [skill.title() for skill in missing_tech],
                'soft': [skill.title() for skill in missing_soft]
            },
            'extra': {
                'technical': [skill.title() for skill in extra_tech],
                'soft': [skill.title() for skill in extra_soft]
            },
            'summary': {
                'total_resume_skills': len(resume_tech) + len(resume_soft),
                'total_jd_skills': total_jd_skills,
                'matched_count': total_matched,
                'missing_count': len(missing_tech) + len(missing_soft)
            }
        }
