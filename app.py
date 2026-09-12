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
import plotly.graph_objects as go
import requests
import base64
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
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a56db 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(26, 86, 219, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-card h3 {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card h1 {
        color: #1a56db;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-card p {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    .section-header {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1a56db;
        display: inline-block;
    }
    
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1a56db;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #22c55e;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-card .icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-card h4 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-new { background: #dbeafe; color: #1a56db; }
    .status-processed { background: #dcfce7; color: #22c55e; }
    .status-skipped { background: #fee2e2; color: #ef4444; }
    .status-low_fit { background: #fef3c7; color: #f59e0b; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] .stRadio > div > div > label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
    }
    
    .footer h3 { color: #1a56db; margin-bottom: 1rem; }
    .footer p { color: #94a3b8; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


def load_jobs():
    """Load jobs from JSON file"""
    jobs_file = Path("job_hunter/data/jobs.json")
    
    if not jobs_file.exists():
        return []
    
    with open(jobs_file, "r") as f:
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
        if folder.is_dir():
            resume_file = folder / "resume.txt"
            if resume_file.exists():
                job_details_file = folder / "job_details.txt"
                job_desc_file = folder / "job_description.txt"
                
                job_info = {}
                if job_details_file.exists():
                    with open(job_details_file, "r") as f:
                        for line in f:
                            if ":" in line:
                                key, value = line.split(":", 1)
                                job_info[key.strip()] = value.strip()
                
                resumes.append({
                    "folder": folder.name,
                    "path": str(folder),
                    "has_resume": True,
                    "has_job_details": job_details_file.exists(),
                    "has_job_description": job_desc_file.exists(),
                    "job_info": job_info
                })
    
    return resumes


def text_to_pdf(text: str) -> bytes:
    """Convert text to PDF using reportlab"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor='#1a56db',
            spaceAfter=12
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        elements = []
        
        for line in text.split('\n'):
            if line.strip():
                if line.isupper() or (len(line) < 50 and line.replace(' ', '').replace('&', '').replace('=', '').isalpha()):
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
    
    # Sidebar
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
            ["📊 Dashboard", "💼 Job Listings", "📄 Generated Resumes", "⚙️ Settings", "ℹ️ How It Works"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        jobs = load_jobs()
        new_count = sum(1 for j in jobs if j.get("status") == "new")
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Quick Stats</p>
            <h3 style="color: white; margin: 0.5rem 0;">{len(jobs)} Jobs</h3>
            <p style="color: #22c55e; font-size: 0.85rem; margin: 0;">{new_count} New</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "💼 Job Listings":
        show_job_listings()
    elif page == "📄 Generated Resumes":
        show_generated_resumes()
    elif page == "⚙️ Settings":
        show_settings()
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
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Jobs</h3>
            <h1>{len(jobs)}</h1>
            <p>All jobs found</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>New Jobs</h3>
            <h1>{new_count}</h1>
            <p>Ready to review</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Processed</h3>
            <h1>{processed_count}</h1>
            <p>Resumes generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Resumes</h3>
            <h1>{len(resumes)}</h1>
            <p>Ready to download</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">📊 Jobs by Status</h3>', unsafe_allow_html=True)
        
        status_counts = {}
        for job in jobs:
            status = job.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            colors = {
                "new": "#1a56db",
                "processed": "#22c55e",
                "low_fit": "#f59e0b",
                "skipped": "#ef4444"
            }
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                color=list(status_counts.keys()),
                color_discrete_map=colors,
                hole=0.4
            )
            fig.update_layout(
                showlegend=True,
                height=300,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No data yet. Jobs will appear here after the first search.")
    
    with col2:
        st.markdown('<h3 class="section-header">📈 Jobs by Platform</h3>', unsafe_allow_html=True)
        
        platform_counts = {}
        for job in jobs:
            platform = job.get("platform", "Unknown")
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        if platform_counts:
            fig = px.bar(
                x=list(platform_counts.keys()),
                y=list(platform_counts.values()),
                color=list(platform_counts.keys()),
                color_discrete_sequence=['#1a56db', '#7c3aed', '#22c55e', '#f59e0b'],
            )
            fig.update_layout(
                height=300,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Platform data will appear after the first search.")
    
    # Last search info
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
    
    # Features
    st.markdown("---")
    st.markdown('<h3 class="section-header">✨ What This Agent Does</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🔍</div>
            <h4>Smart Search</h4>
            <p>Automatically searches for AI/ML/Data Science jobs at 8 AM & 6 PM daily</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📝</div>
            <h4>Tailored Resumes</h4>
            <p>Generates ATS-optimized resumes customized for each job</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">✅</div>
            <h4>Fit Assessment</h4>
            <p>Automatically filters jobs based on your skills and preferences</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🎯</div>
            <h4>Zero Effort</h4>
            <p>Just check the dashboard and apply to the ones you like</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
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
        st.markdown("""
        <div class="info-box">
            <p>📋 No jobs found yet. The agent will search at 8 AM and 6 PM IST daily.</p>
            <p>Jobs will appear here automatically after the first search.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Filters
    st.markdown('<h3 class="section-header">🔍 Filters</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "new", "processed", "low_fit", "skipped"]
        )
    
    with col2:
        search_term = st.text_input("🔍 Search (Company/Title)")
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Newest", "Company", "Title"])
    
    # Apply filters
    filtered = jobs.copy()
    
    if status_filter != "All":
        filtered = [j for j in filtered if j.get("status") == status_filter]
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [j for j in filtered if 
                    search_lower in j.get("title", "").lower() or
                    search_lower in j.get("company", "").lower()]
    
    if sort_by == "Newest":
        filtered.sort(key=lambda x: x.get("scraped_date", ""), reverse=True)
    elif sort_by == "Company":
        filtered.sort(key=lambda x: x.get("company", ""))
    elif sort_by == "Title":
        filtered.sort(key=lambda x: x.get("title", ""))
    
    st.markdown(f'<h3 class="section-header">📋 Found {len(filtered)} Jobs</h3>', unsafe_allow_html=True)
    
    if filtered:
        # Create dataframe for display
        display_data = []
        for job in filtered:
            status = job.get("status", "unknown")
            display_data.append({
                "Title": job.get("title", ""),
                "Company": job.get("company", ""),
                "Location": job.get("location", ""),
                "Status": status,
                "Platform": job.get("platform", ""),
            })
        
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Job Details
        st.markdown('<h3 class="section-header">📝 Job Details</h3>', unsafe_allow_html=True)
        
        selected_title = st.selectbox(
            "Select a job to view details",
            [f"{j.get('title', '')} at {j.get('company', '')}" for j in filtered]
        )
        
        if selected_title:
            # Find the job
            selected_job = None
            for j in filtered:
                if f"{j.get('title', '')} at {j.get('company', '')}" == selected_title:
                    selected_job = j
                    break
            
            if selected_job:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="custom-card">
                        <h4 style="color: #1a56db;">Job Information</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Title:**", selected_job.get("title", ""))
                    st.write("**Company:**", selected_job.get("company", ""))
                    st.write("**Location:**", selected_job.get("location", ""))
                    st.write("**Platform:**", selected_job.get("platform", ""))
                    st.write("**Status:**", selected_job.get("status", ""))
                
                with col2:
                    st.markdown("""
                    <div class="custom-card">
                        <h4 style="color: #1a56db;">Application Details</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("**URL:**", selected_job.get("url", ""))
                    st.write("**Salary:**", selected_job.get("salary", "Not specified"))
                    st.write("**Job Type:**", selected_job.get("job_type", ""))
                    st.write("**Posted:**", selected_job.get("posted_date", ""))
                
                st.markdown("""
                <div class="custom-card">
                    <h4 style="color: #1a56db;">Job Description</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.text_area("Description", selected_job.get("description", ""), height=300, disabled=True)
    else:
        st.warning("No jobs match the selected filters.")


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
        st.markdown("""
        <div class="info-box">
            <p>📄 No resumes generated yet.</p>
            <p>Resumes will appear here automatically after the agent finds matching jobs.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.success(f"✅ {len(resumes)} resumes ready for download!")
    
    for resume in resumes:
        job_info = resume.get("job_info", {})
        title = job_info.get("Job Title", resume["folder"])
        company = job_info.get("Company", "")
        
        with st.expander(f"📁 {title} - {company}", expanded=False):
            
            # Job info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Fit Score:**", job_info.get("Fit Score", "N/A"))
            with col2:
                st.write("**Generated:**", job_info.get("Generated", "N/A"))
            with col3:
                st.write("**Status:**", job_info.get("Status", "new"))
            
            st.markdown("---")
            
            # Read and display resume
            resume_path = Path(resume["path"]) / "resume.txt"
            cover_letter_path = Path(resume["path"]) / "cover_letter.txt"
            job_desc_path = Path(resume["path"]) / "job_description.txt"
            
            # Resume content
            if resume_path.exists():
                with open(resume_path, "r", encoding="utf-8") as f:
                    resume_content = f.read()
                
                st.markdown('<h4 style="color: #1a56db;">📄 Resume</h4>', unsafe_allow_html=True)
                st.text_area("Resume", resume_content, height=400, disabled=True, key=f"resume_{resume['folder']}")
            
            # Cover letter
            if cover_letter_path.exists():
                with open(cover_letter_path, "r", encoding="utf-8") as f:
                    cover_letter = f.read()
                
                st.markdown('<h4 style="color: #1a56db;">✉️ Cover Letter</h4>', unsafe_allow_html=True)
                st.text_area("Cover Letter", cover_letter, height=300, disabled=True, key=f"cl_{resume['folder']}")
            
            # Download buttons
            st.markdown('<h4 style="color: #1a56db;">⬇️ Download</h4>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if resume_path.exists():
                    with open(resume_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.download_button(
                        label="📥 Download Resume (TXT)",
                        data=content,
                        file_name=f"resume_{resume['folder']}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            
            with col2:
                if resume_path.exists():
                    with open(resume_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    pdf_bytes = text_to_pdf(content)
                    if pdf_bytes:
                        st.download_button(
                            label="📄 Download Resume (PDF)",
                            data=pdf_bytes,
                            file_name=f"resume_{resume['folder']}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.info("PDF generation requires reportlab")
            
            with col3:
                if job_desc_path.exists():
                    with open(job_desc_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.download_button(
                        label="📋 Download Job Description",
                        data=content,
                        file_name=f"job_desc_{resume['folder']}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )


def show_settings():
    """Show settings"""
    
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your job search preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">👤 Your Profile</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">Contact Details</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Name", "Pavan Kumar Koti", disabled=True)
        st.text_input("Email", "kotipavankumar12@gmail.com", disabled=True)
        st.text_input("Phone", "+91 7893600187", disabled=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">Professional Links</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input("LinkedIn", "linkedin.com/in/pavan-kumar-koti-200b4438b", disabled=True)
        st.text_input("GitHub", "github.com/koti-pavan-kumar/", disabled=True)
        st.text_input("Location", "Ongole, Andhra Pradesh, India", disabled=True)
    
    st.markdown("---")
    st.markdown('<h3 class="section-header">🔍 Search Preferences</h3>', unsafe_allow_html=True)
    
    st.info("💡 Search preferences are configured in the GitHub repository. Edit `job_hunter/config.py` to change keywords or locations.")
    
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #1a56db;">Current Search Keywords</h4>
        <p>AI, ML, Machine Learning, Data Science, Python, Data Analyst, SWE</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #1a56db;">Preferred Locations</h4>
        <p>Remote, Bangalore, Hyderabad, Chennai, Pune</p>
    </div>
    """, unsafe_allow_html=True)


def show_how_it_works():
    """Show how the agent works"""
    
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ How It Works</h1>
        <p>Understanding the autonomous job hunting agent</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">🤖 Architecture</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #1a56db;">The System</h4>
        <p>This agent uses a 3-part architecture:</p>
        <ol>
            <li><strong>GitHub Actions</strong> - Runs the search automatically at 8 AM and 6 PM IST</li>
            <li><strong>Adzuna API</strong> - Real job search API (not web scraping)</li>
            <li><strong>Streamlit</strong> - This web interface to view results</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">📅 Schedule</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🌅</div>
            <h4>Morning Search</h4>
            <p><strong>8:00 AM IST</strong></p>
            <p>Searches for new AI/ML/Data Science jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🌆</div>
            <h4>Evening Search</h4>
            <p><strong>6:00 PM IST</strong></p>
            <p>Finds more opportunities throughout the day</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">📊 What Happens Each Run</h3>', unsafe_allow_html=True)
    
    steps = [
        ("🔍", "Search", "Finds jobs matching your skills from Adzuna API"),
        ("✅", "Filter", "Assesses fit score (1-10) based on keywords"),
        ("📝", "Generate", "Creates tailored resume for jobs with fit score 4+"),
        ("📁", "Save", "Saves jobs and resumes to the repository"),
        ("🔄", "Commit", "Pushes results back to GitHub automatically")
    ]
    
    cols = st.columns(len(steps))
    for i, (icon, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">🎯 Your Daily Workflow</h3>', unsafe_allow_html=True)
    
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
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🎯 Job Hunter Agent</h3>
        <p>Fully autonomous job hunting | Powered by GitHub Actions</p>
        <p>Searches at 8:00 AM and 6:00 PM IST daily</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
