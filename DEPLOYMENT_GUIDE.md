# 🚀 Deployment Guide - Job Hunter Agent Web Interface

## Overview

Your Job Hunter Agent can now be deployed as a web application with a visual interface. Here are multiple deployment options:

---

## Option 1: Streamlit Cloud (Easiest - Free)

### **Steps:**
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/job-hunter-agent.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   ```
   https://yourusername-job-hunter-agent-app-xxxxx.streamlit.app
   ```

### **Pros:**
- ✅ Free tier available
- ✅ No server setup needed
- ✅ Automatic HTTPS
- ✅ Easy to update

### **Cons:**
- ❌ Limited resources on free tier
- ❌ App sleeps after inactivity

---

## Option 2: Heroku (Free Tier Available)

### **Steps:**
1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install Heroku.cli
   
   # Mac/Linux
   brew tap heroku/brew && brew install heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create job-hunter-agent
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open your app**
   ```bash
   heroku open
   ```

### **Pros:**
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Automatic scaling

### **Cons:**
- ❌ Free tier has limitations
- ❌ Requires Heroku account

---

## Option 3: Railway (Modern & Easy)

### **Steps:**
1. **Go to [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Select your repository**
6. **Railway will auto-detect and deploy**

### **Pros:**
- ✅ Modern interface
- ✅ Easy setup
- ✅ Good free tier

### **Cons:**
- ❌ Newer platform
- ❌ Limited free tier

---

## Option 4: Docker (Self-Hosted)

### **Steps:**
1. **Build Docker Image**
   ```bash
   docker build -t job-hunter-agent .
   ```

2. **Run Docker Container**
   ```bash
   docker run -d -p 8501:8501 --name job-hunter job-hunter-agent
   ```

3. **Or use docker-compose**
   ```bash
   docker-compose up -d
   ```

4. **Access your app**
   ```
   http://localhost:8501
   ```

### **Pros:**
- ✅ Full control
- ✅ No external dependencies
- ✅ Can run anywhere

### **Cons:**
- ❌ Requires Docker knowledge
- ❌ Need your own server

---

## Option 5: PythonAnywhere (Free Tier)

### **Steps:**
1. **Go to [pythonanywhere.com](https://pythonanywhere.com)**
2. **Create free account**
3. **Go to "Web" tab**
4. **Click "Add a new web app"**
5. **Select "Streamlit"**
6. **Upload your files**
7. **Configure and start**

### **Pros:**
- ✅ Free tier available
- ✅ No credit card needed
- ✅ Easy setup

### **Cons:**
- ❌ Limited resources
- ❌ Slower performance

---

## Option 6: AWS/GCP/Azure (Production)

### **AWS (using ECS or EC2):**
```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t job-hunter-agent .
docker tag job-hunter-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/job-hunter-agent:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/job-hunter-agent:latest
```

### **Pros:**
- ✅ Enterprise-grade
- ✅ Scalable
- ✅ Full control

### **Cons:**
- ❌ Complex setup
- ❌ Costs money
- ❌ Requires DevOps knowledge

---

## 🎯 Recommended Option

### **For Beginners: Streamlit Cloud**
- Easiest to set up
- Free tier available
- No server management

### **For Production: Docker + Railway/Heroku**
- More control
- Better performance
- Easy to scale

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All files are in place
- [ ] `requirements_web.txt` is complete
- [ ] `Procfile` exists (for Heroku)
- [ ] `Dockerfile` exists (for Docker)
- [ ] `.streamlit/config.toml` exists
- [ ] Application runs locally:
  ```bash
  streamlit run app.py
  ```

---

## 🔧 Environment Variables

If needed, set these environment variables:

```bash
# For production
export PYTHONUNBUFFERED=1
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 🐛 Troubleshooting

### **App won't start:**
```bash
# Check logs
streamlit run app.py

# Or for Docker
docker logs job-hunter
```

### **Port already in use:**
```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>
```

### **Dependencies not installing:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements_web.txt
```

---

## 📊 Monitoring

### **Check app status:**
```bash
# Streamlit
streamlit run app.py

# Docker
docker ps
docker logs job-hunter

# Heroku
heroku logs --tail
```

### **View database:**
```bash
# SQLite
sqlite3 job_hunter/data/jobs.db

# List tables
.tables

# View jobs
SELECT * FROM job_listings LIMIT 10;
```

---

## 🔄 Updates

### **Update Streamlit Cloud:**
1. Push changes to GitHub
2. Streamlit auto-redeploys

### **Update Heroku:**
```bash
git add .
git commit -m "Update"
git push heroku main
```

### **Update Docker:**
```bash
docker build -t job-hunter-agent .
docker stop job-hunter
docker rm job-hunter
docker run -d -p 8501:8501 --name job-hunter job-hunter-agent
```

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Heroku Documentation](https://devcenter.heroku.com)
- [Docker Documentation](https://docs.docker.com)
- [Railway Documentation](https://docs.railway.app)

---

## 🎯 Quick Start Commands

### **Local Development:**
```bash
# Install dependencies
pip install -r requirements_web.txt

# Run app
streamlit run app.py
```

### **Docker Deployment:**
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8501
```

### **Streamlit Cloud:**
```bash
# Push to GitHub
git push origin main

# Deploy at share.streamlit.io
```

---

**Your Job Hunter Agent is now ready for deployment!** 🚀

Choose the option that best fits your needs and follow the steps above.
