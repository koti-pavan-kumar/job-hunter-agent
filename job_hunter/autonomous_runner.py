"""
Autonomous Scheduler - GitHub Actions based
Runs at 8 AM and 6 PM IST daily via GitHub Actions cron
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from job_hunter.job_search_api import job_search_api
from job_hunter.config import config

# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def run_job_search():
    """Run the autonomous job search and resume generation"""
    
    now = datetime.now(IST)
    print(f"\n{'='*70}")
    print(f"AUTONOMOUS JOB SEARCH - {now.strftime('%Y-%m-%d %H:%M:%S IST')}")
    print(f"{'='*70}\n")
    
    stats = {
        "timestamp": now.isoformat(),
        "jobs_found": 0,
        "new_jobs": 0,
        "resumes_generated": 0,
        "errors": []
    }
    
    # Step 1: Search for jobs from all sources
    print("STEP 1: Searching for jobs from all sources...")
    
    try:
        keywords = config.preferences.keywords
        
        all_jobs = job_search_api.search_all_sources(keywords)
        
        stats["jobs_found"] = len(all_jobs)
        print(f"\nTotal jobs found: {len(all_jobs)}")
        
    except Exception as e:
        error_msg = f"Error searching jobs: {e}"
        print(f"ERROR: {error_msg}")
        stats["errors"].append(error_msg)
        all_jobs = []
    
    # Step 2: Save jobs to JSON
    print("\nSTEP 2: Saving jobs to database...")
    
    try:
        if all_jobs:
            job_search_api.save_jobs_to_json(all_jobs)
            
            existing_jobs = job_search_api.get_jobs_from_json()
            new_count = sum(1 for j in existing_jobs if j.get("status") == "new")
            stats["new_jobs"] = new_count
            print(f"Saved {len(all_jobs)} jobs, {new_count} new")
    except Exception as e:
        error_msg = f"Error saving jobs: {e}"
        print(f"ERROR: {error_msg}")
        stats["errors"].append(error_msg)
    
    # Step 3: Generate resumes for high-fit jobs
    print("\nSTEP 3: Generating resumes for matching jobs...")
    
    try:
        from job_hunter.resume_generator import resume_generator
        
        existing_jobs = job_search_api.get_jobs_from_json()
        new_jobs = [j for j in existing_jobs if j.get("status") == "new"]
        
        resumes_dir = Path(__file__).parent / "resumes"
        resumes_dir.mkdir(exist_ok=True)
        
        for job in new_jobs[:config.preferences.max_applications_per_day]:
            try:
                fit_score = _assess_job_fit(job)
                
                if fit_score < 4:
                    print(f"  Skipping (fit {fit_score}/10): {job['title']}")
                    job["status"] = "low_fit"
                    continue
                
                print(f"  Generating resume for {job['title']} at {job['company']}...")
                
                resume_result = resume_generator.generate_tailored_resume(
                    job_title=job["title"],
                    company_name=job["company"],
                    job_description=job["description"]
                )
                
                company_clean = job["company"].replace(" ", "_").replace("/", "_")[:30]
                title_clean = job["title"].replace(" ", "_").replace("/", "_")[:30]
                job_folder = resumes_dir / f"{company_clean}_{title_clean}"
                job_folder.mkdir(exist_ok=True)
                
                resume_content = resume_result.get("resume_content", {})
                resume_text = format_resume_text(resume_content)
                
                with open(job_folder / "resume.txt", "w", encoding="utf-8") as f:
                    f.write(resume_text)
                
                with open(job_folder / "job_details.txt", "w", encoding="utf-8") as f:
                    f.write(f"Job Title: {job['title']}\n")
                    f.write(f"Company: {job['company']}\n")
                    f.write(f"Location: {job['location']}\n")
                    f.write(f"URL: {job['url']}\n")
                    f.write(f"Fit Score: {fit_score}/10\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                with open(job_folder / "job_description.txt", "w", encoding="utf-8") as f:
                    f.write(f"=== JOB DESCRIPTION ===\n\n{job['description']}\n")
                
                job["status"] = "processed"
                stats["resumes_generated"] += 1
                
                print(f"  Resume generated (fit: {fit_score}/10)")
                
            except Exception as e:
                print(f"  Error generating resume: {e}")
                stats["errors"].append(f"Resume error: {e}")
        
        job_search_api.save_jobs_to_json(all_jobs)
        
    except Exception as e:
        error_msg = f"Error generating resumes: {e}"
        print(f"ERROR: {error_msg}")
        stats["errors"].append(error_msg)
    
    # Step 4: Generate summary
    print(f"\n{'='*70}")
    print(f"SEARCH COMPLETE!")
    print(f"{'='*70}")
    print(f"Statistics:")
    print(f"  - Jobs Found: {stats['jobs_found']}")
    print(f"  - New Jobs: {stats['new_jobs']}")
    print(f"  - Resumes Generated: {stats['resumes_generated']}")
    if stats["errors"]:
        print(f"  - Errors: {len(stats['errors'])}")
    print(f"{'='*70}\n")
    
    stats_file = Path(__file__).parent / "data" / "search_stats.json"
    stats_file.parent.mkdir(exist_ok=True)
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    
    return stats


def _assess_job_fit(job: dict) -> int:
    """Assess how well the job matches user's skills (1-10)"""
    
    good_keywords = [
        "python", "machine learning", "ai", "ml", "data science",
        "deep learning", "nlp", "natural language processing",
        "computer vision", "data analyst", "langchain", "llm",
        "genai", "agentic", "intern", "data scientist"
    ]
    
    bad_keywords = [
        "operations", "cybersecurity", "soc", "finance",
        "data entry", "annotation", "informatica", "talend"
    ]
    
    text = (job.get("title", "") + " " + job.get("description", "")).lower()
    
    score = 5
    
    for kw in good_keywords:
        if kw in text:
            score += 1
    
    for kw in bad_keywords:
        if kw in text:
            score -= 2
    
    return max(1, min(10, score))


def format_resume_text(resume_content: dict) -> str:
    """Format resume content as readable text"""
    
    if not resume_content:
        return "No resume content generated"
    
    parts = []
    
    if resume_content.get("name"):
        parts.append(resume_content["name"])
    if resume_content.get("contact"):
        parts.append(resume_content["contact"])
    
    parts.append("\n" + "="*60)
    parts.append("OBJECTIVE")
    parts.append("="*60)
    parts.append(resume_content.get("objective", ""))
    
    parts.append("\n" + "="*60)
    parts.append("EDUCATION")
    parts.append("="*60)
    parts.append(resume_content.get("education", ""))
    
    parts.append("\n" + "="*60)
    parts.append("TECHNICAL SKILLS")
    parts.append("="*60)
    parts.append(resume_content.get("technical_skills", ""))
    
    parts.append("\n" + "="*60)
    parts.append("PROJECTS")
    parts.append("="*60)
    
    for project in resume_content.get("projects", []):
        parts.append(f"\n{project.get('title', '')} | {project.get('date', '')}")
        parts.append(project.get("tech_stack", ""))
        for bullet in project.get("bullets", []):
            parts.append(f"* {bullet}")
    
    parts.append("\n" + "="*60)
    parts.append("EXPERIENCE")
    parts.append("="*60)
    
    exp = resume_content.get("experience", {})
    if exp:
        parts.append(f"{exp.get('company', '')} | {exp.get('role', '')}")
        parts.append(exp.get("duration", ""))
        for bullet in exp.get("bullets", []):
            parts.append(f"* {bullet}")
    
    parts.append("\n" + "="*60)
    parts.append("ACHIEVEMENTS & CERTIFICATIONS")
    parts.append("="*60)
    parts.append(resume_content.get("achievements", ""))
    
    return "\n".join(parts)


if __name__ == "__main__":
    run_job_search()
