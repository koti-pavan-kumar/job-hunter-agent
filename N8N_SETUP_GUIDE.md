# n8n Job Hunter Agent - Setup Guide

## What is n8n?

n8n is a free, open-source workflow automation tool. It's like a visual programming tool where you connect blocks to create automated workflows. **This is exactly what you asked for** - an automation agent like n8n that runs automatically!

## Quick Setup (5 minutes)

### Step 1: Install n8n

**Option A: Install with npm (Recommended)**
```bash
npm install n8n -g
```

**Option B: Install with Docker**
```bash
docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

**Option C: Use n8n Cloud (Free Tier)**
- Go to https://n8n.io/cloud/
- Sign up for free
- No installation needed!

### Step 2: Start n8n

```bash
n8n start
```

Then open: http://localhost:5678

### Step 3: Import the Workflow

1. Click the **"+"** button to create a new workflow
2. Click the **"..."** menu (three dots)
3. Click **"Import from File"**
4. Select `n8n/workflows/job_search_agent.json`
5. The workflow will be imported!

### Step 4: Configure the Workflow

#### A. Set up Google Sheets (for saving jobs)
1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **Google Sheets OAuth2**
3. Follow the setup instructions
4. Update the workflow to use your credential

#### B. Set up Email Notifications
1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **SMTP**
3. Use Gmail SMTP settings:
   - Host: `smtp.gmail.com`
   - Port: `587`
   - User: `your-email@gmail.com`
   - Password: `your-app-password`
4. Update the workflow to use your credential

### Step 5: Activate the Workflow

1. Click the **"Active"** toggle in the top right
2. The workflow will now run at 8 AM and 6 PM IST automatically!

## How It Works

```
8:00 AM / 6:00 PM IST
       |
       v
+------------------+
| Schedule Trigger |
+------------------+
       |
       v
+------------------+
| Search Job APIs  |  (Arbeitnow, Remotive, Jobicy)
+------------------+
       |
       v
+------------------+
| Filter Jobs      |  (AI/ML/DS/Python skills only)
+------------------+
       |
       v
+------------------+
| Remove Duplicates|
+------------------+
       |
       v
+------------------+
| Score Job Fit    |  (Rate jobs 1-10 based on fit)
+------------------+
       |
       v
+------------------+
| Save to Google   |  (All jobs saved to spreadsheet)
| Sheets           |
+------------------+
       |
       v
+------------------+
| Send Email       |  (Notification with job list)
| Notification     |
+------------------+
```

## Adding LinkedIn/Internshala/Unstop

The free APIs don't have India-specific jobs. To add LinkedIn/Internshala:

### Option A: Use n8n HTTP Request with Cookies
1. Login to LinkedIn in your browser
2. Copy session cookie from DevTools (F12 → Network → Cookie header)
3. Add an HTTP Request node in n8n
4. Set URL: `https://www.linkedin.com/jobs/search/?keywords=python+machine+learning&location=India`
5. Set Header: `Cookie: your-copied-cookie`

### Option B: Use n8n LinkedIn Node (Requires LinkedIn API)
1. Go to https://www.linkedin.com/developers/
2. Create an app
3. Get API access
4. Use n8n's LinkedIn node

## Customization

### Change Search Keywords
Edit the "Search" nodes to change keywords:
- `python machine learning` → `data science analyst`
- `python developer` → `react frontend`

### Change Schedule
Edit the Schedule Trigger node:
- `0 8 * * *` → 8:00 AM daily
- `0 18 * * *` → 6:00 PM daily
- `0 8,12,18 * * *` → 8 AM, 12 PM, 6 PM daily

### Add More Job Sources
Add more HTTP Request nodes for other APIs:
- Adzuna API
- JSearch API
- Indeed API

## Benefits Over Previous Approach

| Previous (Broken) | n8n (Works!) |
|-------------------|--------------|
| Streamlit Cloud can't run background | n8n runs 24/7 |
| Session files lost on redeploy | n8n persists data |
| No email notifications | Built-in email node |
| Manual trigger needed | Automatic schedule |
| Complex code | Visual workflow |

## Troubleshooting

### "Workflow not running"
- Check the Schedule Trigger is active
- Check the workflow toggle is ON (top right)

### "No jobs found"
- Check API endpoints are accessible
- Check filter keywords are correct
- Check the execution log for errors

### "Email not sending"
- Check SMTP credentials
- Check Gmail App Password (not regular password)
- Check spam folder

## Support

- n8n Documentation: https://docs.n8n.io/
- n8n Community: https://community.n8n.io/
- Workflow Import: https://docs.n8n.io/workflows/export-import/
