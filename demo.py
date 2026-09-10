"""
Demo Script - Job Hunter Agent
This script demonstrates how to use the Job Hunter Agent
"""

import sys
from job_hunter.config import config
from job_hunter.database import db
from job_hunter.resume_generator import resume_generator
from job_hunter.scheduler import scheduler

def demo_setup():
    """Demo: Setup configuration"""
    print("\n1. Setting up configuration...")
    
    # Update resume info
    config.update_resume(
        name="John Doe",
        email="john.doe@email.com",
        phone="+91 9876543210",
        linkedin_url="linkedin.com/in/johndoe",
        github_url="github.com/johndoe",
        portfolio_url="johndoe.dev",
        summary="Third-year CS student passionate about AI/ML with experience in Python and data science.",
        skills=["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Data Analysis", "SQL", "Git"],
        education=[
            {
                "degree": "Bachelor of Technology in Computer Science",
                "institution": "ABC College of Engineering",
                "year": "2022-2026",
                "cgpa": "8.5"
            }
        ],
        projects=[
            {
                "title": "AI Chatbot",
                "description": "Built an AI-powered chatbot using NLP and deep learning",
                "technologies": "Python, TensorFlow, Flask",
                "link": "github.com/johndoe/chatbot"
            },
            {
                "title": "Movie Recommendation System",
                "description": "Developed a recommendation engine using collaborative filtering",
                "technologies": "Python, Pandas, Scikit-learn",
                "link": "github.com/johndoe/recommender"
            }
        ],
        certifications=["Google AI/ML Certificate", "AWS Cloud Practitioner"]
    )
    
    # Update job preferences
    config.update_preferences(
        keywords=["AI", "ML", "Machine Learning", "Python", "Data Science", "Internship"],
        locations=["Remote", "Bangalore", "Hyderabad", "Pune"],
        job_type="internship",
        remote=True
    )
    
    print("   Configuration saved!")

def demo_database():
    """Demo: Database operations"""
    print("\n2. Testing database...")
    
    # Check statistics
    stats = db.get_statistics()
    print(f"   Total jobs in database: {stats['total_jobs']}")
    print(f"   New jobs: {stats['new_jobs']}")
    print(f"   Applications sent: {stats['total_applications']}")

def demo_resume_generation():
    """Demo: Resume generation"""
    print("\n3. Generating sample resume...")
    
    # Create a sample job
    from job_hunter.database import JobListing
    from datetime import datetime
    
    sample_job = JobListing(
        id=999,
        platform="LinkedIn",
        title="AI/ML Intern",
        company="Tech Corp",
        location="Bangalore",
        description="Looking for an AI/ML intern with Python, TensorFlow, and data analysis skills.",
        url="https://linkedin.com/jobs/123456",
        job_type="internship",
        scraped_date=datetime.now().isoformat()
    )
    
    # Generate resume
    resume_path = resume_generator.generate_resume(sample_job)
    print(f"   Resume generated: {resume_path}")
    
    # Generate cover letter
    cover_letter_path = resume_generator.save_cover_letter(sample_job)
    print(f"   Cover letter generated: {cover_letter_path}")

def demo_scheduler():
    """Demo: Scheduler status"""
    print("\n4. Scheduler information...")
    print("   Scheduler is ready to run.")
    print("   It will search jobs at 8:00 AM and 6:00 PM daily.")
    print("   Use 'python -m job_hunter run' to start the scheduler.")

def main():
    """Run demo"""
    print("=" * 60)
    print("JOB HUNTER AGENT - DEMO")
    print("=" * 60)
    
    print("\nThis demo shows the main features of Job Hunter Agent.")
    print("In real usage, you would run: python -m job_hunter setup")
    print("=" * 60)
    
    try:
        demo_setup()
        demo_database()
        demo_resume_generation()
        demo_scheduler()
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run 'python -m job_hunter setup' for interactive setup")
        print("2. Run 'python -m job_hunter search' to find jobs")
        print("3. Run 'python -m job_hunter run --immediate' to start scheduler")
        print("4. Run 'python -m job_hunter list' to see all jobs")
        print("5. Run 'python -m job_hunter apply <job_id>' to prepare application")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
