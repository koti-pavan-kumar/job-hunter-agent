"""
Company Legitimacy Checker - Identifies red flags and suspicious companies
"""
from typing import Dict, List, Optional, Tuple
import re

from .config import config

class LegitimacyChecker:
    """Check company legitimacy and identify red flags"""
    
    def __init__(self):
        self.red_flags = config.legitimacy_checker.red_flags
        self.suspicious_domains = config.legitimacy_checker.suspicious_domains
        self.companies_to_avoid = config.legitimacy_checker.companies_to_avoid
    
    def check_company(self, company_name: str, job_description: str, 
                     company_url: str = "") -> Dict:
        """Comprehensive company legitimacy check"""
        
        result = {
            "is_legitimate": True,
            "risk_level": "low",  # low, medium, high
            "red_flags": [],
            "warnings": [],
            "recommendation": "proceed"
        }
        
        # Check 1: Known companies to avoid
        if company_name in self.companies_to_avoid:
            result["is_legitimate"] = False
            result["risk_level"] = "high"
            result["red_flags"].append(f"Company '{company_name}' is in the avoid list")
            result["recommendation"] = "skip"
            return result
        
        # Check 2: Domain analysis
        if company_url:
            domain_issues = self._check_domain(company_url)
            if domain_issues:
                result["red_flags"].extend(domain_issues)
                result["risk_level"] = "high"
        
        # Check 3: Job description analysis
        jd_issues = self._check_job_description(job_description)
        if jd_issues:
            result["warnings"].extend(jd_issues)
            if len(jd_issues) > 2:
                result["risk_level"] = "medium"
        
        # Check 4: Ed-tech/bootcamp detection
        edtech_issues = self._check_edtech_patterns(company_name, job_description, company_url)
        if edtech_issues:
            result["warnings"].extend(edtech_issues)
            result["risk_level"] = "medium"
        
        # Check 5: Payment requests
        payment_issues = self._check_payment_requests(job_description)
        if payment_issues:
            result["red_flags"].extend(payment_issues)
            result["risk_level"] = "high"
            result["recommendation"] = "skip"
        
        # Determine final recommendation
        if result["risk_level"] == "high":
            result["recommendation"] = "skip"
        elif result["risk_level"] == "medium":
            result["recommendation"] = "cautious"
        else:
            result["recommendation"] = "proceed"
        
        return result
    
    def _check_domain(self, company_url: str) -> List[str]:
        """Check domain for suspicious patterns"""
        issues = []
        
        # Extract domain from URL
        domain_match = re.search(r'https?://([^/]+)', company_url)
        if domain_match:
            domain = domain_match.group(1).lower()
            
            # Check for suspicious TLDs
            for suspicious in self.suspicious_domains:
                if domain.endswith(suspicious):
                    issues.append(f"Suspicious domain TLD: {domain} (ends with {suspicious})")
            
            # Check for subdomain patterns
            if domain.count('.') > 2:
                issues.append(f"Complex domain structure: {domain}")
        
        return issues
    
    def _check_job_description(self, job_description: str) -> List[str]:
        """Check job description for red flags"""
        issues = []
        
        jd_lower = job_description.lower()
        
        # Check for vague descriptions
        vague_phrases = [
            "various tasks",
            "other duties as assigned",
            "flexible",
            "dynamic environment",
            "fast-paced"
        ]
        
        vague_count = sum(1 for phrase in vague_phrases if phrase in jd_lower)
        if vague_count > 2:
            issues.append("Job description is vague with multiple generic phrases")
        
        # Check for unrealistic promises
        unrealistic_phrases = [
            "guaranteed job",
            "100% placement",
            "unlimited earnings",
            "quick money",
            "easy work"
        ]
        
        for phrase in unrealistic_phrases:
            if phrase in jd_lower:
                issues.append(f"Unrealistic promise detected: '{phrase}'")
        
        # Check for excessive requirements
        if "5+ years" in jd_lower and "intern" in jd_lower:
            issues.append("Excessive experience requirement for internship role")
        
        return issues
    
    def _check_edtech_patterns(self, company_name: str, job_description: str, 
                              company_url: str) -> List[str]:
        """Check for ed-tech/bootcamp patterns"""
        issues = []
        
        # Check company name
        edtech_keywords = [
            "academy", "institute", "school", "training", "learning",
            "education", "edutech", "edtech"
        ]
        
        company_lower = company_name.lower()
        for keyword in edtech_keywords:
            if keyword in company_lower:
                issues.append(f"Company name contains education-related keyword: '{keyword}'")
        
        # Check job description for ed-tech patterns
        jd_lower = job_description.lower()
        
        edtech_phrases = [
            "certificate of internship",
            "paid course",
            "training program",
            "skill development",
            "professional training"
        ]
        
        for phrase in edtech_phrases:
            if phrase in jd_lower:
                issues.append(f"Ed-tech pattern detected in JD: '{phrase}'")
        
        # Check website for ed-tech patterns
        if company_url:
            url_lower = company_url.lower()
            if "learn" in url_lower or "academy" in url_lower or "school" in url_lower:
                issues.append("URL contains education-related keywords")
        
        return issues
    
    def _check_payment_requests(self, job_description: str) -> List[str]:
        """Check for payment requests"""
        issues = []
        
        jd_lower = job_description.lower()
        
        payment_phrases = [
            "registration fee",
            "application fee",
            "processing fee",
            "security deposit",
            "training fee",
            "payment required"
        ]
        
        for phrase in payment_phrases:
            if phrase in jd_lower:
                issues.append(f"Payment request detected: '{phrase}'")
        
        return issues
    
    def get_risk_summary(self, check_result: Dict) -> str:
        """Get human-readable risk summary"""
        
        if check_result["recommendation"] == "skip":
            return "HIGH RISK: Skip this opportunity. Multiple red flags detected."
        elif check_result["recommendation"] == "cautious":
            return "MEDIUM RISK: Proceed with caution. Some warnings detected."
        else:
            return "LOW RISK: No significant issues detected. Proceed with standard checks."
    
    def get_detailed_report(self, check_result: Dict) -> str:
        """Get detailed legitimacy report"""
        
        report = "COMPANY LEGITIMACY REPORT\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Risk Level: {check_result['risk_level'].upper()}\n"
        report += f"Recommendation: {check_result['recommendation'].upper()}\n\n"
        
        if check_result["red_flags"]:
            report += "RED FLAGS:\n"
            for flag in check_result["red_flags"]:
                report += f"• {flag}\n"
            report += "\n"
        
        if check_result["warnings"]:
            report += "WARNINGS:\n"
            for warning in check_result["warnings"]:
                report += f"• {warning}\n"
            report += "\n"
        
        if not check_result["red_flags"] and not check_result["warnings"]:
            report += "No issues detected.\n"
        
        return report

# Global instance
legitimacy_checker = LegitimacyChecker()
