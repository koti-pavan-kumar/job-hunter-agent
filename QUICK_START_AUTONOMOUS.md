# 🚀 Quick Start - Autonomous Job Hunter

## One Command to Start Everything!

### **Windows:**
```bash
# Double-click this file:
start_autonomous.bat
```

### **Or run directly:**
```bash
python -m job_hunter run --immediate
```

---

## What Happens Next?

### **Automatic Process:**
1. ✅ **Searches** LinkedIn, Naukri, Internshala, Google Jobs
2. ✅ **Filters** jobs matching your skills (AI, ML, Python, Data Science)
3. ✅ **Checks** company legitimacy (removes scams)
4. ✅ **Generates** tailored resume for each matching job
5. ✅ **Generates** cover letter in .docx format
6. ✅ **Saves** everything in `job_hunter/resumes/` folder
7. ✅ **Repeats** at 8:00 AM and 6:00 PM daily

### **Your Only Job:**
1. 📂 Check `job_hunter/resumes/` folder
2. 📄 Review the generated resumes
3. ✅ Apply to the ones you like when you have time

---

## 📁 Example Output

After running, you'll see folders like this:

```
job_hunter/resumes/
├── Tech_Corp_ML_Engineer/
│   ├── resume.txt          # Tailored resume
│   ├── cover_letter.txt    # Professional cover letter
│   ├── job_details.txt     # Job info and fit score
│   └── bridging_notes.txt  # Interview prep (if needed)
├── Google_Data_Analyst/
│   ├── resume.txt
│   ├── cover_letter.txt
│   └── job_details.txt
└── ... (more jobs)
```

---

## 📊 Daily Summary Example

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

## 🎯 Daily Routine (5-10 minutes)

### **Morning:**
1. Check `job_hunter/resumes/` folder
2. See what new resumes were generated overnight
3. Note down which ones you want to apply to

### **Evening:**
1. Check the folder again
2. Apply to 2-3 jobs you like (when you have time)

### **Weekend:**
1. Review all generated resumes
2. Apply to your top 5-10 choices

---

## ❓ Common Questions

### **Q: How do I start it?**
A: Run `python -m job_hunter run --immediate`

### **Q: How do I stop it?**
A: Press `Ctrl+C` in the terminal

### **Q: Where are the resumes?**
A: In `job_hunter/resumes/` folder

### **Q: Can I change search keywords?**
A: Yes, edit `job_hunter/data/config.json`

### **Q: What if I want to search now?**
A: Run `python -m job_hunter search`

### **Q: Can I see what jobs were found?**
A: Run `python -m job_hunter list`

---

## 🔧 Useful Commands

```bash
# Start autonomous mode
python -m job_hunter run --immediate

# Search now (one-time)
python -m job_hunter search

# List all jobs
python -m job_hunter list

# View statistics
python -m job_hunter stats

# Stop the scheduler
Press Ctrl+C
```

---

## 📝 What Gets Generated

### **Resume (resume.txt)**
- Tailored to the specific job
- One-page format
- ATS-optimized
- Includes honest bridging

### **Cover Letter (cover_letter.txt)**
- 5-paragraph structure
- Company-specific
- Professional format
- Ready to send

### **Job Details (job_details.txt)**
- Job title and company
- Fit score (1-10)
- Role type detected
- Application URL

### **Bridging Notes (bridging_notes.txt)**
- Skills you're learning
- What to say in interview
- Honesty reminders

---

## 🎯 Key Features

✅ **Fully Automatic** - No manual searching needed  
✅ **Smart Matching** - Only processes jobs that fit your skills  
✅ **Scam Protection** - Filters out fake companies  
✅ **Tailored Resumes** - Each resume is customized  
✅ **Cover Letters** - Professional letters included  
✅ **Organized Output** - Everything saved in folders  
✅ **Daily Schedule** - Runs at 8 AM and 6 PM  

---

## 🚨 Important Notes

1. **Keep terminal running** - The scheduler needs to stay open
2. **Check daily** - New resumes appear twice a day
3. **Review before applying** - Always check the generated content
4. **Apply manually** - The agent prepares, you apply
5. **Respect platform rules** - Don't spam

---

## 🎯 You're All Set!

Just run:
```bash
python -m job_hunter run --immediate
```

And let the agent work for you! 🤖

*Your job hunting is now fully automated!*
