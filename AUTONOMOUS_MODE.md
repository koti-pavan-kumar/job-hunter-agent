# 🤖 Autonomous Job Hunter Agent

## How It Works (Fully Automatic!)

Your Job Hunter Agent is now **fully autonomous**. Here's what it does automatically:

### **Daily Schedule**
- **8:00 AM** - Searches all platforms (LinkedIn, Naukri, Internshala, Google Jobs)
- **6:00 PM** - Searches again for new postings

### **Automatic Process**
1. **Searches** for jobs matching your skills (AI, ML, Data Science, Python)
2. **Checks** company legitimacy (filters out scams)
3. **Assesses** job fit (only processes jobs with 4+ fit score)
4. **Generates** tailored resume for each matching job
5. **Generates** cover letter in .docx format
6. **Saves** everything in organized folders
7. **Logs** everything for your review

### **Your Only Job**
1. **Check** the `job_hunter/resumes/` folder
2. **Review** the generated resumes
3. **Apply** to the ones you like when you have time

---

## 🚀 How to Start

### **Option 1: Windows Batch File (Easiest)**
```bash
# Double-click this file:
start_autonomous.bat
```

### **Option 2: PowerShell (Windows)**
```powershell
.\start_autonomous.ps1
```

### **Option 3: Bash Script (Linux/Mac)**
```bash
./start_autonomous.sh
```

### **Option 4: Direct Command**
```bash
python -m job_hunter run --immediate
```

---

## 📁 What Gets Generated

### **Folder Structure**
```
job_hunter/resumes/
├── Tech_Corp_ML_Engineer/
│   ├── resume.txt
│   ├── cover_letter.txt
│   ├── job_details.txt
│   └── bridging_notes.txt (if needed)
├── Google_Data_Analyst/
│   ├── resume.txt
│   ├── cover_letter.txt
│   └── job_details.txt
└── ...
```

### **Files Generated**

| File | Description |
|------|-------------|
| `resume.txt` | Tailored resume for that specific job |
| `cover_letter.txt` | Professional cover letter |
| `job_details.txt` | Job information and fit score |
| `bridging_notes.txt` | What to say in interview (if needed) |

---

## 📊 Daily Summary

After each search, you'll see a summary like this:

```
============================================================
DAILY JOB SEARCH SUMMARY
============================================================
Date: 2026-09-10 08:15:30

STATISTICS:
• Jobs Found: 15
• Resumes Generated: 8
• Companies Checked: 15
• Legitimate Jobs: 8
• Skipped Jobs: 7

NEXT STEPS:
1. Check 'job_hunter/resumes/' folder for generated resumes
2. Review each resume and cover letter
3. Apply to the ones you like when you have time

============================================================
```

---

## 🎯 What You Need to Do

### **Daily Routine (5-10 minutes)**

**Morning:**
1. Check the `job_hunter/resumes/` folder
2. See what new resumes were generated overnight
3. Note down which ones you want to apply to

**Evening:**
1. Check the folder again
2. Apply to 2-3 jobs you like (when you have time)

**Weekend:**
1. Review all generated resumes
2. Apply to your top 5-10 choices

### **That's It!**
- No manual searching
- No resume writing
- No cover letter writing
- Just review and apply

---

## 🔧 Customization

### **Change Search Keywords**
Edit `job_hunter/data/config.json`:
```json
{
  "preferences": {
    "keywords": ["AI", "ML", "Machine Learning", "Data Science", "Python"],
    "locations": ["Remote", "Bangalore", "Hyderabad", "Chennai", "Pune"]
  }
}
```

### **Change Search Times**
Edit `job_hunter/scheduler.py`:
```python
# Change from 8 AM and 6 PM to your preferred times
schedule.every().day.at("09:00").do(self.autonomous_job_search)
schedule.every().day.at("19:00").do(self.autonomous_job_search)
```

### **Change Max Applications**
Edit `job_hunter/data/config.json`:
```json
{
  "preferences": {
    "max_applications_per_day": 15
  }
}
```

---

## 📋 Sample Generated Resume

Here's what a generated resume looks like:

```
Pavan Kumar Koti
+91 7893600187 | kotipavankumar12@gmail.com | linkedin.com/in/pavan-kumar-koti-200b4438b | github.com/koti-pavan-kumar/

================================================================================
OBJECTIVE
================================================================================

Motivated Artificial Intelligence & Machine Learning student at Pace Institute 
seeking a ML Engineer position at Tech Corp to apply my skills in Python, 
Machine Learning, LLMs, and Agentic AI. With hands-on experience in production-grade 
projects including LLM systems, ensemble ML, and computer vision, I bring both 
technical depth and a commitment to continuous learning.

================================================================================
EDUCATION
================================================================================

B.Tech — Artificial Intelligence & Machine Learning
Pace Institute of Technology & Sciences, Ongole, AP | 2025–2028
CGPA: 8.2/10 | Top 20% of class

Diploma — Computer Science & Engineering
Rise Krishna Sai Polytechnic College, Ongole, AP | 2022–2025
CGPA: 9.1/10

... (and so on)
```

---

## 🎯 Key Features

### **1. Automatic Skill Matching**
- Analyzes job descriptions
- Matches with your skills
- Only processes jobs with 4+ fit score

### **2. Company Legitimacy Checking**
- Detects scam companies
- Filters out ed-tech bootlegs
- Checks for red flags

### **3. Honest Bridging System**
- Identifies skills you're learning
- Adds proper labels (fundamentals, learning)
- Prepares interview notes

### **4. Role-Based Project Selection**
- Automatically selects best projects
- Orders them by relevance
- Frames bullets for the role

### **5. ATS Optimization**
- Exact keyword matching
- One-page format
- Proper formatting

---

## ❓ FAQ

### **Q: How do I know when new resumes are generated?**
A: Check the `job_hunter/resumes/` folder. New folders appear with company names.

### **Q: Can I run it on my phone?**
A: No, it needs to run on your PC. But you can check the results from your phone.

### **Q: What if I want to stop it?**
A: Press `Ctrl+C` in the terminal window.

### **Q: Can I change the search times?**
A: Yes, edit the `scheduler.py` file.

### **Q: What if a job is not a good fit?**
A: The system automatically skips it (low fit score).

### **Q: Can I add more skills?**
A: Yes, edit the `config.py` file.

---

## 🚨 Important Notes

1. **Keep the terminal running** - The scheduler needs to stay open
2. **Check daily** - New resumes appear twice a day
3. **Review before applying** - Always check the generated content
4. **Apply manually** - The agent prepares, you apply
5. **Respect platform rules** - Don't spam

---

## 🎯 Quick Commands

```bash
# Start autonomous mode
python -m job_hunter run --immediate

# Check what's been generated
dir job_hunter/resumes\

# View statistics
python -m job_hunter stats

# List all jobs
python -m job_hunter list

# Stop the scheduler
Press Ctrl+C
```

---

## 📞 Support

If you have issues:
1. Check `logs/job_hunter.log` for errors
2. Run `python -m job_hunter stats` to see status
3. Check `job_hunter/data/config.json` for settings

---

**Your agent is now fully autonomous! Just start it and let it work for you!** 🤖

*Version 2.0 - Fully Autonomous Mode*
