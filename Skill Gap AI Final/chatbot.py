import json
import re
from datetime import datetime

class SkillAnalysisChatbot:
    def __init__(self):
        self.analysis_data = None
        self.conversation_history = []

    def set_analysis_data(self, analysis_data):
        """Set the analysis data for the chatbot to reference"""
        self.analysis_data = analysis_data

    def get_response(self, user_message):
        """Generate a response based on the user's message and analysis data"""
        if not self.analysis_data:
            return "I don't have access to your skill analysis data yet. Please run an analysis first."

        user_message = user_message.lower().strip()
        self.conversation_history.append({"user": user_message, "timestamp": datetime.now()})

        # Check for greetings
        if self._is_greeting(user_message):
            return self._get_greeting_response()

        # Check for questions about skills
        if any(word in user_message for word in ['skill', 'skills', 'competenc', 'expertise']):
            return self._get_skills_response(user_message)

        # Check for questions about match percentage
        if any(word in user_message for word in ['match', 'percentage', 'rate', 'score']):
            return self._get_match_response(user_message)

        # Check for questions about missing skills
        if any(word in user_message for word in ['missing', 'lack', 'need', 'gap', 'improve']):
            return self._get_missing_skills_response(user_message)

        # Check for questions about recommendations
        if any(word in user_message for word in ['recommend', 'suggest', 'learn', 'study', 'priority']):
            return self._get_recommendations_response(user_message)

        # Check for questions about resume vs job description
        if any(word in user_message for word in ['compare', 'comparison', 'resume', 'job']):
            return self._get_comparison_response(user_message)

        # Default response
        return self._get_default_response()

    def _is_greeting(self, message):
        """Check if the message is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'greetings']
        return any(greeting in message for greeting in greetings)

    def _get_greeting_response(self):
        """Generate a greeting response"""
        match_percentage = self.analysis_data.get('analysis', {}).get('match_percentage', 0)
        greeting = f"Hello! I'm your SkillGapAI assistant. I can help you understand your skill analysis results. "

        if match_percentage >= 80:
            greeting += "Great job! You have a strong match with the job requirements. What would you like to know more about?"
        elif match_percentage >= 60:
            greeting += "You have a decent match, but there are some areas to improve. What specific aspect would you like to explore?"
        else:
            greeting += "There's room for improvement in your skill match. Let me help you understand what you need to work on."

        return greeting

    def _get_skills_response(self, message):
        """Generate response about skills"""
        analysis = self.analysis_data.get('analysis', {})
        resume_skills = self.analysis_data.get('resume_skills', {})
        jd_skills = self.analysis_data.get('jd_skills', {})

        if 'technical' in message or 'tech' in message:
            resume_tech = resume_skills.get('technical', [])
            jd_tech = jd_skills.get('technical', [])
            return f"You have {len(resume_tech)} technical skills in your resume: {', '.join(resume_tech[:5])}{'...' if len(resume_tech) > 5 else ''}. The job requires {len(jd_tech)} technical skills."

        elif 'soft' in message:
            resume_soft = resume_skills.get('soft', [])
            jd_soft = jd_skills.get('soft', [])
            return f"You have {len(resume_soft)} soft skills: {', '.join(resume_soft[:5])}{'...' if len(resume_soft) > 5 else ''}. The job requires {len(jd_soft)} soft skills."

        else:
            total_resume = len(resume_skills.get('technical', [])) + len(resume_skills.get('soft', []))
            total_jd = len(jd_skills.get('technical', [])) + len(jd_skills.get('soft', []))
            return f"You have {total_resume} total skills in your resume, while the job requires {total_jd} skills. You have {analysis.get('summary', {}).get('matched_count', 0)} matching skills."

    def _get_match_response(self, message):
        """Generate response about match percentage"""
        analysis = self.analysis_data.get('analysis', {})
        match_percentage = analysis.get('match_percentage', 0)

        response = f"Your overall skill match is {match_percentage:.1f}%. "

        if match_percentage >= 90:
            response += "Excellent! You're very well-qualified for this role."
        elif match_percentage >= 80:
            response += "Strong match! You have most of the required skills."
        elif match_percentage >= 70:
            response += "Good match, but there are some skills you should develop."
        elif match_percentage >= 60:
            response += "Decent match. Focus on the missing skills to improve your chances."
        else:
            response += "There's significant room for improvement. Consider upskilling in the key areas."

        return response

    def _get_missing_skills_response(self, message):
        """Generate response about missing skills"""
        analysis = self.analysis_data.get('analysis', {})
        missing = analysis.get('missing', {})

        missing_technical = missing.get('technical', [])
        missing_soft = missing.get('soft', [])

        if not missing_technical and not missing_soft:
            return "Great news! You don't appear to be missing any major skills for this role."

        response = "Here are the skills you should focus on developing:\n\n"

        if missing_technical:
            response += f"**Missing Technical Skills ({len(missing_technical)}):**\n"
            for skill in missing_technical[:5]:
                response += f"• {skill}\n"
            if len(missing_technical) > 5:
                response += f"• ... and {len(missing_technical) - 5} more\n"

        if missing_soft:
            response += f"\n**Missing Soft Skills ({len(missing_soft)}):**\n"
            for skill in missing_soft[:5]:
                response += f"• {skill}\n"
            if len(missing_soft) > 5:
                response += f"• ... and {len(missing_soft) - 5} more\n"

        response += "\nI recommend starting with the technical skills as they are often the highest priority for employers."

        return response

    def _get_recommendations_response(self, message):
        """Generate response about recommendations"""
        analysis = self.analysis_data.get('analysis', {})

        # High priority recommendations
        missing_technical = analysis.get('missing', {}).get('technical', [])[:3]
        missing_soft = analysis.get('missing', {}).get('soft', [])[:2]

        # Medium priority (partially matched)
        partial_technical = [item.get('jd_skill', '') for item in analysis.get('partially_matched', {}).get('technical', [])][:2]
        partial_soft = [item.get('jd_skill', '') for item in analysis.get('partially_matched', {}).get('soft', [])][:2]

        response = "**My recommendations for you:**\n\n"

        response += "**🔴 HIGH PRIORITY - Learn these first:**\n"
        for skill in missing_technical:
            response += f"• {skill} (Technical - Critical)\n"
        for skill in missing_soft:
            response += f"• {skill} (Soft Skill - Important)\n"

        if partial_technical or partial_soft:
            response += "\n**🟡 MEDIUM PRIORITY - Strengthen these:**\n"
            for skill in partial_technical:
                response += f"• {skill} (Build on existing technical knowledge)\n"
            for skill in partial_soft:
                response += f"• {skill} (Enhance your soft skills)\n"

        response += "\n**💡 Pro tip:** Start with online courses on platforms like Coursera, Udemy, or LinkedIn Learning. Many offer certificates that you can add to your resume."

        return response

    def _get_comparison_response(self, message):
        """Generate response comparing resume vs job description"""
        resume_skills = self.analysis_data.get('resume_skills', {})
        jd_skills = self.analysis_data.get('jd_skills', {})
        analysis = self.analysis_data.get('analysis', {})

        resume_tech_count = len(resume_skills.get('technical', []))
        resume_soft_count = len(resume_skills.get('soft', []))
        jd_tech_count = len(jd_skills.get('technical', []))
        jd_soft_count = len(jd_skills.get('soft', []))

        response = "**Resume vs Job Description Comparison:**\n\n"
        response += f"**Technical Skills:**\n"
        response += f"• Your resume: {resume_tech_count} skills\n"
        response += f"• Job requires: {jd_tech_count} skills\n"
        response += f"• Gap: {max(0, jd_tech_count - resume_tech_count)} missing\n\n"

        response += f"**Soft Skills:**\n"
        response += f"• Your resume: {resume_soft_count} skills\n"
        response += f"• Job requires: {jd_soft_count} skills\n"
        response += f"• Gap: {max(0, jd_soft_count - resume_soft_count)} missing\n\n"

        matched_count = analysis.get('summary', {}).get('matched_count', 0)
        total_resume = resume_tech_count + resume_soft_count
        total_jd = jd_tech_count + jd_soft_count

        response += f"**Overall:** {matched_count} out of {total_jd} required skills matched ({matched_count/max(total_jd, 1)*100:.1f}%)"

        return response

    def _get_default_response(self):
        """Generate a default response when the query doesn't match specific patterns"""
        responses = [
            "I can help you understand your skill analysis results. Try asking about your match percentage, missing skills, or recommendations!",
            "I'm here to help with your skill gap analysis. What would you like to know about your results?",
            "Feel free to ask me about your skills, match percentage, missing competencies, or upskilling recommendations."
        ]

        return responses[len(self.conversation_history) % len(responses)]