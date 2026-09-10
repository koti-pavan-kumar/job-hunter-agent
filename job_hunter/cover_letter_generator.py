"""
Cover Letter Generator - Follows Pavan's Cover Letter Methodology
"""
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from .config import config, RESUMES_DIR

class CoverLetterGenerator:
    """Generate ATS-optimized cover letters following methodology"""
    
    def __init__(self):
        self.profile = config.personal_profile
        self.preferences = config.resume_preferences
    
    def generate_cover_letter(self, job_title: str, company_name: str, 
                             job_description: str, resume_content: Dict) -> Dict:
        """Generate a tailored cover letter"""
        
        # Analyze JD for cover letter
        analysis = self._analyze_for_cover_letter(job_description)
        
        # Build cover letter following methodology structure
        cover_letter = self._build_cover_letter(
            job_title, company_name, analysis, resume_content
        )
        
        return {
            "cover_letter": cover_letter,
            "format": "docx",  # Rule C: Always .docx format
            "analysis": analysis
        }
    
    def _analyze_for_cover_letter(self, job_description: str) -> Dict:
        """Analyze JD specifically for cover letter"""
        analysis = {
            "company_mission": "",
            "key_requirements": [],
            "company_values": [],
            "specific_technologies": []
        }
        
        # Extract company mission/values
        mission_keywords = ["mission", "vision", "values", "commitment", "dedication"]
        for keyword in mission_keywords:
            if keyword in job_description.lower():
                # Find sentence containing the keyword
                sentences = job_description.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        analysis["company_mission"] = sentence.strip()
                        break
        
        # Extract key requirements
        requirement_keywords = ["required", "must have", "essential", "looking for"]
        for keyword in requirement_keywords:
            if keyword in job_description.lower():
                sentences = job_description.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        analysis["key_requirements"].append(sentence.strip())
        
        return analysis
    
    def _build_cover_letter(self, job_title: str, company_name: str, 
                           analysis: Dict, resume_content: Dict) -> str:
        """Build cover letter following methodology structure"""
        
        # Para 1: Hook (specific and confident, never 'I am writing to apply')
        hook = self._build_hook(job_title, company_name)
        
        # Para 2: Primary proof point with numbers
        primary_proof = self._build_primary_proof(resume_content)
        
        # Para 3: Secondary proof or current internship relevance
        secondary_proof = self._build_secondary_proof(resume_content)
        
        # Para 4: Credibility signals
        credibility = self._build_credibility_signals()
        
        # Para 5: Why THIS company (specific, never generic)
        why_company = self._build_why_company(company_name, analysis)
        
        # Close: Availability + call to action
        close = self._build_close()
        
        # Combine all paragraphs
        cover_letter = f"{hook}\n\n{primary_proof}\n\n{secondary_proof}\n\n{credibility}\n\n{why_company}\n\n{close}"
        
        return cover_letter
    
    def _build_hook(self, job_title: str, company_name: str) -> str:
        """Build hook paragraph - specific and confident"""
        
        # Get top skills from resume
        top_skills = []
        if "technical_skills" in resume_content:
            skills_text = resume_content["technical_skills"]
            if "ML & AI" in skills_text:
                top_skills.append("ensemble ML")
            if "LLMs & GenAI" in skills_text:
                top_skills.append("production LLM systems")
            if "Computer Vision" in skills_text:
                top_skills.append("computer vision")
        
        skills_text = ", ".join(top_skills[:2]) if top_skills else "AI/ML"
        
        hook = f"As a {self.profile.btech['degree'].split('—')[1].strip()} student who has built {skills_text}, "
        hook += f"I am excited about the {job_title} opportunity at {company_name}. "
        hook += f"My experience in production-grade projects demonstrates both technical depth and a commitment to continuous learning."
        
        return hook
    
    def _build_primary_proof(self, resume_content: Dict) -> str:
        """Build primary proof paragraph with numbers"""
        
        # Get the most relevant project
        projects = resume_content.get("projects", [])
        if projects:
            primary_project = projects[0]
            project_name = primary_project.get("title", "").split("—")[0].strip()
            
            # Get proof points based on project
            proof_points = {
                "Avotangi": "I built a production WhatsApp AI chatbot achieving 99% reliability with 2-3 second latency, deployed in just 3 days. The system handles 55+ products with AI agent capabilities including tool calling and conversation memory.",
                "NovaGen": "I developed a health risk classifier processing 9,800 patient records with 22 features, achieving 95.8% Recall using Random Forest ensemble. I selected Recall as the primary metric to minimize false negatives in high-risk patient detection.",
                "Bluestock N100 Capstone": "I built a financial intelligence platform processing 87,000+ rows of real AMFI data through an automated ETL pipeline into a queryable SQLite database. The system includes 16-rule data quality validation and 270+ automated tests.",
                "ShopSmart": "I improved purchase prediction F1-Score from 57% baseline to 67.6% (+18.4%) using advanced ensemble techniques. I handled 84.5% class imbalance and applied GridSearchCV with 5-fold cross-validation."
            }
            
            return proof_points.get(project_name, 
                f"I have hands-on experience in {project_name}, demonstrating both technical skills and problem-solving abilities.")
        
        return "I have hands-on experience in production-grade projects, demonstrating both technical skills and problem-solving abilities."
    
    def _build_secondary_proof(self, resume_content: Dict) -> str:
        """Build secondary proof paragraph"""
        
        # Get experience section
        experience = resume_content.get("experience", {})
        if experience:
            company = experience.get("company", "Bluestock Fintech")
            role = experience.get("role", "Data Analyst Intern")
            
            secondary_proof = f"In my current role as {role} at {company}, "
            secondary_proof += "I have implemented 270+ automated tests using pytest with TDD discipline, "
            secondary_proof += "built a 16-rule data quality validation engine, "
            secondary_proof += "and processed 87,000+ rows of real financial data through automated ETL pipelines."
            
            return secondary_proof
        
        return "In my current internship, I have gained hands-on experience in data analysis, automation, and quality assurance."
    
    def _build_credibility_signals(self) -> str:
        """Build credibility signals paragraph"""
        
        credibility = "My technical credibility is supported by several key achievements:\n"
        credibility += "• Amazon ML Summer School 2026 — Shortlisted nationally for SOP round\n"
        credibility += "• Flipkart GRiD 8.0 — Round 2 Qualifier (1,04,547 registrations nationally)\n"
        credibility += "• Deloitte Australia Data Analytics Job Simulation — Completed with certification\n"
        credibility += "• OOP Through Java — Grade A (9.0/10) in B.Tech Semester 1\n"
        credibility += "• DSA: 100+ problems solved on LeetCode and GeeksforGeeks"
        
        return credibility
    
    def _build_why_company(self, company_name: str, analysis: Dict) -> str:
        """Build why THIS company paragraph (specific, never generic)"""
        
        # Use company mission if available
        if analysis.get("company_mission"):
            why_company = f"I am particularly drawn to {company_name} because of your {analysis['company_mission']}. "
        else:
            why_company = f"I am particularly drawn to {company_name} because of your commitment to innovation "
            why_company += "in the technology space. "
        
        why_company += f"My experience in {self.profile.btech['degree'].split('—')[1].strip()} "
        why_company += f"and hands-on projects in AI/ML aligns well with your requirements for this role. "
        why_company += f"I am confident that my technical skills, combined with my enthusiasm for learning, "
        why_company += f"make me a strong candidate for the {company_name} team."
        
        return why_company
    
    def _build_close(self) -> str:
        """Build closing paragraph"""
        
        close = "I would welcome the opportunity to discuss how I can contribute to your team's success. "
        close += "I am available for an interview at your convenience and can start immediately. "
        close += "Thank you for considering my application."
        
        return close
    
    def save_cover_letter(self, cover_letter: str, job_title: str, company_name: str) -> str:
        """Save cover letter to file"""
        
        # Clean company name for filename
        clean_company = company_name.replace(" ", "_").replace("/", "_")[:20]
        clean_title = job_title.replace(" ", "_").replace("/", "_")[:20]
        date = datetime.now().strftime("%Y%m%d")
        
        filename = f"CoverLetter_{clean_company}_{clean_title}_{date}.txt"
        filepath = RESUMES_DIR / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cover_letter)
        
        return str(filepath)

# Global instance
cover_letter_generator = CoverLetterGenerator()
