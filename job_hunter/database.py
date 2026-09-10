"""
Job Hunter Agent - Database for Application Tracking
"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
from pathlib import Path
import json

from .config import DATA_DIR

@dataclass
class JobListing:
    """Represents a job listing"""
    id: Optional[int] = None
    platform: str = ""
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    url: str = ""
    salary: str = ""
    job_type: str = ""
    posted_date: str = ""
    scraped_date: str = ""
    status: str = "new"  # new, applied, interview, rejected, offered
    
    def to_dict(self):
        return self.__dict__

@dataclass
class Application:
    """Represents a job application"""
    id: Optional[int] = None
    job_id: int = 0
    applied_date: str = ""
    resume_path: str = ""
    cover_letter_path: str = ""
    status: str = "pending"  # pending, sent, viewed, shortlisted
    notes: str = ""
    
    def to_dict(self):
        return self.__dict__

class Database:
    """SQLite database for tracking jobs and applications"""
    
    def __init__(self):
        self.db_path = DATA_DIR / "jobs.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Job listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT,
                url TEXT UNIQUE,
                salary TEXT,
                job_type TEXT,
                posted_date TEXT,
                scraped_date TEXT,
                status TEXT DEFAULT 'new'
            )
        ''')
        
        # Applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                applied_date TEXT,
                resume_path TEXT,
                cover_letter_path TEXT,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (job_id) REFERENCES job_listings (id)
            )
        ''')
        
        # Daily logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                jobs_found INTEGER DEFAULT 0,
                applications_sent INTEGER DEFAULT 0,
                new_platforms INTEGER DEFAULT 0,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_job(self, job: JobListing) -> int:
        """Add a new job listing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO job_listings 
                (platform, title, company, location, description, url, salary, job_type, posted_date, scraped_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job.platform, job.title, job.company, job.location,
                job.description, job.url, job.salary, job.job_type,
                job.posted_date, job.scraped_date, job.status
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # URL already exists
            return -1
        finally:
            conn.close()
    
    def job_exists(self, url: str) -> bool:
        """Check if job already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM job_listings WHERE url = ?", (url,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def get_new_jobs(self) -> List[JobListing]:
        """Get all new jobs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM job_listings WHERE status = 'new' ORDER BY scraped_date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [JobListing(**dict(row)) for row in rows]
    
    def get_all_jobs(self, status: Optional[str] = None) -> List[JobListing]:
        """Get all jobs, optionally filtered by status"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM job_listings WHERE status = ? ORDER BY scraped_date DESC", (status,))
        else:
            cursor.execute("SELECT * FROM job_listings ORDER BY scraped_date DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [JobListing(**dict(row)) for row in rows]
    
    def update_job_status(self, job_id: int, status: str):
        """Update job status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE job_listings SET status = ? WHERE id = ?", (status, job_id))
        conn.commit()
        conn.close()
    
    def add_application(self, application: Application) -> int:
        """Add a new application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO applications 
            (job_id, applied_date, resume_path, cover_letter_path, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            application.job_id, application.applied_date,
            application.resume_path, application.cover_letter_path,
            application.status, application.notes
        ))
        conn.commit()
        app_id = cursor.lastrowid
        conn.close()
        return app_id
    
    def get_applications(self, job_id: Optional[int] = None) -> List[Application]:
        """Get applications, optionally filtered by job_id"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if job_id:
            cursor.execute("SELECT * FROM applications WHERE job_id = ?", (job_id,))
        else:
            cursor.execute("SELECT * FROM applications ORDER BY applied_date DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Application(**dict(row)) for row in rows]
    
    def update_application_status(self, app_id: int, status: str, notes: str = ""):
        """Update application status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if notes:
            cursor.execute("UPDATE applications SET status = ?, notes = ? WHERE id = ?", 
                          (status, notes, app_id))
        else:
            cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
        
        conn.commit()
        conn.close()
    
    def log_daily_stats(self, jobs_found: int, applications_sent: int, notes: str = ""):
        """Log daily statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute('''
            INSERT INTO daily_logs (date, jobs_found, applications_sent, notes)
            VALUES (?, ?, ?, ?)
        ''', (today, jobs_found, applications_sent, notes))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM job_listings")
        stats["total_jobs"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM job_listings WHERE status = 'new'")
        stats["new_jobs"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM applications")
        stats["total_applications"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'shortlisted'")
        stats["shortlisted"] = cursor.fetchone()[0]
        
        # Jobs by platform
        cursor.execute("SELECT platform, COUNT(*) FROM job_listings GROUP BY platform")
        stats["jobs_by_platform"] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def export_to_csv(self, filename: str = "job_report.csv"):
        """Export job listings to CSV"""
        import csv
        
        jobs = self.get_all_jobs()
        
        with open(DATA_DIR / filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Platform", "Title", "Company", "Location", "URL", "Status", "Scraped Date"])
            
            for job in jobs:
                writer.writerow([
                    job.id, job.platform, job.title, job.company,
                    job.location, job.url, job.status, job.scraped_date
                ])
        
        return DATA_DIR / filename

# Global database instance
db = Database()
