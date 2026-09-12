"""
Job Hunter Agent - Professional Web Interface
Reads from JSON data files (populated by GitHub Actions)
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
                "has_job_description": (folder / "job_description.txt").exists(),
                "job_info": job_info
            })
    
    return resumes


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
            <p style="color: #94a3b8; font-size: 0.85rem;">Autonomous Job Search Agent</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "💼 Job Listings", "📄 Generated Resumes", "ℹ️ How It Works"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        jobs = load_jobs()
        new_count = sum(1 for j in jobs if j.get("status") == "new")
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Quick Stats</p>
            <h3 style="color: white; margin: 0.5rem 0;">{len(jobs)} Jobs</h3>
            <p style="color: #22c55e; font-size: 0.85rem; margin: 0;">{new_count} New</p>
        </div>
        """, unsafe_allow_html=True)
    
    if page == "📊 Dashboard":
        show_dashboard()
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
        <p>Autonomous Job Search & Resume Generation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    jobs = load_jobs()
    stats = load_stats()
    resumes = get_generated_resumes()
    
    new_count = sum(1 for j in jobs if j.get("status") == "new")
    processed_count = sum(1 for j in jobs if j.get("status") == "processed")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="metric-card"><h3>Total Jobs</h3><h1>{len(jobs)}</h1><p>All jobs found</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><h3>New Jobs</h3><h1>{new_count}</h1><p>Ready to review</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><h3>Processed</h3><h1>{processed_count}</h1><p>Resumes generated</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><h3>Resumes</h3><h1>{len(resumes)}</h1><p>Ready to download</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">📊 Jobs by Status</h3>', unsafe_allow_html=True)
        status_counts = {}
        for job in jobs:
            status = job.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            colors = {"new": "#1a56db", "processed": "#22c55e", "low_fit": "#f59e0b", "skipped": "#ef4444"}
            fig = px.pie(values=list(status_counts.values()), names=list(status_counts.keys()),
                        color=list(status_counts.keys()), color_discrete_map=colors, hole=0.4)
            fig.update_layout(showlegend=True, height=300, margin=dict(t=20, b=20, l=20, r=20),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-header">📈 Jobs by Platform</h3>', unsafe_allow_html=True)
        platform_counts = {}
        for job in jobs:
            platform = job.get("platform", "Unknown")
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        if platform_counts:
            fig = px.bar(x=list(platform_counts.keys()), y=list(platform_counts.values()),
                        color=list(platform_counts.keys()), color_discrete_sequence=['#1a56db', '#7c3aed', '#22c55e', '#f59e0b'])
            fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    if stats:
        st.markdown("---")
        st.markdown('<h3 class="section-header">🕐 Last Search</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Last Search", stats.get("timestamp", "Never")[:19])
        with col2:
            st.metric("Jobs Found", stats.get("jobs_found", 0))
        with col3:
            st.metric("Resumes Generated", stats.get("resumes_generated", 0))
    
    st.markdown("---")
    st.markdown('<h3 class="section-header">✨ What This Agent Does</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="feature-card"><div class="icon">🔍</div><h4>Smart Search</h4><p>Automatically searches for AI/ML/Data Science jobs at 8 AM & 6 PM daily</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card"><div class="icon">📝</div><h4>Tailored Resumes</h4><p>Generates ATS-optimized resumes customized for each job</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card"><div class="icon">✅</div><h4>Fit Assessment</h4><p>Automatically filters jobs based on your skills and preferences</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-card"><div class="icon">🎯</div><h4>Zero Effort</h4><p>Just check the dashboard and apply to the ones you like</p></div>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <h3>🎯 Job Hunter Agent</h3>
        <p>Autonomous Job Search System | Powered by GitHub Actions</p>
        <p>Searches at 8:00 AM and 6:00 PM IST daily</p>
    </div>
    """, unsafe_allow_html=True)


def show_job_listings():
    """Show job listings"""
    
    st.markdown("""
    <div class="main-header">
        <h1>💼 Job Listings</h1>
        <p>Browse and manage all discovered job opportunities</p>
    </div>
    """, unsafe_allow_html=True)
    
    jobs = load_jobs()
    
    if not jobs:
        st.info("📋 No jobs found yet. The agent will search at 8 AM and 6 PM IST daily.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Status", ["All", "new", "processed", "low_fit"])
    with col2:
        search_term = st.text_input("🔍 Search (Company/Title)")
    
    filtered = jobs
    if status_filter != "All":
        filtered = [j for j in filtered if j.get("status") == status_filter]
    if search_term:
        search_lower = search_term.lower()
        filtered = [j for j in filtered if search_lower in j.get("title", "").lower() or search_lower in j.get("company", "").lower()]
    
    st.markdown(f'<h3 class="section-header">📋 Found {len(filtered)} Jobs</h3>', unsafe_allow_html=True)
    
    if filtered:
        display_data = [{"Title": j.get("title", ""), "Company": j.get("company", ""), "Location": j.get("location", ""), "Status": j.get("status", ""), "Platform": j.get("platform", "")} for j in filtered]
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
                    st.write("**Platform:**", selected_job.get("platform", ""))
                with col2:
                    st.write("**URL:**", selected_job.get("url", ""))
                    st.write("**Status:**", selected_job.get("status", ""))
                    st.write("**Job Type:**", selected_job.get("job_type", ""))
                
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
        st.info("📄 No resumes generated yet. Resumes will appear after the agent finds matching jobs.")
        return
    
    st.success(f"✅ {len(resumes)} resumes ready for download!")
    
    for resume in resumes:
        job_info = resume.get("job_info", {})
        title = job_info.get("Job Title", resume["folder"])
        company = job_info.get("Company", "")
        
        with st.expander(f"📁 {title} - {company}", expanded=False):
            st.write("**Fit Score:**", job_info.get("Fit Score", "N/A"))
            st.write("**Generated:**", job_info.get("Generated", "N/A"))
            
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
        <p>Understanding the autonomous job hunting agent</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">The System</h4>
        <ol>
            <li><strong>GitHub Actions</strong> - Runs the search automatically at 8 AM and 6 PM IST</li>
            <li><strong>Free Job APIs</strong> - Searches Arbeitnow, Remotive, and Jobicy</li>
            <li><strong>Resume Generator</strong> - Creates tailored resumes for matching jobs</li>
            <li><strong>Streamlit</strong> - This web interface to view results</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h4 style="margin-top: 0;">All You Need To Do:</h4>
        <ol>
            <li>🌅 <strong>Morning:</strong> Check this dashboard (2 minutes)</li>
            <li>📄 <strong>Review:</strong> Look at generated resumes</li>
            <li>✅ <strong>Apply:</strong> Apply to jobs you like (when you have time)</li>
        </ol>
        <p><strong>That's it! The agent does everything else.</strong></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
