"""
Naukri Job Scraper
"""
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
import json
import re

from .base import BaseScraper
from ..config import config
from ..database import JobListing

class NaukriScraper(BaseScraper):
    """Scraper for Naukri jobs"""
    
    def __init__(self):
        super().__init__("Naukri")
        self.base_url = "https://www.naukri.com"
        self.search_url = "https://www.naukri.com/jobs-in-india"
    
    def search_jobs(self, keywords: List[str], location: str = "", **kwargs) -> List[JobListing]:
        """Search Naukri for jobs"""
        jobs = []
        search_query = "-".join(keywords).replace(" ", "-").lower()
        
        params = {
            "jobType": "internship" if config.preferences.job_type == "internship" else "",
            "experience": "0",  # Fresher
            "sort": "date"  # Sort by date
        }
        
        # Build search URL
        url = f"{self.base_url}/{search_query}-jobs"
        if location:
            url += f"-in-{location.lower().replace(' ', '-')}"
        
        response = self._make_request(url, params=params)
        if not response:
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="srp-grid__tuple")
        
        for card in job_cards:
            job = self._parse_job_card(card)
            if job:
                jobs.append(job)
        
        return jobs
    
    def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse a job card from Naukri"""
        try:
            # Extract job title
            title_elem = card.find("a", class_="title")
            title = title_elem.text.strip() if title_elem else ""
            url = title_elem["href"] if title_elem else ""
            
            # Extract company name
            company_elem = card.find("a", class_="subTitle")
            company = company_elem.text.strip() if company_elem else ""
            
            # Extract location
            location_elem = card.find("span", class_="location")
            location = location_elem.text.strip() if location_elem else ""
            
            # Extract experience
            exp_elem = card.find("span", class_="experience")
            experience = exp_elem.text.strip() if exp_elem else ""
            
            # Extract salary
            salary_elem = card.find("span", class_="salary")
            salary = salary_elem.text.strip() if salary_elem else ""
            
            if not title or not url:
                return None
            
            return self._parse_job_listing({
                "title": title,
                "company": company,
                "location": location,
                "url": url if url.startswith("http") else self.base_url + url,
                "salary": salary,
                "job_type": "internship" if "intern" in title.lower() else "full-time"
            })
            
        except Exception as e:
            return None
    
    def get_job_details(self, url: str) -> Optional[JobListing]:
        """Get detailed job information from Naukri"""
        response = self._make_request(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        try:
            # Extract job description
            desc_elem = soup.find("div", class_="dang-desk")
            description = desc_elem.text.strip() if desc_elem else ""
            
            # Extract key skills
            skills_elem = soup.find("div", class_="skills")
            skills = skills_elem.text.strip() if skills_elem else ""
            
            return self._parse_job_listing({
                "url": url,
                "description": description + "\n\nSkills: " + skills
            })
            
        except Exception as e:
            return None
