"""
Agent Runner - Main orchestrator for the job hunting agent
Handles login, job extraction, skill matching, and resume generation
"""
import asyncio
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict

from .browser_agent import browser_agent

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))


class AgentRunner:
    """Main agent that runs the autonomous job hunting workflow"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.resumes_dir = Path(__file__).parent.parent / "resumes"
        self.resumes_dir.mkdir(exist_ok=True)
    
    async def run_full_workflow(self):
        """Run the complete autonomous workflow"""
        now = datetime.now(IST)
        
        print(f"\n{'='*70}")
        print(f"🤖 AI JOB HUNTING AGENT - {now.strftime('%Y-%m-%d %H:%M:%S IST')}")
        print(f"{'='*70}\n")
        
        stats = {
            "timestamp": now.isoformat(),
            "platforms_checked": 0,
            "jobs_found": 0,
            "relevant_jobs": 0,
            "resumes_generated": 0
        }
        
        # Step 1: Check login status
        print("📋 STEP 1: Checking login status...")
        login_status = browser_agent.check_login_status()
        
        for platform, logged_in in login_status.items():
            status = "✅ Logged in" if logged_in else "❌ Not logged in"
            print(f"  {platform}: {status}")
        
        # Step 2: Extract jobs from logged-in platforms
        print(f"\n🔍 STEP 2: Extracting jobs from platforms...")
        
        all_jobs = []
        
        if login_status.get("LinkedIn"):
            print("\n  Searching LinkedIn...")
            try:
                linkedin_jobs = await browser_agent.extract_linkedin_jobs()
                linkedin_relevant = [j for j in linkedin_jobs if browser_agent._is_relevant(j["title"], j["description"])]
                all_jobs.extend(linkedin_relevant)
                browser_agent.save_jobs(linkedin_relevant, "LinkedIn")
                stats["platforms_checked"] += 1
                print(f"  LinkedIn: {len(linkedin_relevant)} relevant jobs")
            except Exception as e:
                print(f"  LinkedIn error: {e}")
        
        if login_status.get("Internshala"):
            print("\n  Searching Internshala...")
            try:
                internshala_jobs = await browser_agent.extract_internshala_jobs()
                internshala_relevant = [j for j in internshala_jobs if browser_agent._is_relevant(j["title"], j["description"])]
                all_jobs.extend(internshala_relevant)
                browser_agent.save_jobs(internshala_relevant, "Internshala")
                stats["platforms_checked"] += 1
                print(f"  Internshala: {len(internshala_relevant)} relevant jobs")
            except Exception as e:
                print(f"  Internshala error: {e}")
        
        if login_status.get("Unstop"):
            print("\n  Searching Unstop...")
            try:
                unstop_jobs = await browser_agent.extract_unstop_jobs()
                unstop_relevant = [j for j in unstop_jobs if browser_agent._is_relevant(j["title"], j["description"])]
                all_jobs.extend(unstop_relevant)
                browser_agent.save_jobs(unstop_relevant, "Unstop")
                stats["platforms_checked"] += 1
                print(f"  Unstop: {len(unstop_relevant)} relevant jobs")
            except Exception as e:
                print(f"  Unstop error: {e}")
        
        stats["jobs_found"] = len(all_jobs)
        stats["relevant_jobs"] = len(all_jobs)
        
        # Step 3: Generate resumes for relevant jobs
        print(f"\n📝 STEP 3: Generating resumes for {len(all_jobs)} relevant jobs...")
        
        for job in all_jobs[:10]:  # Limit to 10 resumes per run
            try:
                print(f"  Generating resume for {job['title']} at {job['company']}...")
                
                from job_hunter.resume_generator import resume_generator
                
                resume_result = resume_generator.generate_tailored_resume(
                    job_title=job["title"],
                    company_name=job["company"],
                    job_description=job["description"]
                )
                
                # Save resume
                company_clean = job["company"].replace(" ", "_").replace("/", "_")[:30]
                title_clean = job["title"].replace(" ", "_").replace("/", "_")[:30]
                job_folder = self.resumes_dir / f"{company_clean}_{title_clean}"
                job_folder.mkdir(exist_ok=True)
                
                resume_content = resume_result.get("resume_content", {})
                resume_text = self._format_resume(resume_content)
                
                with open(job_folder / "resume.txt", "w", encoding="utf-8") as f:
                    f.write(resume_text)
                
                with open(job_folder / "job_details.txt", "w", encoding="utf-8") as f:
                    f.write(f"Job Title: {job['title']}\n")
                    f.write(f"Company: {job['company']}\n")
                    f.write(f"Location: {job['location']}\n")
                    f.write(f"URL: {job['url']}\n")
                    f.write(f"Platform: {job['platform']}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                with open(job_folder / "job_description.txt", "w", encoding="utf-8") as f:
                    f.write(f"=== JOB DESCRIPTION ===\n\n{job['description']}\n")
                
                stats["resumes_generated"] += 1
                print(f"  ✅ Resume generated!")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Step 4: Summary
        print(f"\n{'='*70}")
        print(f"✅ AGENT WORKFLOW COMPLETE!")
        print(f"{'='*70}")
        print(f"Platforms checked: {stats['platforms_checked']}")
        print(f"Jobs found: {stats['jobs_found']}")
        print(f"Resumes generated: {stats['resumes_generated']}")
        print(f"{'='*70}\n")
        
        # Save stats
        stats_file = self.data_dir / "agent_stats.json"
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    async def login_all_platforms(self):
        """Login to all platforms"""
        print("\n🔐 Logging into platforms...")
        
        print("\n1. LinkedIn:")
        await browser_agent.login_linkedin()
        
        print("\n2. Internshala:")
        await browser_agent.login_internshala()
        
        print("\n3. Unstop:")
        await browser_agent.login_unstop()
        
        print("\n✅ All platforms logged in!")
    
    def _format_resume(self, resume_content: dict) -> str:
        """Format resume content as text"""
        if not resume_content:
            return "No resume content"
        
        parts = []
        
        if resume_content.get("name"):
            parts.append(resume_content["name"])
        if resume_content.get("contact"):
            parts.append(resume_content["contact"])
        
        for section in ["objective", "education", "technical_skills"]:
            if resume_content.get(section):
                parts.append(f"\n{'='*60}")
                parts.append(section.upper().replace("_", " "))
                parts.append("="*60)
                parts.append(resume_content[section])
        
        if resume_content.get("projects"):
            parts.append(f"\n{'='*60}")
            parts.append("PROJECTS")
            parts.append("="*60)
            for project in resume_content["projects"]:
                parts.append(f"\n{project.get('title', '')} | {project.get('date', '')}")
                for bullet in project.get("bullets", []):
                    parts.append(f"* {bullet}")
        
        return "\n".join(parts)


# Global instance
agent_runner = AgentRunner()


if __name__ == "__main__":
    # Run login
    asyncio.run(agent_runner.login_all_platforms())
    
    # Run workflow
    asyncio.run(agent_runner.run_full_workflow())
