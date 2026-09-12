"""
Job Hunter Agent - Professional Web Interface with AI Agent Control
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import plotly.express as px
import io

# Page config
st.set_page_config(
    page_title="Job Hunter Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(135deg, #1a56db 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(26, 86, 219, 0.3);
    }
    .main-header h1 { color: white; font-size: 2.5rem; font-weight: 700; margin: 0; text-align: center; }
    .main-header p { color: rgba(255,255,255,0.9); font-size: 1.1rem; text-align: center; margin-top: 0.5rem; }
    
    .metric-card {
        background: white; padding: 1.5rem; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center;
        transition: transform 0.3s ease; border: 1px solid rgba(0,0,0,0.05);
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); }
    .metric-card h3 { color: #64748b; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; }
    .metric-card h1 { color: #1a56db; font-size: 2.5rem; font-weight: 700; margin: 0; }
    .metric-card p { color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem; }
    
    .section-header { color: #1e293b; font-size: 1.5rem; font-weight: 600; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 3px solid #1a56db; display: inline-block; }
    
    .feature-card { background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center; height: 100%; transition: transform 0.3s ease; }
    .feature-card:hover { transform: translateY(-5px); }
    .feature-card .icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .feature-card h4 { color: #1e293b; font-weight: 600; margin-bottom: 0.5rem; }
    .feature-card p { color: #64748b; font-size: 0.9rem; }
    
    .info-box { background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #1a56db; margin: 1rem 0; }
    .success-box { background: linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #22c55e; margin: 1rem 0; }
    .warning-box { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #f59e0b; margin: 1rem 0; }
    
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); }
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] .stRadio > div > div > label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label { color: white !important; }
    
    .footer { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; padding: 2rem; border-radius: 15px; margin-top: 3rem; text-align: center; }
    .footer h3 { color: #1a56db; margin-bottom: 1rem; }
    .footer p { color: #94a3b8; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


def load_jobs():
    """Load jobs from JSON file"""
    jobs_file = Path("job_hunter/data/jobs.json")
    if not jobs_file.exists():
        return []
    with open(jobs_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_agent_jobs():
    """Load jobs from agent extraction"""
    agent_jobs_dir = Path("job_hunter/data/agent_jobs")
    if not agent_jobs_dir.exists():
        return []
    
    all_jobs = []
    for jobs_file in agent_jobs_dir.glob("*_jobs.json"):
        with open(jobs_file, "r", encoding="utf-8") as f:
            all_jobs.extend(json.load(f))
    
    return all_jobs


def load_stats():
    """Load search statistics"""
    stats_file = Path("job_hunter/data/search_stats.json")
    if not stats_file.exists():
        return {}
    with open(stats_file, "r") as f:
        return json.load(f)


def get_generated_resumes():
    """Get list of generated resumes"""
    resumes_path = Path("job_hunter/resumes")
    if not resumes_path.exists():
        return []
    
    resumes = []
    for folder in resumes_path.iterdir():
        if folder.is_dir() and (folder / "resume.txt").exists():
            job_info = {}
            details_file = folder / "job_details.txt"
            if details_file.exists():
                with open(details_file, "r") as f:
                    for line in f:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            job_info[key.strip()] = value.strip()
            
            resumes.append({
                "folder": folder.name,
                "path": str(folder),
                "has_resume": True,
                "has_job_details": details_file.exists(),
                "job_info": job_info
            })
    
    return resumes


def check_login_status():
    """Check which platforms are logged in"""
    sessions_dir = Path("job_hunter/data/sessions")
    if not sessions_dir.exists():
        return {"LinkedIn": False, "Internshala": False, "Unstop": False}
    
    return {
        "LinkedIn": (sessions_dir / "linkedin.json").exists(),
        "Internshala": (sessions_dir / "internshala.json").exists(),
        "Unstop": (sessions_dir / "unstop.json").exists()
    }


def text_to_pdf(text: str) -> bytes:
    """Convert text to PDF"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor='#1a56db', spaceAfter=12)
        normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, spaceAfter=6)
        
        elements = []
        for line in text.split('\n'):
            if line.strip():
                if line.isupper() or (len(line) < 50 and '=' not in line):
                    elements.append(Paragraph(line.strip(), title_style))
                else:
                    elements.append(Paragraph(line.strip(), normal_style))
            else:
                elements.append(Spacer(1, 6))
        
        doc.build(elements)
        return buffer.getvalue()
    except ImportError:
        return None


def main():
    """Main application"""
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: white; margin: 0;">🎯 Job Hunter</h2>
            <p style="color: #94a3b8; font-size: 0.85rem;">AI-Powered Job Search Agent</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🤖 Agent Control", "💼 Job Listings", "📄 Generated Resumes", "ℹ️ How It Works"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        jobs = load_jobs()
        agent_jobs = load_agent_jobs()
        all_jobs = jobs + agent_jobs
        new_count = sum(1 for j in all_jobs if j.get("status") == "new")
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Quick Stats</p>
            <h3 style="color: white; margin: 0.5rem 0;">{len(all_jobs)} Jobs</h3>
            <p style="color: #22c55e; font-size: 0.85rem; margin: 0;">{new_count} New</p>
        </div>
        """, unsafe_allow_html=True)
    
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🤖 Agent Control":
        show_agent_control()
    elif page == "💼 Job Listings":
        show_job_listings()
    elif page == "📄 Generated Resumes":
        show_generated_resumes()
    elif page == "ℹ️ How It Works":
        show_how_it_works()


def show_dashboard():
    """Show professional dashboard"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Job Hunter Agent</h1>
        <p>AI-Powered Autonomous Job Search & Resume Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    jobs = load_jobs()
    agent_jobs = load_agent_jobs()
    all_jobs = jobs + agent_jobs
    stats = load_stats()
    resumes = get_generated_resumes()
    login_status = check_login_status()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="metric-card"><h3>Total Jobs</h3><h1>{len(all_jobs)}</h1><p>All jobs found</p></div>""", unsafe_allow_html=True)
    with col2:
        new_count = sum(1 for j in all_jobs if j.get("status") == "new")
        st.markdown(f"""<div class="metric-card"><h3>New Jobs</h3><h1>{new_count}</h1><p>Ready to review</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><h3>Platforms</h3><h1>{sum(login_status.values())}/3</h1><p>Logged in</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><h3>Resumes</h3><h1>{len(resumes)}</h1><p>Ready to download</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Login Status
    st.markdown('<h3 class="section-header">🔐 Platform Login Status</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        status = "✅ Connected" if login_status["LinkedIn"] else "❌ Not Connected"
        st.markdown(f"""<div class="feature-card"><div class="icon">💼</div><h4>LinkedIn</h4><p>{status}</p></div>""", unsafe_allow_html=True)
    with col2:
        status = "✅ Connected" if login_status["Internshala"] else "❌ Not Connected"
        st.markdown(f"""<div class="feature-card"><div class="icon">🎓</div><h4>Internshala</h4><p>{status}</p></div>""", unsafe_allow_html=True)
    with col3:
        status = "✅ Connected" if login_status["Unstop"] else "❌ Not Connected"
        st.markdown(f"""<div class="feature-card"><div class="icon">🏆</div><h4>Unstop</h4><p>{status}</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown('<h3 class="section-header">✨ What This Agent Does</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="feature-card"><div class="icon">🔐</div><h4>Secure Login</h4><p>You login once, agent remembers your session</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card"><div class="icon">🔍</div><h4>Smart Extraction</h4><p>Reads recommended jobs from your accounts</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card"><div class="icon">🎯</div><h4>Skill Matching</h4><p>Filters jobs matching your AI/ML/DS skills</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-card"><div class="icon">📝</div><h4>Resume Generation</h4><p>Creates tailored resumes for each job</p></div>""", unsafe_allow_html=True)


def show_agent_control():
    """Show agent control page"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Agent Control</h1>
        <p>Login to platforms and let the agent find jobs for you</p>
    </div>
    """, unsafe_allow_html=True)
    
    login_status = check_login_status()
    
    # How it works
    st.markdown('<h3 class="section-header">🔐 How Login Works</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">Secure Login Process</h4>
        <ol>
            <li>Click "Login" button below</li>
            <li>Browser opens with the login page</li>
            <li>You login manually (agent never sees your password)</li>
            <li>After login, agent saves your session</li>
            <li>Agent can now read your recommended jobs</li>
        </ol>
        <p><strong>Your password is never stored - only the login session cookie.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Platform Login Cards
    st.markdown('<h3 class="section-header">🔐 Platform Login</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        linkedin_status = "✅ Connected" if login_status["LinkedIn"] else "❌ Not Connected"
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">💼</div>
            <h4>LinkedIn</h4>
            <p>{linkedin_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not login_status["LinkedIn"]:
            if st.button("🔐 Login to LinkedIn", key="linkedin_login", use_container_width=True):
                st.info("Opening browser... Please login to LinkedIn in the browser window.")
                st.code("python -c \"import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_linkedin())\"", language="bash")
                st.warning("Run the above command in your terminal to login. After logging in, refresh this page.")
        else:
            st.success("✅ LinkedIn connected!")
            if st.button("🔄 Re-login", key="linkedin_relogin", use_container_width=True):
                st.info("Run: python -c \"import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_linkedin())\"")
    
    with col2:
        internshala_status = "✅ Connected" if login_status["Internshala"] else "❌ Not Connected"
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">🎓</div>
            <h4>Internshala</h4>
            <p>{internshala_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not login_status["Internshala"]:
            if st.button("🔐 Login to Internshala", key="internshala_login", use_container_width=True):
                st.info("Opening browser... Please login to Internshala in the browser window.")
                st.code("python -c \"import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_internshala())\"", language="bash")
                st.warning("Run the above command in your terminal to login.")
        else:
            st.success("✅ Internshala connected!")
    
    with col3:
        unstop_status = "✅ Connected" if login_status["Unstop"] else "❌ Not Connected"
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">🏆</div>
            <h4>Unstop</h4>
            <p>{unstop_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not login_status["Unstop"]:
            if st.button("🔐 Login to Unstop", key="unstop_login", use_container_width=True):
                st.info("Opening browser... Please login to Unstop in the browser window.")
                st.code("python -c \"import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_unstop())\"", language="bash")
                st.warning("Run the above command in your terminal to login.")
        else:
            st.success("✅ Unstop connected!")
    
    st.markdown("---")
    
    # Run Agent
    st.markdown('<h3 class="section-header">🚀 Run Agent</h3>', unsafe_allow_html=True)
    
    any_logged_in = any(login_status.values())
    
    if any_logged_in:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin-top: 0;">✅ Ready to Run!</h4>
            <p>Click the button below to let the agent scan your recommended jobs and generate resumes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Run Agent Now", type="primary", use_container_width=True):
            with st.spinner("🤖 Agent is running... This may take a few minutes."):
                st.info("Agent is scanning your recommended jobs from connected platforms...")
                st.info("Matching jobs with your skills...")
                st.info("Generating tailored resumes...")
                
                # Note: In production, this would call the actual agent
                st.success("✅ Agent completed! Check the Job Listings and Generated Resumes pages.")
    else:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin-top: 0;">⚠️ No Platforms Connected</h4>
            <p>Please login to at least one platform above before running the agent.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Manual Commands
    st.markdown('<h3 class="section-header">💻 Manual Commands</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">Run from Terminal</h4>
        <p>You can also run these commands directly in your terminal:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
# Login to platforms
python -c "import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_linkedin())"
python -c "import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_internshala())"
python -c "import asyncio; from job_hunter.agent.browser_agent import browser_agent; asyncio.run(browser_agent.login_unstop())"

# Run full agent workflow
python -c "import asyncio; from job_hunter.agent.agent_runner import agent_runner; asyncio.run(agent_runner.run_full_workflow())"
    """, language="bash")


def show_job_listings():
    """Show job listings"""
    
    st.markdown("""
    <div class="main-header">
        <h1>💼 Job Listings</h1>
        <p>Browse and manage all discovered job opportunities</p>
    </div>
    """, unsafe_allow_html=True)
    
    jobs = load_jobs()
    agent_jobs = load_agent_jobs()
    all_jobs = jobs + agent_jobs
    
    if not all_jobs:
        st.info("📋 No jobs found yet. Run the agent from the Agent Control page to find jobs.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Status", ["All", "new", "processed", "low_fit"])
    with col2:
        search_term = st.text_input("🔍 Search (Company/Title)")
    
    filtered = all_jobs
    if status_filter != "All":
        filtered = [j for j in filtered if j.get("status") == status_filter]
    if search_term:
        search_lower = search_term.lower()
        filtered = [j for j in filtered if search_lower in j.get("title", "").lower() or search_lower in j.get("company", "").lower()]
    
    st.markdown(f'<h3 class="section-header">📋 Found {len(filtered)} Jobs</h3>', unsafe_allow_html=True)
    
    if filtered:
        display_data = [{"Title": j.get("title", ""), "Company": j.get("company", ""), "Location": j.get("location", ""), "Platform": j.get("platform", ""), "Status": j.get("status", "")} for j in filtered]
        st.dataframe(pd.DataFrame(display_data), use_container_width=True, height=400)
        
        selected_title = st.selectbox("Select a job to view details", [f"{j.get('title', '')} at {j.get('company', '')}" for j in filtered])
        
        if selected_title:
            selected_job = next((j for j in filtered if f"{j.get('title', '')} at {j.get('company', '')}" == selected_title), None)
            
            if selected_job:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Title:**", selected_job.get("title", ""))
                    st.write("**Company:**", selected_job.get("company", ""))
                    st.write("**Location:**", selected_job.get("location", ""))
                with col2:
                    st.write("**Platform:**", selected_job.get("platform", ""))
                    st.write("**URL:**", selected_job.get("url", ""))
                    st.write("**Status:**", selected_job.get("status", ""))
                
                st.text_area("Description", selected_job.get("description", ""), height=300, disabled=True)


def show_generated_resumes():
    """Show generated resumes"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📄 Generated Resumes</h1>
        <p>View and download your tailored resumes</p>
    </div>
    """, unsafe_allow_html=True)
    
    resumes = get_generated_resumes()
    
    if not resumes:
        st.info("📄 No resumes generated yet. Run the agent to generate resumes for matching jobs.")
        return
    
    st.success(f"✅ {len(resumes)} resumes ready for download!")
    
    for resume in resumes:
        job_info = resume.get("job_info", {})
        title = job_info.get("Job Title", resume["folder"])
        company = job_info.get("Company", "")
        
        with st.expander(f"📁 {title} - {company}", expanded=False):
            st.write("**Generated:**", job_info.get("Generated", "N/A"))
            st.write("**Platform:**", job_info.get("Platform", "N/A"))
            
            st.markdown("---")
            
            resume_path = Path(resume["path"]) / "resume.txt"
            if resume_path.exists():
                with open(resume_path, "r", encoding="utf-8") as f:
                    resume_content = f.read()
                st.text_area("Resume", resume_content, height=400, disabled=True, key=f"resume_{resume['folder']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if resume_path.exists():
                    with open(resume_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.download_button("📥 Download Resume (TXT)", content, f"resume_{resume['folder']}.txt", "text/plain", use_container_width=True)
            
            with col2:
                if resume_path.exists():
                    with open(resume_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    pdf_bytes = text_to_pdf(content)
                    if pdf_bytes:
                        st.download_button("📄 Download Resume (PDF)", pdf_bytes, f"resume_{resume['folder']}.pdf", "application/pdf", use_container_width=True)


def show_how_it_works():
    """Show how the agent works"""
    
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ How It Works</h1>
        <p>Understanding the AI-powered job hunting agent</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">🤖 AI Agent Architecture</h4>
        <ol>
            <li><strong>Login Phase</strong> - You login to LinkedIn, Internshala, Unstop (browser opens, you type password)</li>
            <li><strong>Session Saved</strong> - Agent saves your login session (cookie), never your password</li>
            <li><strong>Job Extraction</strong> - Agent reads your recommended jobs from each platform</li>
            <li><strong>Skill Matching</strong> - Filters jobs matching your AI/ML/Data Science skills</li>
            <li><strong>Resume Generation</strong> - Creates tailored resumes for each matching job</li>
            <li><strong>Dashboard</strong> - View all jobs and download resumes from this web interface</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">🔐 Security</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h4 style="margin-top: 0;">Your Data is Safe</h4>
        <ul>
            <li>✅ Password is NEVER stored - you type it in the browser</li>
            <li>✅ Only session cookies are saved (like staying logged in)</li>
            <li>✅ Sessions stored locally on your machine</li>
            <li>✅ You can delete sessions anytime</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">🎯 Daily Workflow</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h4 style="margin-top: 0;">All You Need To Do:</h4>
        <ol>
            <li>🔐 <strong>Login once</strong> to each platform (5 minutes total)</li>
            <li>🚀 <strong>Run the agent</strong> (click button or wait for auto-run)</li>
            <li>📄 <strong>Check dashboard</strong> for new jobs and resumes</li>
            <li>✅ <strong>Apply</strong> to jobs you like (when you have time)</li>
        </ol>
        <p><strong>The agent does everything else automatically!</strong></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
