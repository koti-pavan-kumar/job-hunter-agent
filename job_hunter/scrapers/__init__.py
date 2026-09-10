"""
Job Hunter Agent - Scrapers Package
"""
from .base import BaseScraper
from .linkedin import LinkedInScraper
from .naukri import NaukriScraper
from .internshala import InternshalaScraper
from .google_jobs import GoogleJobsScraper

__all__ = [
    "BaseScraper",
    "LinkedInScraper",
    "NaukriScraper",
    "InternshalaScraper",
    "GoogleJobsScraper"
]
