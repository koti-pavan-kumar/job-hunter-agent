"""
Google Jobs Aggregator Scraper
"""
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote_plus

from .base import BaseScraper
from ..config import config
from ..database import JobListing

class GoogleJobsScraper(BaseScraper):
    """Scraper for Google Jobs (aggregates from multiple platforms)"""
    
    def __init__(self):
        super().__init__("Google Jobs")
        self.search_url = "https://www.google.com/search"
    
    def search_jobs(self, keywords: List[str], location: str = "", **kwargs) -> List[JobListing]:
        """Search Google for jobs"""
        jobs = []
        search_query = " ".join(keywords)
        
        # Build search query for jobs
        query = f"{search_query} internship jobs"
        if location:
            query += f" in {location}"
        
        params = {
            "q": query,
            "ibp": "htl;jobs",  # Google Jobs tab
            "htivrt": "jobs",
            "htichips": "date_posted:week"  # Last week
        }
        
        response = self._make_request(self.search_url, params=params)
        if not response:
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Google Jobs uses different structure
        job_cards = soup.find_all("div", class_="iFjolb")
        if not job_cards:
            job_cards = soup.find_all("li", class_="iFjolb")
        
        for card in job_cards:
            job = self._parse_job_card(card)
            if job:
                jobs.append(job)
        
        return jobs
    
    def _parse_job_card(self, card) -> Optional[JobListing]:
        """Parse a job card from Google Jobs"""
        try:
            # Extract job title
            title_elem = card.find("h3")
            title = title_elem.text.strip() if title_elem else ""
            
            # Extract company name
            company_elem = card.find("div", class_="BjJfJf")
            company = company_elem.text.strip() if company_elem else ""
            
            # Extract location
            location_elem = card.find("div", class_="Qk80Jf")
            location = location_elem.text.strip() if location_elem else ""
            
            # Extract job URL
            link_elem = card.find("a")
            url = link_elem["href"] if link_elem else ""
            
            # Extract posted date
            date_elem = card.find("div", class_="rdKbEf")
            posted_date = date_elem.text.strip() if date_elem else ""
            
            if not title:
                return None
            
            return self._parse_job_listing({
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "posted_date": posted_date,
                "job_type": "internship"
            })
            
        except Exception as e:
            return None
    
    def get_job_details(self, url: str) -> Optional[JobListing]:
        """Get detailed job information"""
        # Google Jobs typically links to the original job posting
        if not url:
            return None
        
        response = self._make_request(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        try:
            # Try to extract description from the page
            desc_elem = soup.find("div", class_="job-description")
            if not desc_elem:
                desc_elem = soup.find("section", class_="job-description")
            if not desc_elem:
                desc_elem = soup.find("div", {"class": lambda x: x and "description" in x.lower()})
            
            description = desc_elem.text.strip() if desc_elem else ""
            
            return self._parse_job_listing({
                "url": url,
                "description": description
            })
            
        except Exception as e:
            return None
    
    def search_with_custom_query(self, query: str) -> List[JobListing]:
        """Search with a custom query"""
        jobs = []
        
        params = {
            "q": query,
            "ibp": "htl;jobs",
            "htivrt": "jobs"
        }
        
        response = self._make_request(self.search_url, params=params)
        if not response:
            return jobs
        
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="iFjolb")
        
        for card in job_cards:
            job = self._parse_job_card(card)
            if job:
                jobs.append(job)
        
        return jobs
