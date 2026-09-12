# Job Hunter Agent

An autonomous job search and resume generation system that runs automatically twice daily.

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions (Scheduler)                              │
│  Runs at 8:00 AM and 6:00 PM IST daily                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Job Search APIs (Free)                                  │
│  - Arbeitnow API                                         │
│  - Remotive API                                          │
│  - Jobicy API                                            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Resume Generator                                        │
│  - Tailored resumes for each job                         │
│  - Fit score assessment                                  │
│  - ATS optimization                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Web Interface (Streamlit Cloud)                         │
│  - View all jobs                                         │
│  - Download resumes                                      │
│  - Track application status                              │
└─────────────────────────────────────────────────────────┘
```

## Features

- **Autonomous Operation**: Runs automatically at 8 AM and 6 PM IST
- **Multiple Job Sources**: Searches 3+ free job APIs
- **Smart Filtering**: Filters jobs based on your skills
- **Resume Generation**: Creates tailored resumes for matching jobs
- **Web Dashboard**: Beautiful interface to view and download resumes

## Deployment

### 1. GitHub Actions (Scheduler)
The scheduler runs automatically via GitHub Actions. No setup needed!

### 2. Streamlit Cloud (Web Interface)
Your app is live at:
```
https://job-hunter-agent-j32moqhcqpkwnp9tetjsdb.streamlit.app/
```

## Usage

1. The agent searches for jobs automatically at 8 AM and 6 PM
2. Check the web dashboard to view found jobs
3. Download tailored resumes for jobs you want to apply to
4. Apply when you have time!

## Files

- `job_hunter/data/jobs.json` - All found jobs
- `job_hunter/resumes/` - Generated resumes
- `job_hunter/data/search_stats.json` - Search statistics

## Configuration

Edit `job_hunter/config.py` to customize:
- Search keywords
- Preferred locations
- Max applications per day
