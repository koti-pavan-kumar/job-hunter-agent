# 🚀 Quick Start Guide - Job Hunter Agent

## What's Been Built

I've created a complete **Job Hunting Agent** that automates your job search process. Here's what it does:

### ✅ Features Implemented

1. **Automated Job Search**
   - LinkedIn scraper
   - Naukri scraper
   - Internshala scraper
   - Google Jobs aggregator

2. **Resume Generator**
   - Creates tailored resumes for each job
   - Highlights relevant skills
   - Generates cover letters

3. **Application Tracker**
   - SQLite database to track all jobs
   - Monitor application status
   - Export reports to CSV

4. **Daily Scheduler**
   - Runs at 8 AM and 6 PM automatically
   - Searches across all platforms
   - Generates resumes for new jobs

---

## 🎯 How to Use (Step-by-Step)

### Step 1: Setup Your Profile

```bash
python -m job_hunter setup
```

This will ask you for:
- Your name, email, phone
- LinkedIn, GitHub, Portfolio URLs
- Your skills (Python, ML, DSA, etc.)
- Job preferences (keywords, location, type)

### Step 2: Search for Jobs

```bash
# Search all platforms
python -m job_hunter search

# Search with specific keywords
python -m job_hunter search -k "AI, Machine Learning"

# Search on specific platform
python -m job_hunter search -p linkedin

# Search in specific location
python -m job_hunter search -l "Bangalore"
```

### Step 3: View Found Jobs

```bash
# List all jobs
python -m job_hunter list

# List only new jobs
python -m job_hunter list --status new

# List applied jobs
python -m job_hunter list --status applied
```

### Step 4: Prepare Application

```bash
# Generate resume for job ID 5
python -m job_hunter apply 5
```

This will:
- Create a tailored resume for that specific job
- Generate a personalized cover letter
- Save both in the `resumes/` folder

### Step 5: Start Daily Scheduler

```bash
# Run scheduler (searches at 8 AM & 6 PM daily)
python -m job_hunter run

# Run immediately and then continue
python -m job_hunter run --immediate
```

### Step 6: View Statistics

```bash
python -m job_hunter stats
```

### Step 7: Export Report

```bash
python -m job_hunter export
```

---

## 📁 What's Been Created

```
job_hunter/
├── __init__.py          # Package init
├── __main__.py          # Entry point
├── cli.py               # Command line interface
├── config.py            # Configuration management
├── database.py          # SQLite database
├── resume_generator.py  # Resume generation
├── scheduler.py         # Daily scheduler
├── scrapers/            # Platform scrapers
│   ├── base.py          # Base scraper class
│   ├── linkedin.py      # LinkedIn scraper
│   ├── naukri.py        # Naukri scraper
│   ├── internshala.py   # Internshala scraper
│   └── google_jobs.py   # Google Jobs scraper
├── data/                # Database and configs
├── resumes/             # Generated resumes
└── logs/                # Application logs
```

---

## 🎨 Example Output

When you run the system, it will:

1. **Search LinkedIn, Naukri, Internshala, Google Jobs**
2. **Store new jobs in database**
3. **Generate tailored resumes** like this:

```
John Doe
john.doe@email.com | +91 9876543210
linkedin.com/in/johndoe | github.com/johndoe

================================================================================
OBJECTIVE
================================================================================

Motivated Computer Science student seeking an internship position at Tech Corp 
to apply my skills in Python, Machine Learning, Deep Learning...

================================================================================
TECHNICAL SKILLS
================================================================================
Programming Languages: Python
ML/AI Skills: Machine Learning, Deep Learning, TensorFlow, PyTorch
Tools & Technologies: SQL, Git

================================================================================
PROJECTS
================================================================================

Project 1: AI Chatbot
Built an AI-powered chatbot using NLP and deep learning
Technologies: Python, TensorFlow, Flask
...
```

---

## 💡 Tips for Your Situation

### Time Management

Since you have limited time (morning and evening):

1. **Run the scheduler in background**
   ```bash
   python -m job_hunter run --immediate
   ```
   Let it search while you study.

2. **Check results quickly**
   ```bash
   python -m job_hunter list --status new
   ```
   Only review new jobs (5-10 min).

3. **Batch apply on weekends**
   ```bash
   python -m job_hunter apply <job_id>
   ```
   Generate resumes for all good matches.

### Best Practices

1. **Run scheduler daily** - It searches at 8 AM and 6 PM
2. **Review jobs weekly** - Spend 30 min on Sunday
3. **Apply to quality jobs** - Don't spam, be selective
4. **Update your profile** - Keep skills and projects current

---

## ⚠️ Important Notes

1. **Resumes are text files** - You can convert to PDF using online tools
2. **Manual application required** - The agent prepares, you apply
3. **Respect platform rules** - Don't spam or violate ToS
4. **Review generated content** - Always check before applying

---

## 🎯 Your Daily Routine (Suggested)

### Morning (Before College)
```
8:00 AM - Scheduler runs automatically
          Searches all platforms
          Generates resumes for new jobs

8:15 AM - Quick check (5 min)
          python -m job_hunter list --status new
          Note down good matches
```

### Evening (After College)
```
6:00 PM - Scheduler runs again
          Finds more jobs

6:15 PM - Review and apply (30 min)
          python -m job_hunter apply <job_id>
          Apply to 5-10 quality jobs
```

### Weekend (Sunday)
```
10:00 AM - Full review (1 hour)
           python -m job_hunter list
           python -m job_hunter stats
           Apply to all pending good matches
           Update your profile if needed
```

---

## 🚀 Ready to Start?

Run this command now:

```bash
python -m job_hunter setup
```

This will guide you through setting up your profile. Then run:

```bash
python -m job_hunter search
```

And see the magic happen!

---

**Need help?** Run `python -m job_hunter --help` for all commands.
