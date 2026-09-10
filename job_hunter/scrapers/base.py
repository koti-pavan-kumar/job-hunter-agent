"""
Base Scraper Class - Common functionality for all scrapers
"""
import requests
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
import logging
import time
import random

from ..config import config
from ..database import db, JobListing

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for job scrapers"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    
    @abstractmethod
    def search_jobs(self, keywords: List[str], location: str = "", **kwargs) -> List[JobListing]:
        """Search for jobs - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_job_details(self, url: str) -> Optional[JobListing]:
        """Get detailed job information - must be implemented by subclasses"""
        pass
    
    def scrape_and_store(self, keywords: List[str], location: str = "") -> List[JobListing]:
        """Scrape jobs and store in database"""
        logger.info(f"Scraping {self.platform_name} for: {keywords}")
        
        try:
            jobs = self.search_jobs(keywords, location)
            new_jobs = []
            
            for job in jobs:
                if not db.job_exists(job.url):
                    job_id = db.add_job(job)
                    if job_id > 0:
                        job.id = job_id
                        new_jobs.append(job)
                        logger.info(f"Added new job: {job.title} at {job.company}")
            
            logger.info(f"Found {len(new_jobs)} new jobs from {self.platform_name}")
            return new_jobs
            
        except Exception as e:
            logger.error(f"Error scraping {self.platform_name}: {e}")
            return []
    
    def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add random delay to avoid detection"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def _make_request(self, url: str, method: str = "GET", **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with error handling"""
        try:
            self._random_delay()
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def _parse_job_listing(self, data: Dict) -> JobListing:
        """Parse job data into JobListing object"""
        return JobListing(
            platform=self.platform_name,
            title=data.get("title", ""),
            company=data.get("company", ""),
            location=data.get("location", ""),
            description=data.get("description", ""),
            url=data.get("url", ""),
            salary=data.get("salary", ""),
            job_type=data.get("job_type", ""),
            posted_date=data.get("posted_date", ""),
            scraped_date=datetime.now().isoformat(),
            status="new"
        )
