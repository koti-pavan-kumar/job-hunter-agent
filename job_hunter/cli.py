"""
CLI Interface - Command line interface for Job Hunter Agent
"""
import argparse
import sys
from datetime import datetime

from .config import config
from .database import db
from .scheduler import autonomous_hunter
from .resume_generator import resume_generator

def print_banner():
    """Print application banner"""
    banner = """
============================================================
           JOB HUNTER AGENT v2.0 (Autonomous)
       Automated Job Search & Resume Generation
============================================================
    """
    print(banner)

def setup_command(args):
    """Interactive setup wizard"""
    print("\n Setup Wizard - Job Hunter Agent")
    print("=" * 50)
    
    # Personal Information
    print("\n Personal Information (Pre-loaded from your profile)")
    print(f"Name: {config.personal_profile.name}")
    print(f"Email: {config.personal_profile.email}")
    print(f"Phone: {config.personal_profile.phone}")
    print(f"LinkedIn: {config.personal_profile.linkedin_url}")
    print(f"GitHub: {config.personal_profile.github_url}")
    
    # Job Preferences
    print("\n Job Preferences")
    keywords_input = input("Job keywords (comma-separated, or press Enter to use defaults): ").strip()
    if keywords_input:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    else:
        keywords = config.preferences.keywords
    
    locations_input = input("Preferred locations (comma-separated, or press Enter for defaults): ").strip()
    if locations_input:
        locations = [l.strip() for l in locations_input.split(",") if l.strip()]
    else:
        locations = config.preferences.locations
    
    config.update_preferences(keywords=keywords, locations=locations)
    
    print("\n Setup complete!")
    print("Run 'python -m job_hunter run' to start autonomous job hunting!")

def run_command(args):
    """Start autonomous scheduler"""
    print("\n STARTING FULLY AUTONOMOUS JOB HUNTER")
    print("=" * 60)
    print("This agent will automatically:")
    print("  Search jobs at 8:00 AM and 6:00 PM daily")
    print("  Check company legitimacy")
    print("  Generate tailored resumes for matching jobs")
    print("  Generate cover letters")
    print("  Save everything in 'job_hunter/resumes/' folder")
    print("=" * 60)
    print("\nYou just need to:")
    print("  1. Check the 'job_hunter/resumes/' folder")
    print("  2. Review the generated resumes")
    print("  3. Apply to the ones you like when you have time")
    print("=" * 60)
    print("\nPress Ctrl+C to stop.\n")
    
    autonomous_hunter.start_autonomous_mode(run_immediately=args.immediate)

def search_command(args):
    """Search for jobs (one-time)"""
    print("\n Searching for jobs...")
    
    keywords = args.keywords.split(",") if args.keywords else config.preferences.keywords
    location = args.location or (config.preferences.locations[0] if config.preferences.locations else "")
    
    from .scrapers import LinkedInScraper, NaukriScraper, InternshalaScraper, GoogleJobsScraper
    
    scrapers = []
    if not args.platform or "linkedin" in args.platform.lower():
        scrapers.append(LinkedInScraper())
    if not args.platform or "naukri" in args.platform.lower():
        scrapers.append(NaukriScraper())
    if not args.platform or "internshala" in args.platform.lower():
        scrapers.append(InternshalaScraper())
    if not args.platform or "google" in args.platform.lower():
        scrapers.append(GoogleJobsScraper())
    
    total_jobs = 0
    for scraper in scrapers:
        print(f"\nSearching {scraper.platform_name}...")
        jobs = scraper.scrape_and_store(keywords, location)
        print(f"Found {len(jobs)} new jobs")
        total_jobs += len(jobs)
    
    print(f"\n Total new jobs found: {total_jobs}")
    print("Run 'python -m job_hunter list' to see all jobs.")

def list_command(args):
    """List jobs"""
    print("\n Job Listings")
    print("=" * 80)
    
    status_filter = args.status if args.status else None
    jobs = db.get_all_jobs(status_filter)
    
    if not jobs:
        print("No jobs found. Run 'python -m job_hunter search' to find jobs.")
        return
    
    for job in jobs[:20]:  # Show first 20
        status_icon = {
            "new": "NEW",
            "processed": "DONE",
            "applied": "SENT",
            "interview": "INTERVIEW",
            "rejected": "REJECT",
            "offered": "OFFER",
            "skipped": "SKIP",
            "low_fit": "LOW FIT"
        }.get(job.status, "???")
        
        print(f"\n[{status_icon}] {job.title}")
        print(f"   Company: {job.company}")
        print(f"   Location: {job.location}")
        print(f"   Platform: {job.platform}")
        print(f"   Status: {job.status}")
        print(f"   URL: {job.url}")
        print("-" * 80)
    
    if len(jobs) > 20:
        print(f"\n... and {len(jobs) - 20} more jobs.")
        print("Use 'python -m job_hunter list --status new' to filter.")

def apply_command(args):
    """Generate resume and prepare application"""
    print("\n Preparing Application")
    
    job_id = args.job_id
    jobs = db.get_all_jobs("new")
    
    job = None
    for j in jobs:
        if j.id == job_id:
            job = j
            break
    
    if not job:
        print(f" Job with ID {job_id} not found or not in 'new' status.")
        return
    
    print(f"\nJob: {job.title} at {job.company}")
    print(f"Generating tailored resume...")
    
    # Generate resume
    resume_result = resume_generator.generate_tailored_resume(
        job_title=job.title,
        company_name=job.company,
        job_description=job.description
    )
    
    print(f"Fit Score: {resume_result['fit_score']}/10")
    print(f"Role Type: {resume_result['analysis']['role_type']}")
    
    # Generate cover letter
    from .cover_letter_generator import cover_letter_generator
    cover_letter_result = cover_letter_generator.generate_cover_letter(
        job_title=job.title,
        company_name=job.company,
        job_description=job.description,
        resume_content=resume_result["resume_content"]
    )
    
    # Save files
    from pathlib import Path
    from .config import RESUMES_DIR
    
    company_clean = job.company.replace(" ", "_").replace("/", "_")[:20]
    title_clean = job.title.replace(" ", "_").replace("/", "_")[:20]
    job_folder = RESUMES_DIR / f"{company_clean}_{title_clean}"
    job_folder.mkdir(exist_ok=True)
    
    # Save resume
    resume_path = job_folder / "resume.txt"
    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(str(resume_result["resume_content"]))
    
    # Save cover letter
    cover_letter_path = job_folder / "cover_letter.txt"
    with open(cover_letter_path, "w", encoding="utf-8") as f:
        f.write(cover_letter_result["cover_letter"])
    
    print(f"\n Resume saved: {resume_path}")
    print(f"Cover letter saved: {cover_letter_path}")
    
    db.update_job_status(job.id, "processed")
    print(f"\n Application prepared for {job.title} at {job.company}")
    print("Review the generated files and apply manually.")

def stats_command(args):
    """Show statistics"""
    print("\n Job Hunter Statistics")
    print("=" * 50)
    
    stats = db.get_statistics()
    
    print(f"Total Jobs in Database: {stats['total_jobs']}")
    print(f"New Jobs (Unprocessed): {stats['new_jobs']}")
    print(f"Total Applications Sent: {stats['total_applications']}")
    print(f"Shortlisted: {stats['shortlisted']}")
    
    if stats['jobs_by_platform']:
        print("\nJobs by Platform:")
        for platform, count in stats['jobs_by_platform'].items():
            print(f"  {platform}: {count}")

def export_command(args):
    """Export job report"""
    print("\n Exporting Job Report")
    
    filename = args.filename if args.filename else "job_report.csv"
    filepath = db.export_to_csv(filename)
    
    print(f" Report exported to: {filepath}")

def main():
    """Main entry point"""
    print_banner()
    
    parser = argparse.ArgumentParser(description="Job Hunter Agent - Autonomous Job Search")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Setup command
    subparsers.add_parser("setup", help="Interactive setup wizard")
    
    # Run command (main autonomous mode)
    run_parser = subparsers.add_parser("run", help="Start autonomous job hunter (RECOMMENDED)")
    run_parser.add_argument("-i", "--immediate", action="store_true", help="Run search immediately")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for jobs (one-time)")
    search_parser.add_argument("-k", "--keywords", help="Comma-separated keywords")
    search_parser.add_argument("-l", "--location", help="Job location")
    search_parser.add_argument("-p", "--platform", help="Platform (linkedin/naukri/internshala/google)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List jobs")
    list_parser.add_argument("-s", "--status", help="Filter by status (new/applied/interview)")
    
    # Apply command
    apply_parser = subparsers.add_parser("apply", help="Prepare application for a job")
    apply_parser.add_argument("job_id", type=int, help="Job ID to apply for")
    
    # Stats command
    subparsers.add_parser("stats", help="Show statistics")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export job report")
    export_parser.add_argument("-f", "--filename", help="Output filename")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    commands = {
        "setup": setup_command,
        "run": run_command,
        "search": search_command,
        "list": list_command,
        "apply": apply_command,
        "stats": stats_command,
        "export": export_command
    }
    
    commands[args.command](args)

if __name__ == "__main__":
    main()
