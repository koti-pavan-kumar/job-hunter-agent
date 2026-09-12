"""
Cookie-based Agent — Uses session cookies to read recommended jobs from platforms
No browser needed on the server — works on any cloud platform
"""
import requests
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class CookieAgent:
    """
    Agent that uses session cookies to access LinkedIn/Internshala/Unstop
    and extract recommended jobs.
    """
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.cookies_dir = self.data_dir / "cookies"
        self.cookies_dir.mkdir(exist_ok=True)
        self.jobs_dir = self.data_dir / "agent_jobs"
        self.jobs_dir.mkdir(exist_ok=True)
        
        self.skill_keywords = [
            "python", "machine learning", "data science", "ai", "ml",
            "deep learning", "nlp", "computer vision", "data analyst",
            "software engineer", "developer", "intern", "internship",
            "fresher", "junior", "backend", "frontend", "full stack",
            "langchain", "llm", "genai", "tensorflow", "pytorch"
        ]
        
        self.exclude_keywords = [
            "tax", "steuerberater", "accounting", "finance", "manufacturing",
            "hr", "human resource", "recruitment", "talent acquisition",
            "sales", "marketing", "operations", "legal", "insurance"
        ]

    # ====================== SAVE / LOAD COOKIES ======================

    def save_cookies(self, platform: str, cookie_string: str):
        """Save cookie string for a platform"""
        cookies_file = self.cookies_dir / f"{platform.lower()}_cookies.txt"
        cookies_file.write_text(cookie_string, encoding="utf-8")
    
    def get_cookies(self, platform: str) -> Optional[str]:
        """Load saved cookie string for a platform"""
        cookies_file = self.cookies_dir / f"{platform.lower()}_cookies.txt"
        if cookies_file.exists():
            return cookies_file.read_text(encoding="utf-8").strip()
        return None
    
    def get_cookie_status(self) -> Dict[str, bool]:
        """Check which platforms have cookies"""
        return {
            "LinkedIn": (self.cookies_dir / "linkedin_cookies.txt").exists(),
            "Internshala": (self.cookies_dir / "internshala_cookies.txt").exists(),
            "Unstop": (self.cookies_dir / "unstop_cookies.txt").exists()
        }

    # ====================== LINKEDIN ======================

    def extract_linkedin_jobs(self) -> List[Dict]:
        """Extract recommended jobs from LinkedIn using session cookies"""
        cookies = self.get_cookies("LinkedIn")
        if not cookies:
            print("  LinkedIn: No cookies saved")
            return []

        jobs = []
        try:
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie": cookies
            })

            # Search for relevant jobs in India
            url = "https://www.linkedin.com/guest-api/hi/search?keywords=python%20machine%20learning&location=India&f_TPR=r604800"
            response = session.get(url, timeout=30)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    for item in data.get("elements", [])[:30]:
                        job = item.get("jobPosting", {})
                        title = job.get("title", "")
                        company = job.get("companyName", "")
                        link = job.get("url", "")
                        location = job.get("location", "")
                        
                        if title and self._is_relevant(title):
                            jobs.append(self._create_job(
                                title=title,
                                company=company or "Unknown",
                                location=location or "India",
                                description=job.get("description", "")[:500],
                                url=link,
                                platform="LinkedIn"
                            ))
                except Exception:
                    pass

            # Also try scraping job list page
            response2 = session.get(
                "https://www.linkedin.com/jobs/search/?keywords=python+machine+learning&location=India&f_TPR=r604800",
                timeout=30
            )
            if response2.status_code == 200:
                # Extract from HTML
                for match in re.finditer(
                    r'<h3[^>]*class="[^"]*base-search-card__title[^"]*"[^>]*>([^<]+)</h3>.*?'
                    r'<h4[^>]*class="[^"]*base-search-card__subtitle[^"]*"[^>]*>([^<]+)</h4>.*?'
                    r'<a[^>]*href="([^"]+)"',
                    response2.text, re.DOTALL
                ):
                    title = match.group(1).strip()
                    company = match.group(2).strip()
                    link = match.group(3).strip()
                    if title and self._is_relevant(title):
                        jobs.append(self._create_job(
                            title=title, company=company,
                            location="India",
                            description="",
                            url=f"https://www.linkedin.com{link}" if link.startswith("/") else link,
                            platform="LinkedIn"
                        ))

            print(f"  LinkedIn: found {len(jobs)} relevant jobs")
        except Exception as e:
            print(f"  LinkedIn error: {e}")
        
        self._save_agent_jobs(jobs, "LinkedIn")
        return jobs

    # ====================== INTERNSHALA ======================

    def extract_internshala_jobs(self) -> List[Dict]:
        """Extract recommended jobs from Internshala using session cookies"""
        cookies = self.get_cookies("Internshala")
        if not cookies:
            print("  Internshala: No cookies saved")
            return []

        jobs = []
        try:
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml",
                "Cookie": cookies
            })

            # Try Internshala jobs page
            response = session.get("https://internshala.com/jobs", timeout=30)
            if response.status_code == 200:
                for match in re.finditer(
                    r'<h3[^>]*>\s*([^<]+?)\s*</h3>.*?'
                    r'<p[^>]*>\s*([^<]+?)\s*</p>',
                    response.text, re.DOTALL
                ):
                    title = match.group(1).strip()
                    company = match.group(2).strip()
                    if title and self._is_relevant(title):
                        jobs.append(self._create_job(
                            title=title, company=company,
                            location="India", description="",
                            url="https://internshala.com/jobs",
                            platform="Internshala"
                        ))

            # Also try API
            api = session.get(
                "https://internshala.com/api/v1/jobs?search=python+machine+learning",
                timeout=30
            )
            if api.status_code == 200:
                try:
                    for item in api.json().get("jobs", [])[:20]:
                        title = item.get("title", "")
                        company = item.get("company", {}).get("name", "")
                        if title and self._is_relevant(title):
                            jobs.append(self._create_job(
                                title=title, company=company,
                                location="India",
                                description=item.get("description", "")[:500],
                                url=f"https://internshala.com/jobs/{item.get('url', '')}",
                                platform="Internshala"
                            ))
                except Exception:
                    pass

            print(f"  Internshala: found {len(jobs)} relevant jobs")
        except Exception as e:
            print(f"  Internshala error: {e}")

        self._save_agent_jobs(jobs, "Internshala")
        return jobs

    # ====================== UNSTOP ======================

    def extract_unstop_jobs(self) -> List[Dict]:
        """Extract jobs from Unstop using session cookies"""
        cookies = self.get_cookies("Unstop")
        if not cookies:
            print("  Unstop: No cookies saved")
            return []

        jobs = []
        try:
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Cookie": cookies
            })

            # Unstop API
            response = session.get(
                "https://www.unstop.com/api/v2/opportunities?search=python+machine+learning&per_page=20",
                timeout=30
            )
            if response.status_code == 200:
                try:
                    for item in response.json().get("opportunities", [])[:20]:
                        title = item.get("title", "")
                        company = item.get("company", {}).get("name", "")
                        if title and self._is_relevant(title):
                            jobs.append(self._create_job(
                                title=title, company=company,
                                location="India",
                                description=item.get("description", "")[:500],
                                url=item.get("url", ""),
                                platform="Unstop"
                            ))
                except Exception:
                    pass

            print(f"  Unstop: found {len(jobs)} relevant jobs")
        except Exception as e:
            print(f"  Unstop error: {e}")

        self._save_agent_jobs(jobs, "Unstop")
        return jobs

    # ====================== SHARED ======================

    def _is_relevant(self, title: str) -> bool:
        t = title.lower()
        if any(k in t for k in self.exclude_keywords):
            return False
        return any(k in t for k in self.skill_keywords)

    def _create_job(self, title: str, company: str, location: str,
                    description: str, url: str, platform: str) -> Dict:
        return {
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "url": url,
            "platform": platform,
            "fetchedAt": datetime.now().isoformat()
        }

    def _save_agent_jobs(self, jobs: List[Dict], platform: str):
        """Append jobs to the per-platform JSON file"""
        if not jobs:
            return
        jobs_file = self.jobs_dir / f"{platform.lower()}_jobs.json"
        existing = []
        if jobs_file.exists():
            try:
                existing = json.loads(jobs_file.read_text(encoding='utf-8'))
            except Exception:
                existing = []
        existing.extend(jobs)
        jobs_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')

    def run_all(self) -> int:
        """Run all extractors, return total jobs found"""
        total = 0
        for extractor in [self.extract_linkedin_jobs, self.extract_internshala_jobs, self.extract_unstop_jobs]:
            total += len(extractor())
        return total
