# 🎯 Job Hunter Agent

Automated Job Search & Application Tracker for Students

## 📋 Features

- **Automated Job Search**: Search multiple platforms daily
- **Resume Generator**: Create tailored resumes for each job
- **Application Tracker**: Track all your applications
- **Daily Scheduler**: Run searches automatically
- **Multi-Platform Support**: LinkedIn, Naukri, Internshala, Google Jobs

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Setup

```bash
python -m job_hunter setup
```

This will guide you through:
- Personal information
- Skills and preferences
- Job search criteria

### 3. Start Job Hunting

```bash
# Run scheduler (searches at 8 AM and 6 PM daily)
python -m job_hunter run --immediate

# Or run once
python -m job_hunter run
```

## 📚 Commands

### Setup Wizard
```bash
python -m job_hunter setup
```
Interactive setup to configure your profile and preferences.

### Search Jobs
```bash
python -m job_hunter search
python -m job_hunter search -k "AI, ML" -l "Bangalore"
python -m job_hunter search -p linkedin
```

### List Jobs
```bash
python -m job_hunter list
python -m job_hunter list --status new
python -m job_hunter list --status applied
```

### Prepare Application
```bash
python -m job_hunter apply <job_id>
```
Generates tailored resume and cover letter for a specific job.

### View Statistics
```bash
python -m job_hunter stats
```

### Export Report
```bash
python -m job_hunter export
python -m job_hunter export -f my_report.csv
```

### Start Scheduler
```bash
python -m job_hunter run
python -m job_hunter run --immediate
```

## 📁 Project Structure

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
│   ├── __init__.py
│   ├── base.py          # Base scraper class
│   ├── linkedin.py      # LinkedIn scraper
│   ├── naukri.py        # Naukri scraper
│   ├── internshala.py   # Internshala scraper
│   └── google_jobs.py   # Google Jobs scraper
├── data/                # Database and configs
├── resumes/             # Generated resumes
└── logs/                # Application logs
```

## ⚙️ Configuration

After running setup, your configuration is saved in `data/config.json`.

You can manually edit this file to update:
- Job keywords
- Preferred locations
- Resume information
- Skills

## 📊 Database

The application uses SQLite to track:
- Job listings from all platforms
- Your applications
- Daily statistics

Data is stored in `data/jobs.db`.

## 🔄 How It Works

1. **Daily Search**: Scheduler runs at 8 AM and 6 PM
2. **Scrape Jobs**: Searches LinkedIn, Naukri, Internshala, Google
3. **Store in DB**: New jobs are added to database
4. **Generate Resume**: Creates tailored resume for each job
5. **Generate Cover Letter**: Creates personalized cover letter
6. **Track Applications**: Updates status in database

## 📝 Notes

- **Resumes are generated as text files** in the `resumes/` directory
- **You need to manually apply** to jobs after reviewing generated documents
- **Respect platform ToS**: Don't spam or automate actual applications
- **Review resumes**: Always review generated content before applying

## 🛠️ Customization

### Add New Platforms

1. Create new scraper in `scrapers/` directory
2. Inherit from `BaseScraper`
3. Implement `search_jobs()` and `get_job_details()`
4. Add to `scrapers/__init__.py`

### Customize Resume Templates

Edit `resume_generator.py` to modify resume format and content.

## ⚠️ Disclaimer

This tool is for educational purposes. Always:
- Respect platform Terms of Service
- Review generated content before applying
- Don't spam or mass-apply without review
- Follow ethical job hunting practices

## 📧 Support

For issues or suggestions, please create an issue in the repository.

---

**Happy Job Hunting! 🎯**
