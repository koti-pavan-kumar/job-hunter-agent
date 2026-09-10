"""
LinkedIn Job Scraper
"""
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
import json
import re

from .base import BaseScraper
from ..config import config
from ..database import JobListing

class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn jobs"""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    def search_jobs(self, keywords: List[str], location: str = "", **kwargs) -> List[JobListing]:
        """Search LinkedIn for jobs"""
        jobs = []
        search_query = " ".join(keywords)
        
        params = {
            "keywords": search_query,
            "location": location or "India",
            "f_TPR": "r604800",  # Last week
            "f_E": "2%2C3",  # Entry level, Associate
            "position": 1,
            "pageNum": 0,
            "start": 0
        }
        
        # Try to fetch multiple pages
        for page in range(3):  # Get up to 3 pages
            params["start"] = page * 25
            
            response = self._make_request(self.base_url, params=params)
            if not response:
                break
            
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("li")
            
            if not job_cards:
                break
            
            for card in job_cards:
                job = self._parse_job_card(card)
                if job:
                    jobs.append(job)
        
        return jobs
    
    def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse a job card from LinkedIn"""
        try:
            # Extract job title
            title_elem = card.find("h3", class_="base-search-card__title")
            title = title_elem.text.strip() if title_elem else ""
            
            # Extract company name
            company_elem = card.find("h4", class_="base-search-card__subtitle")
            company = company_elem.text.strip() if company_elem else ""
            
            # Extract location
            location_elem = card.find("span", class_="job-search-card__location")
            location = location_elem.text.strip() if location_elem else ""
            
            # Extract job URL
            link_elem = card.find("a", class_="base-card__full-link")
            url = link_elem["href"].split("?")[0] if link_elem else ""
            
            # Extract posted date
            date_elem = card.find("time")
            posted_date = date_elem.get("datetime", "") if date_elem else ""
            
            if not title or not url:
                return None
            
            return self._parse_job_listing({
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "posted_date": posted_date,
                "job_type": "internship" if "intern" in title.lower() else "full-time"
            })
            
        except Exception as e:
            return None
    
    def get_job_details(self, url: str) -> Optional[JobListing]:
        """Get detailed job information from LinkedIn"""
        response = self._make_request(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        try:
            # Extract job description
            desc_elem = soup.find("div", class_="show-more-less-html__markup")
            description = desc_elem.text.strip() if desc_elem else ""
            
            # Extract salary if available
            salary_elem = soup.find("div", class_="salary")
            salary = salary_elem.text.strip() if salary_elem else ""
            
            return self._parse_job_listing({
                "url": url,
                "description": description,
                "salary": salary
            })
            
        except Exception as e:
            return None
