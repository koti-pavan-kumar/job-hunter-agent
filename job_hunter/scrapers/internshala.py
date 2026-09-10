"""
Internshala Job Scraper
"""
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
import json
import re

from .base import BaseScraper
from ..config import config
from ..database import JobListing

class InternshalaScraper(BaseScraper):
    """Scraper for Internshala internships"""
    
    def __init__(self):
        super().__init__("Internshala")
        self.base_url = "https://internshala.com"
        self.internship_url = "https://internshala.com/internships"
    
    def search_jobs(self, keywords: List[str], location: str = "", **kwargs) -> List[JobListing]:
        """Search Internshala for internships"""
        jobs = []
        search_query = "-".join(keywords).replace(" ", "-").lower()
        
        params = {
            "search": " ".join(keywords),
            "location": location or "work from home",
            "job_type": "internship"
        }
        
        response = self._make_request(self.internship_url, params=params)
        if not response:
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="individual_internship")
        
        for card in job_cards:
            job = self._parse_job_card(card)
            if job:
                jobs.append(job)
        
        return jobs
    
    def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse a job card from Internshala"""
        try:
            # Extract job title
            title_elem = card.find("h3", class_="heading_line")
            title = title_elem.text.strip() if title_elem else ""
            
            # Extract company name
            company_elem = card.find("p", class_="company-name")
            company = company_elem.text.strip() if company_elem else ""
            
            # Extract location
            location_elem = card.find("p", class_="location")
            location = location_elem.text.strip() if location_elem else ""
            
            # Extract stipend
            stipend_elem = card.find("span", class_="stipend")
            salary = stipend_elem.text.strip() if stipend_elem else ""
            
            # Extract job URL
            link_elem = card.find("a", class_="view_detail_button")
            url = link_elem["href"] if link_elem else ""
            if url and not url.startswith("http"):
                url = self.base_url + url
            
            # Extract posted date
            date_elem = card.find("div", class_="small")
            posted_date = date_elem.text.strip() if date_elem else ""
            
            if not title or not url:
                return None
            
            return self._parse_job_listing({
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "salary": salary,
                "posted_date": posted_date,
                "job_type": "internship"
            })
            
        except Exception as e:
            return None
    
    def get_job_details(self, url: str) -> Optional[JobListing]:
        """Get detailed job information from Internshala"""
        response = self._make_request(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        try:
            # Extract job description
            desc_elem = soup.find("div", class_="about_the_role")
            description = desc_elem.text.strip() if desc_elem else ""
            
            # Extract requirements
            req_elem = soup.find("div", class_="requirements")
            requirements = req_elem.text.strip() if req_elem else ""
            
            # Extract perks
            perks_elem = soup.find("div", class_="perks")
            perks = perks_elem.text.strip() if perks_elem else ""
            
            full_description = f"{description}\n\nRequirements:\n{requirements}\n\nPerks:\n{perks}"
            
            return self._parse_job_listing({
                "url": url,
                "description": full_description
            })
            
        except Exception as e:
            return None
