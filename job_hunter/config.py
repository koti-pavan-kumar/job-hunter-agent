"""
Job Hunter Agent - Configuration with Pavan's Complete Profile
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Dict
import json

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESUMES_DIR = BASE_DIR / "resumes"
LOGS_DIR = BASE_DIR / "logs"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
for dir_path in [DATA_DIR, RESUMES_DIR, LOGS_DIR, TEMPLATES_DIR]:
    dir_path.mkdir(exist_ok=True)

@dataclass
class PersonalProfile:
    """Pavan's complete personal profile"""
    name: str = "Pavan Kumar Koti"
    email: str = "kotipavankumar12@gmail.com"
    phone: str = "+91 7893600187"
    location: str = "Ongole, Andhra Pradesh, India"
    linkedin_url: str = "linkedin.com/in/pavan-kumar-koti-200b4438b"
    github_url: str = "github.com/koti-pavan-kumar/"
    portfolio_url: str = ""
    
    # Education
    btech: dict = None
    diploma: dict = None
    
    # Career goals
    career_goals: str = "Move from technical roles into leadership and people management"
    seeking: str = "ML/AI/Data Science/SWE internships and entry-level roles"
    open_to_relocate: List[str] = None
    
    def __post_init__(self):
        if self.btech is None:
            self.btech = {
                "degree": "B.Tech — Artificial Intelligence & Machine Learning",
                "institution": "Pace Institute of Technology & Sciences, Ongole, AP",
                "university": "JNTUK Kakinada",
                "years": "2025–2028",
                "cgpa": "8.2/10",
                "rank": "Top 20% of class",
                "roll_no": "25KQ5A6101"
            }
        if self.diploma is None:
            self.diploma = {
                "degree": "Diploma — Computer Science & Engineering",
                "institution": "Rise Krishna Sai Polytechnic College, Ongole, AP",
                "years": "2022–2025",
                "cgpa": "9.1/10"
            }
        if self.open_to_relocate is None:
            self.open_to_relocate = ["Bangalore", "Hyderabad", "Chennai", "Pune"]

@dataclass
class Project:
    """Project details"""
    title: str = ""
    description: str = ""
    tech_stack: str = ""
    github_url: str = ""
    live_url: str = ""
    bullets: List[str] = None
    role_types: List[str] = None  # Which role types this project is best for
    
    def __post_init__(self):
        if self.bullets is None:
            self.bullets = []
        if self.role_types is None:
            self.role_types = []

@dataclass
class Experience:
    """Work experience"""
    company: str = ""
    role: str = ""
    duration: str = ""
    type: str = ""  # internship, full-time, simulation
    description: str = ""
    bullets: List[str] = None
    role_specific_frames: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.bullets is None:
            self.bullets = []
        if self.role_specific_frames is None:
            self.role_specific_frames = {}

@dataclass
class SkillCategory:
    """Skills organized by category"""
    category: str = ""
    skills: List[str] = None
    proficiency: str = ""  # genuine, bridging_needed, learning
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []

@dataclass
class ResumePreferences:
    """Resume creation preferences"""
    # Core Rules
    tailor_every_resume: bool = True
    honest_framing_only: bool = True
    ats_first_human_second: bool = True
    
    # Formatting Rules
    one_page_always: bool = True
    font: str = "Arial"
    name_size: int = 44
    section_header_size: int = 22
    body_size: int = 19
    subline_size: int = 18
    
    # Colors
    blue_color: str = "#1a56db"
    black_color: str = "#0d0d0d"
    gray_color: str = "#444444"
    light_gray_color: str = "#666666"
    
    # ATS Rules
    avoid_tables: bool = True
    avoid_columns: bool = True
    avoid_headers_footers: bool = True
    avoid_text_boxes: bool = True
    
    # Cover Letter Rules
    cover_letter_format: str = "docx"  # docx only, never plain text
    cover_letter_structure: List[str] = None
    
    def __post_init__(self):
        if self.cover_letter_structure is None:
            self.cover_letter_structure = [
                "Hook (specific and confident, never 'I am writing to apply')",
                "Primary proof point with numbers",
                "Secondary proof or current internship relevance",
                "Credibility signals",
                "Why THIS company (specific, never generic)",
                "Availability + call to action"
            ]

@dataclass
class BridgingRules:
    """Honest bridging rules for skills"""
    # Skills that are genuinely held (no bridging needed)
    genuine_skills: List[str] = None
    
    # Skills that need bridging (partial exposure only)
    bridging_skills: Dict[str, str] = None
    
    # Bridging phrases
    bridging_phrases: Dict[str, str] = None
    
    def __post_init__(self):
        if self.genuine_skills is None:
            self.genuine_skills = [
                "Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "Random Forest",
                "Gradient Boosting", "Ensemble Methods", "LangChain", "LLaMA 3.3 70B",
                "Groq API", "Prompt Engineering", "FastAPI", "REST APIs", "SQLite",
                "SQLAlchemy", "ETL pipelines", "Data Cleaning", "EDA", "Statistical Analysis",
                "Matplotlib", "Seaborn", "Plotly", "Streamlit", "Power BI", "Git & GitHub",
                "pytest", "OOP", "Java", "DSA", "YOLO11s", "OpenCV", "Computer Vision",
                "Real-time Inference"
            ]
        
        if self.bridging_skills is None:
            self.bridging_skills = {
                "TensorFlow": "fundamentals — coursework exposure, no production use",
                "PyTorch": "fundamentals — coursework exposure, no production use",
                "Docker": "learning — understands concepts, no hands-on deployment",
                "RAG Pipelines": "concepts — understands architecture, no full project built yet",
                "Vector Databases (FAISS/ChromaDB)": "fundamentals — conceptual from LangChain study",
                "LangGraph": "actively learning — no hands-on yet",
                "Tableau": "learning — Power BI experience, Tableau not used",
                "MySQL/PostgreSQL": "fundamentals — primary DB experience is SQLite, same SQL syntax",
                "React": "fundamentals — Streamlit/JavaScript experience, no React app built",
                "AWS": "fundamentals — conceptual knowledge, no console deployment",
                "MLflow/Kubeflow": "concepts — understands MLOps principles, no tooling used"
            }
        
        if self.bridging_phrases is None:
            self.bridging_phrases = {
                "never_used": "(fundamentals) or (concepts)",
                "currently_learning": "(learning) or actively learning",
                "used_once": "State the specific project context — never generalize"
            }

@dataclass
class ProjectSelectionGuide:
    """Which project leads by role type"""
    role_project_order: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.role_project_order is None:
            self.role_project_order = {
                "Data Analyst": ["Bluestock N100 Capstone", "ShopSmart", "NovaGen"],
                "ML Engineer": ["NovaGen", "ShopSmart", "Bluestock N100 Capstone", "Avotangi"],
                "GenAI/LLM/Agentic AI": ["Avotangi", "Bluestock N100 Capstone", "NovaGen"],
                "SWE/Software Engineering": ["Avotangi (as distributed system)", "Bluestock N100 Capstone (as data platform)", "NovaGen"],
                "Healthcare AI": ["NovaGen", "Bluestock N100 Capstone", "Avotangi"],
                "BI/Dashboard": ["Bluestock N100 Capstone", "ShopSmart"],
                "Data Engineering/ETL": ["Bluestock N100 Capstone", "ShopSmart"],
                "Fintech/Quant": ["Bluestock N100 Capstone", "NovaGen", "Avotangi"],
                "Computer Vision": ["AI Blind Assist", "NovaGen"]
            }

@dataclass
class LegitimacyChecker:
    """Company legitimacy checking rules"""
    red_flags: List[str] = None
    suspicious_domains: List[str] = None
    companies_to_avoid: List[str] = None
    
    def __post_init__(self):
        if self.red_flags is None:
            self.red_flags = [
                ".cc, .tk, .xyz domain emails — not legitimate business emails",
                "'Refer & Win' banners prominently featured — MLM-style operation",
                "Vague JD with no specific responsibilities — copy-paste generic posting",
                "Asking for payment at any stage — immediate red flag, report to platform",
                "No LinkedIn company page or employees listed — unverifiable company",
                "Ed-tech/bootcamp companies disguised as employers"
            ]
        
        if self.suspicious_domains is None:
            self.suspicious_domains = [".cc", ".tk", ".xyz", ".ml", ".ga"]
        
        if self.companies_to_avoid is None:
            self.companies_to_avoid = [
                "Crossing Hurdles", "Zetheta Algorithms", "Nexora",
                "Fin Maverick", "Cornixe"
            ]

@dataclass
class JobPreferences:
    """User's job preferences"""
    keywords: List[str] = None
    locations: List[str] = None
    job_type: str = "internship"
    remote: bool = True
    min_stipend: int = 0
    max_applications_per_day: int = 10
    roles_to_avoid: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = ["AI", "ML", "Machine Learning", "Data Science", "Python", "Data Analyst", "SWE"]
        if self.locations is None:
            self.locations = ["Remote", "Bangalore", "Hyderabad", "Chennai", "Pune"]
        if self.roles_to_avoid is None:
            self.roles_to_avoid = [
                "Operations",
                "Cybersecurity/SOC",
                "Pure Finance",
                "Data Entry/Annotation",
                "ETL tools (Informatica, Talend, Airflow)"
            ]

class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.personal_profile = PersonalProfile()
        self.resume_preferences = ResumePreferences()
        self.bridging_rules = BridgingRules()
        self.project_selection_guide = ProjectSelectionGuide()
        self.legitimacy_checker = LegitimacyChecker()
        self.preferences = JobPreferences()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        config_file = DATA_DIR / "config.json"
        if config_file.exists():
            with open(config_file, "r") as f:
                data = json.load(f)
                # Update attributes from loaded data
                for key, value in data.items():
                    if hasattr(self, key):
                        if isinstance(value, dict):
                            # For dataclass instances, update their attributes
                            current = getattr(self, key)
                            if hasattr(current, '__dict__'):
                                for k, v in value.items():
                                    if hasattr(current, k):
                                        setattr(current, k, v)
                        else:
                            setattr(self, key, value)
    
    def save_config(self):
        """Save configuration to file"""
        config_file = DATA_DIR / "config.json"
        data = {
            "personal_profile": self.personal_profile.__dict__,
            "resume_preferences": self.resume_preferences.__dict__,
            "bridging_rules": self.bridging_rules.__dict__,
            "project_selection_guide": self.project_selection_guide.__dict__,
            "legitimacy_checker": self.legitimacy_checker.__dict__,
            "preferences": self.preferences.__dict__
        }
        with open(config_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def update_personal_profile(self, **kwargs):
        """Update personal profile"""
        for key, value in kwargs.items():
            if hasattr(self.personal_profile, key):
                setattr(self.personal_profile, key, value)
        self.save_config()
    
    def update_preferences(self, **kwargs):
        """Update job preferences"""
        for key, value in kwargs.items():
            if hasattr(self.preferences, key):
                setattr(self.preferences, key, value)
        self.save_config()

# Global config instance
config = Config()
