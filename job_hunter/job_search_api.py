"""
Job Search API - Uses multiple FREE APIs for job search
No authentication required for these APIs:
- Findwork.dev (tech jobs)
- Arbeitnow (global jobs)
- Remotive (remote jobs)
- Jobicy (remote jobs)
"""
import requests
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
import time
import re

class JobSearchAPI:
    """Real job search using multiple free APIs"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        # Tech keywords for filtering
        self.tech_keywords = [
            "python", "machine learning", "data science", "ai", "ml",
            "developer", "engineer", "software", "data", "analyst",
            "intern", "junior", "fresher", "backend", "frontend",
            "full stack", "react", "node", "java", "javascript",
            "typescript", "django", "fastapi", "flask", "sql",
            "cloud", "aws", "azure", "docker", "kubernetes",
            "automation", "devops", "mlops", "nlp", "computer vision",
            "deep learning", "tensorflow", "pytorch", "langchain", "llm"
        ]
    
    def search_findwork(self, keywords: List[str]) -> List[Dict]:
        """Search Findwork API (free, no auth needed)"""
        jobs = []
        search_query = " ".join(keywords[:3])
        
        try:
            url = "https://findwork.dev/api/jobs/"
            params = {"search": search_query, "order_by": "relevance", "remote": "true"}
            
            response = self.session.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get("results", []):
                    parsed = self._parse_findwork_job(job)
                    if parsed:
                        jobs.append(parsed)
                print(f"  Findwork: Found {len(jobs)} jobs")
            else:
                print(f"  Findwork: Status {response.status_code}")
        except Exception as e:
            print(f"  Findwork error: {e}")
        
        return jobs
    
    def search_arbeitnow(self, keywords: List[str]) -> List[Dict]:
        """Search Arbeitnow API (free, no auth needed)"""
        jobs = []
        
        try:
            url = "https://www.arbeitnow.com/api/job-board-api"
            params = {"search": " ".join(keywords[:3])}
            
            response = self.session.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get("data", []):
                    parsed = self._parse_arbeitnow_job(job)
                    if parsed and self._is_tech_job(parsed):
                        jobs.append(parsed)
                print(f"  Arbeitnow: Found {len(jobs)} tech jobs")
            else:
                print(f"  Arbeitnow: Status {response.status_code}")
        except Exception as e:
            print(f"  Arbeitnow error: {e}")
        
        return jobs
    
    def search_remotive(self, keywords: List[str]) -> List[Dict]:
        """Search Remotive API (free, remote jobs)"""
        jobs = []
        
        try:
            url = "https://remotive.com/api/remote-jobs"
            params = {"search": " ".join(keywords[:3])}
            
            response = self.session.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get("jobs", []):
                    parsed = self._parse_remotive_job(job)
                    if parsed and self._is_tech_job(parsed):
                        jobs.append(parsed)
                print(f"  Remotive: Found {len(jobs)} tech jobs")
            else:
                print(f"  Remotive: Status {response.status_code}")
        except Exception as e:
            print(f"  Remotive error: {e}")
        
        return jobs
    
    def search_jobicy(self, keywords: List[str]) -> List[Dict]:
        """Search Jobicy API (free, remote jobs)"""
        jobs = []
        
        try:
            url = "https://jobicy.com/api/v2/remote-jobs"
            params = {"count": 50, "tag": keywords[0] if keywords else "python"}
            
            response = self.session.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get("jobs", []):
                    parsed = self._parse_jobicy_job(job)
                    if parsed and self._is_tech_job(parsed):
                        jobs.append(parsed)
                print(f"  Jobicy: Found {len(jobs)} tech jobs")
            else:
                print(f"  Jobicy: Status {response.status_code}")
        except Exception as e:
            print(f"  Jobicy error: {e}")
        
        return jobs
    
    def _is_tech_job(self, job: Dict) -> bool:
        """Check if job is tech-related"""
        text = (job.get("title", "") + " " + job.get("description", "")).lower()
        return any(kw in text for kw in self.tech_keywords)
    
    def search_all_sources(self, keywords: List[str]) -> List[Dict]:
        """Search all free API sources"""
        print("\nSearching job sources...")
        
        all_jobs = []
        all_jobs.extend(self.search_findwork(keywords))
        time.sleep(1)
        all_jobs.extend(self.search_arbeitnow(keywords))
        time.sleep(1)
        all_jobs.extend(self.search_remotive(keywords))
        time.sleep(1)
        all_jobs.extend(self.search_jobicy(keywords))
        
        # Deduplicate by URL
        seen_urls = set()
        unique_jobs = []
        for job in all_jobs:
            url = job.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_jobs.append(job)
        
        print(f"\nTotal unique tech jobs found: {len(unique_jobs)}")
        return unique_jobs
    
    def _parse_findwork_job(self, raw: Dict) -> Optional[Dict]:
        """Parse Findwork job"""
        try:
            title = raw.get("role", "")
            company = raw.get("company_name", "")
            url = raw.get("url", "")
            description = raw.get("text", "") or raw.get("description", "")
            location = raw.get("location", "")
            
            if not title or not url:
                return None
            
            return self._create_job(title, company, location or "Remote", description, url, "Findwork")
        except:
            return None
    
    def _parse_arbeitnow_job(self, raw: Dict) -> Optional[Dict]:
        """Parse Arbeitnow job"""
        try:
            title = raw.get("title", "")
            company = raw.get("company_name", "")
            url = raw.get("url", "")
            description = raw.get("description", "")
            location = raw.get("location", "")
            remote = raw.get("remote", False)
            
            if not title or not url:
                return None
            
            if remote:
                location = "Remote" + (f" ({location})" if location else "")
            
            return self._create_job(title, company, location, description, url, "Arbeitnow")
        except:
            return None
    
    def _parse_remotive_job(self, raw: Dict) -> Optional[Dict]:
        """Parse Remotive job"""
        try:
            title = raw.get("title", "")
            company = raw.get("company_name", "")
            url = raw.get("url", "")
            description = raw.get("description", "")
            location = raw.get("candidate_required_location", "Remote")
            
            if not title or not url:
                return None
            
            return self._create_job(title, company, location, description, url, "Remotive")
        except:
            return None
    
    def _parse_jobicy_job(self, raw: Dict) -> Optional[Dict]:
        """Parse Jobicy job"""
        try:
            title = raw.get("jobTitle", "")
            company = raw.get("companyName", "")
            url = raw.get("url", "")
            description = raw.get("jobDescription", "")
            location = raw.get("jobGeo", "Remote")
            
            if not title or not url:
                return None
            
            return self._create_job(title, company, location, description, url, "Jobicy")
        except:
            return None
    
    def _create_job(self, title: str, company: str, location: str,
                    description: str, url: str, platform: str) -> Dict:
        """Create a standardized job object"""
        job_id = hashlib.md5(url.encode()).hexdigest()[:12]
        
        job_type = "full-time"
        if "intern" in title.lower():
            job_type = "internship"
        elif "contract" in title.lower() or "freelance" in title.lower():
            job_type = "contract"
        elif "junior" in title.lower() or "entry" in title.lower():
            job_type = "entry-level"
        
        # Clean description
        description = re.sub(r'<[^>]+>', '', description)
        description = re.sub(r'\s+', ' ', description).strip()
        
        return {
            "id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "description": description[:2000],
            "url": url,
            "salary": "",
            "job_type": job_type,
            "posted_date": "",
            "scraped_date": datetime.now().isoformat(),
            "platform": platform,
            "status": "new"
        }
    
    def save_jobs_to_json(self, jobs: List[Dict]) -> str:
        """Save jobs to JSON file"""
        jobs_file = self.data_dir / "jobs.json"
        
        existing_jobs = []
        if jobs_file.exists():
            with open(jobs_file, "r", encoding="utf-8") as f:
                existing_jobs = json.load(f)
        
        existing_urls = {job["url"] for job in existing_jobs}
        new_jobs = [job for job in jobs if job["url"] not in existing_urls]
        
        all_jobs = existing_jobs + new_jobs
        
        with open(jobs_file, "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(new_jobs)} new jobs to {jobs_file}")
        return str(jobs_file)
    
    def get_jobs_from_json(self) -> List[Dict]:
        """Load jobs from JSON file"""
        jobs_file = self.data_dir / "jobs.json"
        
        if jobs_file.exists():
            with open(jobs_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        return []


# Global instance
job_search_api = JobSearchAPI()
