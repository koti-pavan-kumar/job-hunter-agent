# 🤖 Fully Autonomous Job Hunter Agent

## ✅ No Manual Commands Required!

This guide will deploy a **fully autonomous agent** like n8n that:
- ✅ Runs automatically at 8 AM and 6 PM daily
- ✅ No manual commands needed
- ✅ No keeping your PC on
- ✅ Works 24/7 in the cloud

---

## 🎯 How It Works

```
┌─────────────────────────────────────────────────────────┐
│  Cloud Scheduler (Railway/Render)                        │
│  ✅ Runs 24/7 in the cloud                              │
│  ✅ Searches at 8 AM and 6 PM automatically             │
│  ✅ Generates resumes automatically                     │
│  ✅ No manual intervention needed                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Web Interface (Streamlit Cloud)                         │
│  ✅ View generated resumes                              │
│  ✅ Download resumes and cover letters                  │
│  ✅ Apply to jobs                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Options

### **Option 1: Railway (Recommended)**

**Why Railway?**
- ✅ Free tier available
- ✅ Supports background workers
- ✅ Easy deployment
- ✅ Automatic scaling

**Steps:**

1. **Go to Railway**
   ```
   https://railway.app
   ```

2. **Sign in with GitHub**

3. **Click "New Project"**

4. **Select "Deploy from GitHub repo"**

5. **Select your repository:**
   ```
   koti-pavan-kumar/job-hunter-agent
   ```

6. **Railway will auto-detect and deploy**

7. **Your scheduler is now running 24/7!**

---

### **Option 2: Render (Good Alternative)**

**Why Render?**
- ✅ Free tier available
- ✅ Supports background workers
- ✅ Easy setup

**Steps:**

1. **Go to Render**
   ```
   https://render.com
   ```

2. **Sign in with GitHub**

3. **Click "New" → "Background Worker"**

4. **Select your repository**

5. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python cloud_scheduler.py`

6. **Click "Create Background Worker"**

7. **Your scheduler is now running 24/7!**

---

### **Option 3: PythonAnywhere (Free)**

**Why PythonAnywhere?**
- ✅ Free tier
- ✅ Supports scheduled tasks
- ✅ No credit card needed

**Steps:**

1. **Go to PythonAnywhere**
   ```
   https://pythonanywhere.com
   ```

2. **Create free account**

3. **Go to "Tasks" tab**

4. **Add scheduled task:**
   - Command: `python cloud_scheduler.py`
   - Time: `0 8 * * *` (8 AM daily)
   - Time: `0 18 * * *` (6 PM daily)

5. **Your scheduler is now running!**

---

## 📋 What Gets Deployed

### **Cloud Scheduler**
- Runs automatically at 8 AM and 6 PM
- Searches LinkedIn, Naukri, Internshala, Google Jobs
- Checks company legitimacy
- Generates tailored resumes
- Generates cover letters
- Saves everything in organized folders

### **Web Interface**
- Dashboard with statistics
- Job listings browser
- Generated resumes viewer
- Settings configuration
- Agent control panel

---

## 🎯 Your Daily Workflow (After Deployment)

### **Morning:**
1. Open web interface
2. Check "📄 Generated Resumes"
3. See new resumes from overnight
4. Note down which ones to apply to

### **Evening:**
1. Check web interface again
2. Apply to 2-3 jobs you like

### **That's it!** The agent does all the work!

---

## 📊 Timeline

| Time | What Happens | Where |
|------|--------------|-------|
| **8:00 AM** | Scheduler searches all platforms | Cloud (Railway/Render) |
| **8:15 AM** | Generates resumes for matching jobs | Cloud |
| **9:00 AM** | You open web interface | Browser |
| **9:05 AM** | You see new resumes | Browser |
| **6:00 PM** | Scheduler searches again | Cloud |
| **6:15 PM** | More resumes generated | Cloud |
| **Anytime** | You apply to jobs | Browser |

---

## ❓ FAQ

### **Q: Do I need to run any commands daily?**
**A:** NO! The scheduler runs automatically in the cloud. You just check the web interface.

### **Q: Do I need to keep my PC on?**
**A:** NO! The scheduler runs in the cloud, not on your PC.

### **Q: How do I know when new resumes are generated?**
**A:** Check the web interface. New resumes appear automatically.

### **Q: Can I customize the schedule?**
**A:** Yes! Edit `cloud_scheduler.py` to change the schedule times.

### **Q: What if the scheduler stops?**
**A:** Railway/Render will automatically restart it.

---

## 🔧 Customization

### **Change Schedule Times**

Edit `cloud_scheduler.py`:

```python
# Change from 8 AM and 6 PM to your preferred times
schedule.every().day.at("09:00").do(self.autonomous_job_search)
schedule.every().day.at("19:00").do(self.autonomous_job_search)
```

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

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All files are in GitHub repository
- [ ] `cloud_scheduler.py` exists
- [ ] `requirements.txt` is complete
- [ ] `railway.json` exists (for Railway)
- [ ] `render.yaml` exists (for Render)
- [ ] `app.py` exists (for web interface)

---

## 🚀 Quick Deployment Commands

### **Railway:**
```bash
# Just push to GitHub and deploy via Railway dashboard
git push origin main
```

### **Render:**
```bash
# Just push to GitHub and deploy via Render dashboard
git push origin main
```

### **PythonAnywhere:**
```bash
# Upload files and set up scheduled tasks
# via PythonAnywhere dashboard
```

---

## 🎯 Summary

| Feature | Before (Manual) | After (Autonomous) |
|---------|-----------------|-------------------|
| **Daily Commands** | ❌ Need to type | ✅ No commands needed |
| **PC Required** | ❌ Must keep PC on | ✅ Runs in cloud |
| **Schedule** | ❌ Manual start | ✅ Automatic 8 AM & 6 PM |
| **Intervention** | ❌ Daily manual | ✅ Zero intervention |
| **Like n8n** | ❌ No | ✅ Yes! |

---

## 🎉 You're All Set!

**After deploying:**
1. ✅ Scheduler runs automatically at 8 AM and 6 PM
2. ✅ No manual commands needed
3. ✅ No keeping PC on
4. ✅ Just check web interface and apply

**Deploy now and enjoy fully autonomous job hunting!** 🚀

---

*Fully Autonomous Deployment Guide v2.0*
