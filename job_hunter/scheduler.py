"""
Scheduler - Fully Autonomous Job Hunting
"""
import schedule
import time
from datetime import datetime
import logging
from typing import List

from .config import config
from .database import db, JobListing
from .scrapers import LinkedInScraper, NaukriScraper, InternshalaScraper, GoogleJobsScraper
from .resume_generator import resume_generator
from .cover_letter_generator import cover_letter_generator
from .legitimacy_checker import legitimacy_checker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/job_hunter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutonomousJobHunter:
    """Fully autonomous job hunting scheduler"""
    
    def __init__(self):
        self.scrapers = [
            LinkedInScraper(),
            NaukriScraper(),
            InternshalaScraper(),
            GoogleJobsScraper()
        ]
        self.daily_stats = {
            "jobs_found": 0,
            "resumes_generated": 0,
            "companies_checked": 0,
            "legitimate_jobs": 0,
            "skipped_jobs": 0
        }
    
    def autonomous_job_search(self):
        """Fully autonomous job search and resume generation"""
        logger.info("=" * 70)
        logger.info(f"AUTONOMOUS JOB SEARCH - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        
        # Reset daily stats
        self.daily_stats = {
            "jobs_found": 0,
            "resumes_generated": 0,
            "companies_checked": 0,
            "legitimate_jobs": 0,
            "skipped_jobs": 0
        }
        
        # Get user preferences
        keywords = config.preferences.keywords
        location = config.preferences.locations[0] if config.preferences.locations else ""
        
        # Step 1: Search all platforms
        logger.info("\n📡 STEP 1: Searching all platforms...")
        for scraper in self.scrapers:
            try:
                logger.info(f"  Searching {scraper.platform_name}...")
                jobs = scraper.scrape_and_store(keywords, location)
                self.daily_stats["jobs_found"] += len(jobs)
                logger.info(f"  Found {len(jobs)} new jobs on {scraper.platform_name}")
            except Exception as e:
                logger.error(f"  Error searching {scraper.platform_name}: {e}")
        
        # Step 2: Process new jobs
        logger.info(f"\n🔍 STEP 2: Processing {self.daily_stats['jobs_found']} new jobs...")
        new_jobs = db.get_new_jobs()
        
        for job in new_jobs[:config.preferences.max_applications_per_day]:
            try:
                # Step 2a: Check company legitimacy
                logger.info(f"\n  Checking {job.company}...")
                legitimacy_result = legitimacy_checker.check_company(
                    company_name=job.company,
                    job_description=job.description,
                    company_url=job.url
                )
                self.daily_stats["companies_checked"] += 1
                
                if legitimacy_result["recommendation"] == "skip":
                    logger.warning(f"  ⚠️ SKIPPED: {job.company} - {legitimacy_result['risk_level']} risk")
                    db.update_job_status(job.id, "skipped")
                    self.daily_stats["skipped_jobs"] += 1
                    continue
                
                # Step 2b: Assess fit with user's skills
                fit_score = self._assess_job_fit(job)
                
                if fit_score < 4:
                    logger.info(f"  ⏭️ Low fit ({fit_score}/10): {job.title} at {job.company}")
                    db.update_job_status(job.id, "low_fit")
                    self.daily_stats["skipped_jobs"] += 1
                    continue
                
                # Step 2c: Generate tailored resume
                logger.info(f"  📝 Generating resume for {job.title} at {job.company}...")
                resume_result = resume_generator.generate_tailored_resume(
                    job_title=job.title,
                    company_name=job.company,
                    job_description=job.description
                )
                
                # Step 2d: Generate cover letter
                cover_letter_result = cover_letter_generator.generate_cover_letter(
                    job_title=job.title,
                    company_name=job.company,
                    job_description=job.description,
                    resume_content=resume_result["resume_content"]
                )
                
                # Step 2e: Save files
                self._save_generated_files(job, resume_result, cover_letter_result)
                
                # Step 2f: Update database
                db.update_job_status(job.id, "processed")
                
                self.daily_stats["resumes_generated"] += 1
                self.daily_stats["legitimate_jobs"] += 1
                
                logger.info(f"  ✅ Generated resume for {job.title} at {job.company}")
                logger.info(f"     Fit Score: {fit_score}/10 | Role: {resume_result['analysis']['role_type']}")
                
            except Exception as e:
                logger.error(f"  ❌ Error processing job {job.id}: {e}")
        
        # Step 3: Generate daily summary
        self._generate_daily_summary()
        
        # Step 4: Log statistics
        db.log_daily_stats(
            self.daily_stats["jobs_found"],
            self.daily_stats["resumes_generated"],
            f"Companies checked: {self.daily_stats['companies_checked']}, "
            f"Legitimate: {self.daily_stats['legitimate_jobs']}, "
            f"Skipped: {self.daily_stats['skipped_jobs']}"
        )
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ AUTONOMOUS SEARCH COMPLETE!")
        logger.info("=" * 70)
        logger.info("Check 'job_hunter/resumes/' folder for generated resumes.")
        logger.info("Review them and apply when you have time.")
        logger.info("=" * 70)
    
    def _assess_job_fit(self, job: JobListing) -> int:
        """Assess how well the job matches user's skills (1-10)"""
        
        # Keywords that indicate good fit
        good_fit_keywords = [
            "python", "machine learning", "ai", "ml", "data science",
            "deep learning", "nlp", "natural language processing",
            "computer vision", "data analyst", "data science",
            "langchain", "llm", "genai", "agentic"
        ]
        
        # Keywords that indicate bad fit
        bad_fit_keywords = [
            "operations", "cybersecurity", "soc", "finance",
            "data entry", "annotation", "informatica", "talend"
        ]
        
        job_description_lower = job.description.lower()
        job_title_lower = job.title.lower()
        
        # Calculate fit score
        score = 5  # Base score
        
        # Add points for good keywords
        for keyword in good_fit_keywords:
            if keyword in job_description_lower or keyword in job_title_lower:
                score += 1
        
        # Subtract points for bad keywords
        for keyword in bad_fit_keywords:
            if keyword in job_description_lower or keyword in job_title_lower:
                score -= 2
        
        # Bonus for specific role matches
        if "intern" in job_title_lower:
            score += 1
        if "ai" in job_title_lower or "ml" in job_title_lower:
            score += 1
        
        return max(1, min(10, score))
    
    def _save_generated_files(self, job: JobListing, resume_result: Dict, 
                             cover_letter_result: Dict):
        """Save generated resume and cover letter files"""
        
        from pathlib import Path
        from .config import RESUMES_DIR
        
        # Create job-specific folder
        company_clean = job.company.replace(" ", "_").replace("/", "_")[:20]
        title_clean = job.title.replace(" ", "_").replace("/", "_")[:20]
        job_folder = RESUMES_DIR / f"{company_clean}_{title_clean}"
        job_folder.mkdir(exist_ok=True)
        
        # Save resume as text file
        resume_content = resume_result["resume_content"]
        resume_text = self._format_resume_text(resume_content)
        
        resume_path = job_folder / "resume.txt"
        with open(resume_path, "w", encoding="utf-8") as f:
            f.write(resume_text)
        
        # Save cover letter
        cover_letter_path = job_folder / "cover_letter.txt"
        with open(cover_letter_path, "w", encoding="utf-8") as f:
            f.write(cover_letter_result["cover_letter"])
        
        # Save job details
        job_details_path = job_folder / "job_details.txt"
        with open(job_details_path, "w", encoding="utf-8") as f:
            f.write(f"Job Title: {job.title}\n")
            f.write(f"Company: {job.company}\n")
            f.write(f"Location: {job.location}\n")
            f.write(f"URL: {job.url}\n")
            f.write(f"Fit Score: {resume_result['fit_score']}/10\n")
            f.write(f"Role Type: {resume_result['analysis']['role_type']}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Save bridging notes if any
        if resume_result.get("bridging_notes"):
            bridging_path = job_folder / "bridging_notes.txt"
            with open(bridging_path, "w", encoding="utf-8") as f:
                f.write("BRIDGING NOTES - What to say in interview:\n\n")
                for note in resume_result["bridging_notes"]:
                    f.write(f"• {note}\n")
    
    def _format_resume_text(self, resume_content: Dict) -> str:
        """Format resume content as readable text"""
        
        resume = f"""
{resume_content['name']}
{resume_content['contact']}

================================================================================
OBJECTIVE
================================================================================

{resume_content['objective']}

================================================================================
EDUCATION
================================================================================

{resume_content['education']}

================================================================================
TECHNICAL SKILLS
================================================================================

{resume_content['technical_skills']}

================================================================================
PROJECTS
================================================================================

"""
        
        for i, project in enumerate(resume_content['projects'], 1):
            resume += f"{project['title']} | {project['date']}\n"
            resume += f"{project['tech_stack']}\n"
            resume += f"{project['github']}\n\n"
            for bullet in project['bullets']:
                resume += f"• {bullet}\n"
            resume += "\n"
        
        resume += """
================================================================================
EXPERIENCE
================================================================================

"""
        
        exp = resume_content['experience']
        resume += f"{exp['company']} | {exp['role']}\n"
        resume += f"{exp['duration']}\n\n"
        for bullet in exp['bullets']:
            resume += f"• {bullet}\n"
        
        resume += f"""

================================================================================
ACHIEVEMENTS & CERTIFICATIONS
================================================================================

{resume_content['achievements']}

================================================================================
ADDITIONAL
================================================================================

{resume_content['additional']}

================================================================================
"""
        
        return resume
    
    def _generate_daily_summary(self):
        """Generate and save daily summary"""
        
        summary = f"""
================================================================================
DAILY JOB SEARCH SUMMARY
================================================================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

STATISTICS:
• Jobs Found: {self.daily_stats['jobs_found']}
• Resumes Generated: {self.daily_stats['resumes_generated']}
• Companies Checked: {self.daily_stats['companies_checked']}
• Legitimate Jobs: {self.daily_stats['legitimate_jobs']}
• Skipped Jobs: {self.daily_stats['skipped_jobs']}

NEXT STEPS:
1. Check 'job_hunter/resumes/' folder for generated resumes
2. Review each resume and cover letter
3. Apply to the ones you like when you have time

================================================================================
"""
        
        # Save summary
        from .config import DATA_DIR
        summary_path = DATA_DIR / f"daily_summary_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        
        logger.info(summary)
    
    def start_autonomous_mode(self, run_immediately: bool = False):
        """Start fully autonomous job hunting"""
        logger.info("🚀 STARTING FULLY AUTONOMOUS JOB HUNTER")
        logger.info("=" * 70)
        logger.info("This agent will:")
        logger.info("  ✅ Search jobs at 8:00 AM and 6:00 PM daily")
        logger.info("  ✅ Check company legitimacy automatically")
        logger.info("  ✅ Generate tailored resumes for matching jobs")
        logger.info("  ✅ Generate cover letters in .docx format")
        logger.info("  ✅ Save everything in organized folders")
        logger.info("  ✅ You just review and apply when you have time!")
        logger.info("=" * 70)
        
        # Schedule autonomous search at 8 AM and 6 PM
        schedule.every().day.at("08:00").do(self.autonomous_job_search)
        schedule.every().day.at("18:00").do(self.autonomous_job_search)
        
        logger.info("\n📅 Schedule:")
        logger.info("  • 8:00 AM - Morning search")
        logger.info("  • 6:00 PM - Evening search")
        logger.info("\nPress Ctrl+C to stop.")
        
        # Run immediately if requested
        if run_immediately:
            logger.info("\n⚡ Running initial autonomous search...")
            self.autonomous_job_search()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\n🛑 Autonomous job hunter stopped by user.")
            logger.info("Generated resumes are in 'job_hunter/resumes/' folder.")

# Global instance
autonomous_hunter = AutonomousJobHunter()
