"""
Browser Automation Agent - Logs into job platforms and extracts recommended jobs
Uses Playwright for browser automation with user-controlled login
"""
import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

# Try to import playwright
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright && playwright install chromium")


class BrowserAgent:
    """AI Agent that automates browser to check job recommendations"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.sessions_dir = self.data_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        self.jobs_dir = self.data_dir / "agent_jobs"
        self.jobs_dir.mkdir(exist_ok=True)
        
        # Pavan's skill keywords
        self.skill_keywords = [
            "python", "machine learning", "data science", "ai", "ml",
            "deep learning", "nlp", "computer vision", "data analyst",
            "software engineer", "developer", "intern", "internship",
            "fresher", "junior", "backend", "frontend", "full stack",
            "langchain", "llm", "genai", "tensorflow", "pytorch"
        ]
    
    async def login_linkedin(self) -> bool:
        """Open browser for user to login to LinkedIn"""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright not available")
            return False
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                storage_state=str(self.sessions_dir / "linkedin.json") 
                if (self.sessions_dir / "linkedin.json").exists() else None
            )
            page = await context.new_page()
            
            await page.goto("https://www.linkedin.com/login")
            print("\n" + "="*60)
            print("LINKEDIN LOGIN")
            print("="*60)
            print("1. Login to your LinkedIn account in the browser")
            print("2. After login, come back here and press Enter")
            print("="*60)
            
            input("\nPress Enter after logging in to LinkedIn...")
            
            # Save session
            await context.storage_state(path=str(self.sessions_dir / "linkedin.json"))
            print("✅ LinkedIn session saved!")
            
            await browser.close()
            return True
    
    async def login_internshala(self) -> bool:
        """Open browser for user to login to Internshala"""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright not available")
            return False
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                storage_state=str(self.sessions_dir / "internshala.json")
                if (self.sessions_dir / "internshala.json").exists() else None
            )
            page = await context.new_page()
            
            await page.goto("https://internshala.com/login")
            print("\n" + "="*60)
            print("INTERNSHALA LOGIN")
            print("="*60)
            print("1. Login to your Internshala account in the browser")
            print("2. After login, come back here and press Enter")
            print("="*60)
            
            input("\nPress Enter after logging in to Internshala...")
            
            await context.storage_state(path=str(self.sessions_dir / "internshala.json"))
            print("✅ Internshala session saved!")
            
            await browser.close()
            return True
    
    async def login_unstop(self) -> bool:
        """Open browser for user to login to Unstop"""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright not available")
            return False
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                storage_state=str(self.sessions_dir / "unstop.json")
                if (self.sessions_dir / "unstop.json").exists() else None
            )
            page = await context.new_page()
            
            await page.goto("https://unstop.com/login")
            print("\n" + "="*60)
            print("UNSTOP LOGIN")
            print("="*60)
            print("1. Login to your Unstop account in the browser")
            print("2. After login, come back here and press Enter")
            print("="*60)
            
            input("\nPress Enter after logging in to Unstop...")
            
            await context.storage_state(path=str(self.sessions_dir / "unstop.json"))
            print("✅ Unstop session saved!")
            
            await browser.close()
            return True
    
    async def extract_linkedin_jobs(self) -> List[Dict]:
        """Extract recommended jobs from LinkedIn"""
        jobs = []
        session_file = self.sessions_dir / "linkedin.json"
        
        if not session_file.exists():
            print("❌ LinkedIn not logged in. Run login first.")
            return jobs
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(session_file))
            page = await context.new_page()
            
            try:
                # Go to LinkedIn jobs page
                await page.goto("https://www.linkedin.com/jobs/", timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Check if logged in
                if "login" in page.url:
                    print("❌ LinkedIn session expired. Please login again.")
                    await browser.close()
                    return jobs
                
                # Search for relevant jobs
                search_url = "https://www.linkedin.com/jobs/search/?keywords=python%20machine%20learning%20data%20science&location=India&f_TPR=r604800"
                await page.goto(search_url, timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Extract job cards
                job_cards = await page.query_selector_all(".job-card-container")
                
                for card in job_cards[:20]:
                    try:
                        title_elem = await card.query_selector(".job-card-list__title")
                        company_elem = await card.query_selector(".job-card-container__primary-description")
                        link_elem = await card.query_selector("a")
                        
                        if title_elem and link_elem:
                            title = await title_elem.inner_text()
                            company = await company_elem.inner_text() if company_elem else "Unknown"
                            link = await link_elem.get_attribute("href")
                            
                            if link and not link.startswith("http"):
                                link = "https://www.linkedin.com" + link
                            
                            jobs.append(self._create_job(
                                title=title.strip(),
                                company=company.strip(),
                                location="India/Remote",
                                description=f"LinkedIn job at {company}",
                                url=link or "",
                                platform="LinkedIn"
                            ))
                    except Exception as e:
                        continue
                
                print(f"  LinkedIn: Found {len(jobs)} jobs")
                
            except Exception as e:
                print(f"  LinkedIn error: {e}")
            
            await browser.close()
        
        return jobs
    
    async def extract_internshala_jobs(self) -> List[Dict]:
        """Extract recommended jobs from Internshala"""
        jobs = []
        session_file = self.sessions_dir / "internshala.json"
        
        if not session_file.exists():
            print("❌ Internshala not logged in. Run login first.")
            return jobs
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(session_file))
            page = await context.new_page()
            
            try:
                # Go to Internshala recommended jobs
                await page.goto("https://internshala.com/jobs", timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Check if logged in
                if "login" in page.url:
                    print("❌ Internshala session expired. Please login again.")
                    await browser.close()
                    return jobs
                
                # Extract job cards
                job_cards = await page.query_selector_all(".job_card")
                
                for card in job_cards[:20]:
                    try:
                        title_elem = await card.query_selector("h3")
                        company_elem = await card.query_selector(".company-name")
                        link_elem = await card.query_selector("a")
                        
                        if title_elem and link_elem:
                            title = await title_elem.inner_text()
                            company = await company_elem.inner_text() if company_elem else "Unknown"
                            link = await link_elem.get_attribute("href")
                            
                            if link and not link.startswith("http"):
                                link = "https://internshala.com" + link
                            
                            jobs.append(self._create_job(
                                title=title.strip(),
                                company=company.strip(),
                                location="India",
                                description=f"Internshala job at {company}",
                                url=link or "",
                                platform="Internshala"
                            ))
                    except Exception as e:
                        continue
                
                print(f"  Internshala: Found {len(jobs)} jobs")
                
            except Exception as e:
                print(f"  Internshala error: {e}")
            
            await browser.close()
        
        return jobs
    
    async def extract_unstop_jobs(self) -> List[Dict]:
        """Extract recommended jobs from Unstop"""
        jobs = []
        session_file = self.sessions_dir / "unstop.json"
        
        if not session_file.exists():
            print("❌ Unstop not logged in. Run login first.")
            return jobs
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(session_file))
            page = await context.new_page()
            
            try:
                # Go to Unstop jobs/opportunities
                await page.goto("https://unstop.com/opportunities", timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Check if logged in
                if "login" in page.url:
                    print("❌ Unstop session expired. Please login again.")
                    await browser.close()
                    return jobs
                
                # Extract opportunity cards
                cards = await page.query_selector_all(".opportunity-card")
                
                for card in cards[:20]:
                    try:
                        title_elem = await card.query_selector("h3, .title")
                        company_elem = await card.query_selector(".company")
                        link_elem = await card.query_selector("a")
                        
                        if title_elem and link_elem:
                            title = await title_elem.inner_text()
                            company = await company_elem.inner_text() if company_elem else "Unknown"
                            link = await link_elem.get_attribute("href")
                            
                            if link and not link.startswith("http"):
                                link = "https://unstop.com" + link
                            
                            jobs.append(self._create_job(
                                title=title.strip(),
                                company=company.strip(),
                                location="India",
                                description=f"Unstop opportunity at {company}",
                                url=link or "",
                                platform="Unstop"
                            ))
                    except Exception as e:
                        continue
                
                print(f"  Unstop: Found {len(jobs)} jobs")
                
            except Exception as e:
                print(f"  Unstop error: {e}")
            
            await browser.close()
        
        return jobs
    
    def _is_relevant(self, title: str, description: str = "") -> bool:
        """Check if job is relevant to skills"""
        text = (title + " " + description).lower()
        return any(kw in text for kw in self.skill_keywords)
    
    def _create_job(self, title: str, company: str, location: str,
                    description: str, url: str, platform: str) -> Dict:
        """Create standardized job object"""
        job_id = hashlib.md5(url.encode()).hexdigest()[:12]
        
        job_type = "full-time"
        if "intern" in title.lower():
            job_type = "internship"
        elif "fresher" in title.lower() or "junior" in title.lower():
            job_type = "entry-level"
        
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
    
    def save_jobs(self, jobs: List[Dict], platform: str) -> str:
        """Save jobs to JSON file"""
        jobs_file = self.jobs_dir / f"{platform.lower()}_jobs.json"
        
        existing_jobs = []
        if jobs_file.exists():
            with open(jobs_file, "r", encoding="utf-8") as f:
                existing_jobs = json.load(f)
        
        existing_urls = {job["url"] for job in existing_jobs}
        new_jobs = [job for job in jobs if job["url"] not in existing_urls]
        
        all_jobs = existing_jobs + new_jobs
        
        with open(jobs_file, "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(new_jobs)} new {platform} jobs")
        return str(jobs_file)
    
    def get_all_agent_jobs(self) -> List[Dict]:
        """Get all jobs found by the agent"""
        all_jobs = []
        
        for jobs_file in self.jobs_dir.glob("*_jobs.json"):
            with open(jobs_file, "r", encoding="utf-8") as f:
                all_jobs.extend(json.load(f))
        
        # Deduplicate
        seen_urls = set()
        unique_jobs = []
        for job in all_jobs:
            if job["url"] not in seen_urls:
                seen_urls.add(job["url"])
                unique_jobs.append(job)
        
        return unique_jobs
    
    def check_login_status(self) -> Dict[str, bool]:
        """Check which platforms are logged in"""
        status = {
            "LinkedIn": (self.sessions_dir / "linkedin.json").exists(),
            "Internshala": (self.sessions_dir / "internshala.json").exists(),
            "Unstop": (self.sessions_dir / "unstop.json").exists()
        }
        return status


# Global instance
browser_agent = BrowserAgent()
