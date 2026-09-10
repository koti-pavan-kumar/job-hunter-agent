"""
Resume Generator - Follows Pavan's Resume Creation Methodology
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
import re

from .config import config, RESUMES_DIR

class ResumeGenerator:
    """Generate ATS-optimized, tailored resumes following methodology rules"""
    
    def __init__(self):
        self.profile = config.personal_profile
        self.preferences = config.resume_preferences
        self.bridging_rules = config.bridging_rules
        self.project_guide = config.project_selection_guide
    
    def analyze_job_description(self, job_description: str) -> Dict:
        """Analyze JD and extract key information"""
        analysis = {
            "required_skills": [],
            "preferred_skills": [],
            "exact_phrases": [],
            "soft_skills": [],
            "company_values": [],
            "role_type": "unknown",
            "fit_score": 5
        }
        
        # Extract skills
        technical_skills = [
            "python", "java", "javascript", "typescript", "c++", "c", "sql",
            "machine learning", "deep learning", "nlp", "natural language processing",
            "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
            "pandas", "numpy", "data analysis", "data science", "ai", "artificial intelligence",
            "ml", "statistics", "data visualization", "tableau", "power bi",
            "html", "css", "react", "node.js", "django", "flask", "fastapi",
            "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
            "sql", "mongodb", "postgresql", "mysql", "rest api", "graphql",
            "langchain", "llm", "genai", "generative ai", "agentic ai",
            "rag", "vector database", "embedding", "fine-tuning"
        ]
        
        description_lower = job_description.lower()
        
        for skill in technical_skills:
            if skill in description_lower:
                analysis["required_skills"].append(skill)
        
        # Detect role type
        role_keywords = {
            "Data Analyst": ["data analyst", "data analysis", "analytics", "reporting", "dashboard"],
            "ML Engineer": ["ml engineer", "machine learning engineer", "ml engineer"],
            "GenAI/LLM": ["genai", "generative ai", "llm", "large language model", "agentic", "langchain"],
            "SWE": ["software engineer", "swe", "backend", "frontend", "full stack"],
            "Healthcare AI": ["healthcare", "medical", "clinical", "patient", "health"],
            "Data Engineering": ["data engineer", "etl", "data pipeline", "data warehouse"],
            "Computer Vision": ["computer vision", "image processing", "opencv", "yolo"]
        }
        
        for role_type, keywords in role_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    analysis["role_type"] = role_type
                    break
        
        return analysis
    
    def select_projects_for_role(self, role_type: str) -> List[str]:
        """Select which projects to include based on role type"""
        return self.project_guide.role_project_order.get(role_type, ["NovaGen", "Avotangi", "Bluestock N100 Capstone"])
    
    def apply_honest_bridging(self, skills: List[str]) -> Tuple[List[str], List[str]]:
        """Apply honest bridging to skills"""
        bridged_skills = []
        bridging_notes = []
        
        for skill in skills:
            skill_lower = skill.lower()
            
            # Check if skill is genuinely held
            is_genuine = False
            for genuine in self.bridging_rules.genuine_skills:
                if genuine.lower() in skill_lower or skill_lower in genuine.lower():
                    is_genuine = True
                    break
            
            if is_genuine:
                bridged_skills.append(skill)
            else:
                # Check if skill needs bridging
                for bridged, note in self.bridging_rules.bridging_skills.items():
                    if bridged.lower() in skill_lower or skill_lower in bridged.lower():
                        bridged_skills.append(f"{skill} ({note.split('—')[0].strip()})")
                        bridging_notes.append(f"{skill}: {note}")
                        break
                else:
                    # Skill not found in bridging rules, add with learning tag
                    bridged_skills.append(f"{skill} (learning)")
                    bridging_notes.append(f"{skill}: learning — not previously encountered")
        
        return bridged_skills, bridging_notes
    
    def generate_tailored_resume(self, job_title: str, company_name: str, job_description: str) -> Dict:
        """Generate a tailored resume for a specific job"""
        
        # Step 1: Analyze JD
        analysis = self.analyze_job_description(job_description)
        
        # Step 2: Check fit score
        fit_score = self._calculate_fit_score(analysis)
        
        # Step 3: Select projects
        selected_projects = self.select_projects_for_role(analysis["role_type"])
        
        # Step 4: Build resume content
        resume_content = self._build_resume_content(
            job_title, company_name, analysis, selected_projects
        )
        
        # Step 5: Generate cover letter
        cover_letter = self._generate_cover_letter(
            job_title, company_name, analysis, selected_projects
        )
        
        return {
            "resume_content": resume_content,
            "cover_letter": cover_letter,
            "analysis": analysis,
            "fit_score": fit_score,
            "bridging_notes": resume_content.get("bridging_notes", [])
        }
    
    def _calculate_fit_score(self, analysis: Dict) -> int:
        """Calculate fit score (1-10)"""
        # Simple scoring based on skill match
        score = 5  # Base score
        
        # Add points for matched skills
        score += min(len(analysis["required_skills"]), 5)
        
        # Determine role type match
        if analysis["role_type"] != "unknown":
            score += 2
        
        return min(score, 10)
    
    def _build_resume_content(self, job_title: str, company_name: str, 
                              analysis: Dict, selected_projects: List[str]) -> Dict:
        """Build resume content following methodology"""
        
        # Build objective
        objective = self._build_objective(job_title, company_name, analysis)
        
        # Build skills section
        skills_section = self._build_skills_section(analysis)
        
        # Build projects section
        projects_section = self._build_projects_section(selected_projects, analysis["role_type"])
        
        # Build experience section
        experience_section = self._build_experience_section(analysis["role_type"])
        
        # Build achievements section
        achievements_section = self._build_achievements_section()
        
        # Build additional section
        additional_section = self._build_additional_section()
        
        return {
            "name": self.profile.name,
            "contact": f"{self.profile.phone} | {self.profile.email} | {self.profile.linkedin_url} | {self.profile.github_url}",
            "objective": objective,
            "education": self._build_education_section(),
            "technical_skills": skills_section,
            "projects": projects_section,
            "experience": experience_section,
            "achievements": achievements_section,
            "additional": additional_section,
            "bridging_notes": []
        }
    
    def _build_objective(self, job_title: str, company_name: str, analysis: Dict) -> str:
        """Build objective section (3-5 sentences)"""
        
        # Get top skills from JD
        top_skills = analysis["required_skills"][:4]
        skills_text = ", ".join(top_skills) if top_skills else "Python, Machine Learning, Data Analysis"
        
        objective = f"Motivated {self.profile.btech['degree'].split('—')[1].strip()} student at {self.profile.btech['institution'].split(',')[0]} "
        objective += f"seeking a {job_title} position at {company_name} to apply my skills in {skills_text}. "
        objective += f"With hands-on experience in production-grade projects including LLM systems, ensemble ML, and computer vision, "
        objective += f"I bring both technical depth and a commitment to continuous learning."
        
        return objective
    
    def _build_education_section(self) -> str:
        """Build education section"""
        education = f"B.Tech — {self.profile.btech['degree'].split('—')[1].strip()}\n"
        education += f"{self.profile.btech['institution']} | {self.profile.btech['years']}\n"
        education += f"CGPA: {self.profile.btech['cgpa']} | {self.profile.btech['rank']}\n\n"
        
        education += f"Diploma — {self.profile.diploma['degree'].split('—')[1].strip()}\n"
        education += f"{self.profile.diploma['institution']} | {self.profile.diploma['years']}\n"
        education += f"CGPA: {self.profile.diploma['cgpa']}"
        
        return education
    
    def _build_skills_section(self, analysis: Dict) -> str:
        """Build technical skills section"""
        # Group skills by category
        categories = {
            "ML & AI": [],
            "LLMs & GenAI": [],
            "Data Engineering": [],
            "Software Engineering": [],
            "Computer Vision": [],
            "Tools": []
        }
        
        # Categorize skills
        for skill in analysis["required_skills"]:
            if skill in ["machine learning", "deep learning", "scikit-learn", "random forest", "gradient boosting"]:
                categories["ML & AI"].append(skill)
            elif skill in ["langchain", "llm", "genai", "generative ai", "agentic ai", "rag", "vector database"]:
                categories["LLMs & GenAI"].append(skill)
            elif skill in ["pandas", "numpy", "sql", "data analysis", "data science"]:
                categories["Data Engineering"].append(skill)
            elif skill in ["python", "java", "javascript", "fastapi", "django", "flask"]:
                categories["Software Engineering"].append(skill)
            elif skill in ["computer vision", "opencv", "yolo"]:
                categories["Computer Vision"].append(skill)
            elif skill in ["git", "docker", "aws", "linux"]:
                categories["Tools"].append(skill)
        
        # Add base skills if categories are empty
        if not categories["ML & AI"]:
            categories["ML & AI"] = ["Scikit-learn", "Random Forest", "Gradient Boosting", "Ensemble Methods"]
        if not categories["LLMs & GenAI"]:
            categories["LLMs & GenAI"] = ["LangChain", "LLaMA 3.3 70B", "Prompt Engineering"]
        if not categories["Data Engineering"]:
            categories["Data Engineering"] = ["Pandas", "NumPy", "SQLite", "ETL Pipelines"]
        if not categories["Software Engineering"]:
            categories["Software Engineering"] = ["Python", "Java", "FastAPI", "REST APIs"]
        if not categories["Computer Vision"]:
            categories["Computer Vision"] = ["YOLO11s", "OpenCV", "Real-time Inference"]
        if not categories["Tools"]:
            categories["Tools"] = ["Git & GitHub", "VS Code", "Jupyter Notebook"]
        
        # Build skills text
        skills_text = ""
        for category, skills in categories.items():
            if skills:
                skills_text += f"{category}: {', '.join(skills)}\n"
        
        return skills_text
    
    def _build_projects_section(self, selected_projects: List[str], role_type: str) -> List[Dict]:
        """Build projects section"""
        projects = []
        
        # Project database
        project_db = {
            "Avotangi": {
                "title": "Avotangi — Production LLM WhatsApp Chatbot",
                "date": "Dec 2025",
                "tech_stack": "LangChain + LLaMA 3.3 70B + FastAPI + Twilio + n8n",
                "github": "github.com/koti-pavan-kumar/avotangi",
                "bullets": [
                    "Built production WhatsApp AI chatbot for luxury footwear brand with 55+ products",
                    "Achieved 99% reliability with 2-3 second latency, deployed in 3 days",
                    "Implemented AI agent with tool calling, conversation memory, and context-aware reasoning",
                    "Developed FastAPI backend with webhook-based real-time processing"
                ]
            },
            "NovaGen": {
                "title": "NovaGen — Health Risk Classifier",
                "date": "Jun 2026",
                "tech_stack": "Python · Scikit-learn · Ensemble ML",
                "github": "github.com/koti-pavan-kumar/novagen-health-classifier",
                "bullets": [
                    "Processed 9,800 health records with 22 features (physiological, lifestyle, medical history)",
                    "Benchmarked 5 models: Logistic Regression (82.8%), KNN (88.3%), Gradient Boosting (94.9%), Voting Classifier (93.1%), Random Forest (95.8%)",
                    "Selected Recall as primary metric — minimise false negatives in high-risk patient detection",
                    "Final: Random Forest (200 estimators) — 95.8% Recall, 93.7% Accuracy"
                ]
            },
            "Bluestock N100 Capstone": {
                "title": "Bluestock N100 Financial Intelligence Platform",
                "date": "Jun 2026",
                "tech_stack": "Python, Pandas, NumPy, SQLite, SQLAlchemy, Matplotlib, Seaborn, Plotly, Streamlit, Power BI, Git/GitHub, pytest",
                "github": "github.com/koti-pavan-kumar/bluestock-mf-capstone",
                "bullets": [
                    "Processed 87,000+ rows real AMFI data through automated Python ETL pipeline into queryable SQLite database",
                    "Built 16-rule data quality validation engine with severity tiers for production-grade data integrity",
                    "Implemented 270+ automated tests (pytest) — TDD with systematic QA sweeps and methodical root-cause debugging",
                    "Deployed live Streamlit analytics dashboard covering industry AUM trends, investor demographics, and SIP market trends"
                ]
            },
            "ShopSmart": {
                "title": "ShopSmart — E-Commerce Purchase Predictor",
                "date": "May 2026",
                "tech_stack": "Python · Decision Tree · GridSearchCV · Scikit-learn",
                "github": "github.com/koti-pavan-kumar/shopsmart-ml",
                "bullets": [
                    "Processed 12,330 e-commerce sessions with 18 features",
                    "Handled 84.5% class imbalance using class_weight balancing",
                    "Applied GridSearchCV (5-fold CV): pre-pruning (max_depth=2) + post-pruning (CCP alpha)",
                    "Improved F1-Score from 57% baseline to 67.6% (+18.4%)"
                ]
            },
            "AI Blind Assist": {
                "title": "AI Blind Assistance System",
                "date": "2025",
                "tech_stack": "Python · YOLO11s · OpenCV · Multilingual TTS",
                "github": "github.com/koti-pavan-kumar/ai-blind-assistance-system",
                "bullets": [
                    "Achieved real-time object detection at 26 FPS on standard laptop CPU",
                    "Implemented multilingual TTS: English, Telugu, Hindi",
                    "Applied CLAHE enhancement and danger priority logic",
                    "Selected YOLO11s over YOLO11m (FPS dropped from 26 to 6)"
                ]
            }
        }
        
        # Add selected projects
        for project_name in selected_projects:
            # Remove role type annotations
            clean_name = project_name.split(" (")[0]
            if clean_name in project_db:
                projects.append(project_db[clean_name])
        
        return projects
    
    def _build_experience_section(self, role_type: str) -> Dict:
        """Build experience section"""
        experience = {
            "company": "Bluestock Fintech Pvt. Ltd.",
            "role": "Data Analyst Intern (Remote)",
            "duration": "Jun 2026 – Present",
            "type": "internship",
            "bullets": []
        }
        
        # Role-specific framing
        if role_type in ["Data Analyst", "Data Engineering", "BI/Dashboard", "Fintech/Quant"]:
            experience["bullets"] = [
                "Leading N100 Financial Intelligence Platform for 92 Nifty 100 companies",
                "Built 16-rule data quality validation engine with severity tiers",
                "Implemented 270+ automated tests (pytest) — TDD with systematic QA",
                "Processing 87,000+ rows real AMFI data through automated ETL pipeline"
            ]
        elif role_type == "SWE/Software Engineering":
            experience["bullets"] = [
                "Implemented 270+ automated tests (pytest) — TDD with systematic QA",
                "Built production-grade data engineering pipeline with 12-table schema",
                "Applied systematic debugging and root-cause analysis",
                "Maintained Git version control and structured documentation"
            ]
        elif role_type == "GenAI/LLM":
            experience["bullets"] = [
                "Developed AI-assisted analytics workflows using LLM-based report generation",
                "Built NLP commentary system for automated investment insights",
                "Integrated LLM capabilities for natural language data querying",
                "Applied prompt engineering for financial analysis automation"
            ]
        else:
            experience["bullets"] = [
                "Leading N100 Financial Intelligence Platform for 92 Nifty 100 companies",
                "Built 16-rule data quality validation engine with severity tiers",
                "Implemented 270+ automated tests (pytest) — TDD with systematic QA",
                "Processing 87,000+ rows real AMFI data through automated ETL pipeline"
            ]
        
        return experience
    
    def _build_achievements_section(self) -> str:
        """Build achievements/certifications section"""
        achievements = [
            "Amazon ML Summer School 2026 — Shortlisted nationally for SOP round",
            "Flipkart GRiD 8.0 — Round 2 Qualifier | 1,04,547 registrations nationally",
            "Deloitte Australia Data Analytics Job Simulation — Feb 2026",
            "OOP Through Java — Grade A (9.0/10) | B.Tech Semester 1",
            "DSA: 100+ problems solved (LeetCode, GeeksforGeeks)"
        ]
        
        return "\n".join(achievements)
    
    def _build_additional_section(self) -> str:
        """Build additional section"""
        return f"Languages: English, Telugu, Hindi\nGitHub: {self.profile.github_url}\nLinkedIn: {self.profile.linkedin_url}"
    
    def _generate_cover_letter(self, job_title: str, company_name: str, 
                               analysis: Dict, selected_projects: List[str]) -> str:
        """Generate cover letter following methodology"""
        
        # Para 1: Hook
        hook = f"As a {self.profile.btech['degree'].split('—')[1].strip()} student who has built production-grade LLM systems and ensemble ML models, "
        hook += f"I am excited about the {job_title} opportunity at {company_name}."
        
        # Para 2: Primary proof point
        primary_project = selected_projects[0] if selected_projects else "NovaGen"
        primary_proof = self._get_project_proof(primary_project, analysis["role_type"])
        
        # Para 3: Secondary proof
        secondary_project = selected_projects[1] if len(selected_projects) > 1 else "Avotangi"
        secondary_proof = self._get_project_proof(secondary_project, analysis["role_type"])
        
        # Para 4: Credibility signals
        credibility = "My experience includes Amazon ML Summer School shortlisting, Flipkart GRiD Round 2 qualification, "
        credibility += "and current internship at Bluestock Fintech where I've implemented 270+ automated tests."
        
        # Para 5: Why THIS company
        why_company = f"I am particularly drawn to {company_name} because of your commitment to innovation "
        why_company += f"in the technology space. My technical skills align well with your requirements for {job_title}."
        
        # Close
        close = "I would welcome the opportunity to discuss how I can contribute to your team's success."
        
        cover_letter = f"{hook}\n\n{primary_proof}\n\n{secondary_proof}\n\n{credibility}\n\n{why_company}\n\n{close}"
        
        return cover_letter
    
    def _get_project_proof(self, project_name: str, role_type: str) -> str:
        """Get proof points for a project"""
        proofs = {
            "Avotangi": "I built a production WhatsApp AI chatbot achieving 99% reliability with 2-3 second latency, deployed in just 3 days.",
            "NovaGen": "I developed a health risk classifier processing 9,800 patient records with 95.8% Recall using Random Forest ensemble.",
            "Bluestock N100 Capstone": "I built a financial intelligence platform processing 87,000+ rows of real AMFI data with 270+ automated tests.",
            "ShopSmart": "I improved purchase prediction F1-Score from 57% to 67.6% (+18.4%) using advanced ensemble techniques."
        }
        
        return proofs.get(project_name, "I have hands-on experience in production-grade projects.")

# Global instance
resume_generator = ResumeGenerator()
