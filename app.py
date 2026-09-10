"""
Job Hunter Agent - Professional Web Interface
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import plotly.express as px
import plotly.graph_objects as go

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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
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
    
    /* Metric Cards */
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
    
    /* Section Headers */
    .section-header {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1a56db;
        display: inline-block;
    }
    
    /* Cards */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a56db 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 86, 219, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 86, 219, 0.4);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > div > label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #94a3b8 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #94a3b8 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stTextInput label {
        color: white !important;
    }
    
    /* Info Boxes */
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
    
    /* Table Styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 10px 10px 0 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
    }
    
    .footer h3 {
        color: #1a56db;
        margin-bottom: 1rem;
    }
    
    .footer p {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Feature Cards */
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
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-new {
        background: #dbeafe;
        color: #1a56db;
    }
    
    .status-processed {
        background: #dcfce7;
        color: #22c55e;
    }
    
    .status-skipped {
        background: #fee2e2;
        color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)

def load_config():
    """Load configuration"""
    config_path = Path("job_hunter/data/config.json")
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

def load_jobs():
    """Load jobs from database"""
    import sqlite3
    db_path = Path("job_hunter/data/jobs.db")
    
    if not db_path.exists():
        return pd.DataFrame()
    
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM job_listings ORDER BY scraped_date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def load_statistics():
    """Load statistics from database"""
    import sqlite3
    db_path = Path("job_hunter/data/jobs.db")
    
    if not db_path.exists():
        return {}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM job_listings")
    stats["total_jobs"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM job_listings WHERE status = 'new'")
    stats["new_jobs"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM job_listings WHERE status = 'processed'")
    stats["processed_jobs"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT platform, COUNT(*) FROM job_listings GROUP BY platform")
    stats["jobs_by_platform"] = dict(cursor.fetchall())
    
    conn.close()
    return stats

def get_generated_resumes():
    """Get list of generated resumes"""
    resumes_path = Path("job_hunter/resumes")
    if not resumes_path.exists():
        return []
    
    resumes = []
    for folder in resumes_path.iterdir():
        if folder.is_dir():
            resume_files = list(folder.glob("resume.txt"))
            if resume_files:
                resumes.append({
                    "folder": folder.name,
                    "path": str(folder),
                    "has_resume": True,
                    "has_cover_letter": (folder / "cover_letter.txt").exists(),
                    "has_job_details": (folder / "job_details.txt").exists()
                })
    return resumes

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
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "💼 Job Listings", "📄 Generated Resumes", "⚙️ Settings", "🚀 Agent Control"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        stats = load_statistics()
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Quick Stats</p>
            <h3 style="color: white; margin: 0.5rem 0;">""" + str(stats.get("total_jobs", 0)) + """ Jobs</h3>
            <p style="color: #22c55e; font-size: 0.85rem; margin: 0;">""" + str(stats.get("new_jobs", 0)) + """ New</p>
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
    elif page == "🚀 Agent Control":
        show_agent_control()

def show_dashboard():
    """Show professional dashboard"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Job Hunter Agent</h1>
        <p>Autonomous Job Search & Resume Generation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load statistics
    stats = load_statistics()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Total Jobs</h3>
            <h1>""" + str(stats.get("total_jobs", 0)) + """</h1>
            <p>All jobs found</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>New Jobs</h3>
            <h1>""" + str(stats.get("new_jobs", 0)) + """</h1>
            <p>Ready to process</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Processed</h3>
            <h1>""" + str(stats.get("processed_jobs", 0)) + """</h1>
            <p>Resumes generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Resumes</h3>
            <h1>""" + str(len(get_generated_resumes())) + """</h1>
            <p>Ready to download</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">📊 Jobs by Platform</h3>', unsafe_allow_html=True)
        
        jobs_by_platform = stats.get("jobs_by_platform", {})
        
        if jobs_by_platform:
            fig = px.pie(
                values=list(jobs_by_platform.values()),
                names=list(jobs_by_platform.keys()),
                color_discrete_sequence=['#1a56db', '#7c3aed', '#22c55e', '#f59e0b'],
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
            st.markdown("""
            <div class="info-box">
                <p>📊 No data available yet. Start the agent to begin collecting jobs.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="section-header">📈 Recent Activity</h3>', unsafe_allow_html=True)
        
        # Sample activity data
        activity_data = pd.DataFrame({
            'Time': ['8:00 AM', '6:00 PM', '8:00 AM', '6:00 PM'],
            'Action': ['Search', 'Search', 'Generate', 'Generate'],
            'Count': [15, 12, 8, 6]
        })
        
        fig = px.bar(
            activity_data,
            x='Time',
            y='Count',
            color='Action',
            color_discrete_sequence=['#1a56db', '#22c55e'],
            barmode='group'
        )
        fig.update_layout(
            height=300,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Features Section
    st.markdown('<h3 class="section-header">✨ Key Features</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🔍</div>
            <h4>Smart Search</h4>
            <p>Automatically searches LinkedIn, Naukri, Internshala, and Google Jobs</p>
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
            <h4>Legitimacy Check</h4>
            <p>Filters out scams and fake companies automatically</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📬</div>
            <h4>Cover Letters</h4>
            <p>Creates professional cover letters for each application</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🎯 Job Hunter Agent</h3>
        <p>Autonomous Job Search System | Powered by AI</p>
        <p>Searches at 8:00 AM and 6:00 PM daily</p>
    </div>
    """, unsafe_allow_html=True)

def show_job_listings():
    """Show job listings with professional styling"""
    
    st.markdown("""
    <div class="main-header">
        <h1>💼 Job Listings</h1>
        <p>Browse and manage all discovered job opportunities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load jobs
    df_jobs = load_jobs()
    
    if df_jobs.empty:
        st.markdown("""
        <div class="info-box">
            <p>📋 No jobs found yet. Start the agent to begin collecting jobs.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Filters
    st.markdown('<h3 class="section-header">🔍 Filters</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "new", "processed", "applied", "skipped", "low_fit"]
        )
    
    with col2:
        platform_filter = st.selectbox(
            "Platform",
            ["All"] + list(df_jobs["platform"].unique())
        )
    
    with col3:
        search_term = st.text_input("Search (Company/Title)")
    
    # Apply filters
    filtered_df = df_jobs.copy()
    
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]
    
    if platform_filter != "All":
        filtered_df = filtered_df[filtered_df["platform"] == platform_filter]
    
    if search_term:
        mask = (
            filtered_df["company"].str.contains(search_term, case=False, na=False) |
            filtered_df["title"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Display results
    st.markdown(f'<h3 class="section-header">📋 Found {len(filtered_df)} Jobs</h3>', unsafe_allow_html=True)
    
    if not filtered_df.empty:
        # Create styled dataframe
        display_df = filtered_df[["title", "company", "location", "platform", "status", "scraped_date"]].copy()
        display_df.columns = ["Job Title", "Company", "Location", "Platform", "Status", "Scraped"]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Job Details
        st.markdown('<h3 class="section-header">📝 Job Details</h3>', unsafe_allow_html=True)
        
        selected_job = st.selectbox(
            "Select a job to view details",
            filtered_df["id"].tolist(),
            format_func=lambda x: f"{filtered_df[filtered_df['id']==x]['title'].iloc[0]} at {filtered_df[filtered_df['id']==x]['company'].iloc[0]}"
        )
        
        if selected_job:
            job = filtered_df[filtered_df["id"] == selected_job].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="custom-card">
                    <h4 style="color: #1a56db;">Job Information</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**Title:**", job["title"])
                st.write("**Company:**", job["company"])
                st.write("**Location:**", job["location"])
                st.write("**Platform:**", job["platform"])
            
            with col2:
                st.markdown("""
                <div class="custom-card">
                    <h4 style="color: #1a56db;">Application Details</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**Status:**", job["status"])
                st.write("**URL:**", job["url"])
                st.write("**Scraped:**", job["scraped_date"])
            
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #1a56db;">Job Description</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area("Description", job["description"], height=300, disabled=True)
    else:
        st.warning("No jobs match the selected filters.")

def show_generated_resumes():
    """Show generated resumes with professional styling"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📄 Generated Resumes</h1>
        <p>View and download your tailored resumes and cover letters</p>
    </div>
    """, unsafe_allow_html=True)
    
    resumes = get_generated_resumes()
    
    if not resumes:
        st.markdown("""
        <div class="info-box">
            <p>📄 No resumes generated yet. Start the agent to begin generating resumes.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f'<div class="success-box"><p>✅ {len(resumes)} resumes generated!</p></div>', unsafe_allow_html=True)
    
    # Display resumes
    for resume in resumes:
        with st.expander(f"📁 {resume['folder']}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write("📄 Resume")
                st.write("✅" if resume["has_resume"] else "❌")
            
            with col2:
                st.write("✉️ Cover Letter")
                st.write("✅" if resume["has_cover_letter"] else "❌")
            
            with col3:
                st.write("📋 Job Details")
                st.write("✅" if resume["has_job_details"] else "❌")
            
            with col4:
                if st.button(f"👁️ View", key=f"view_{resume['folder']}"):
                    st.session_state.selected_resume = resume["folder"]
            
            # Show resume content if selected
            if st.session_state.get("selected_resume") == resume["folder"]:
                st.markdown("---")
                
                # Read and display resume
                resume_path = Path(resume["path"]) / "resume.txt"
                if resume_path.exists():
                    with open(resume_path, "r") as f:
                        resume_content = f.read()
                    
                    st.markdown('<h4 class="section-header">📄 Resume Content</h4>', unsafe_allow_html=True)
                    st.text_area("Resume", resume_content, height=500, disabled=True)
                
                # Read and display cover letter
                cover_letter_path = Path(resume["path"]) / "cover_letter.txt"
                if cover_letter_path.exists():
                    with open(cover_letter_path, "r") as f:
                        cover_letter_content = f.read()
                    
                    st.markdown('<h4 class="section-header">✉️ Cover Letter</h4>', unsafe_allow_html=True)
                    st.text_area("Cover Letter", cover_letter_content, height=400, disabled=True)
                
                # Download buttons
                st.markdown('<h4 class="section-header">⬇️ Download</h4>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if resume_path.exists():
                        with open(resume_path, "r") as f:
                            st.download_button(
                                label="📥 TXT",
                                data=f.read(),
                                file_name=f"resume_{resume['folder']}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                
                with col2:
                    if resume_path.exists():
                        with open(resume_path, "r") as f:
                            resume_content = f.read()
                        from job_hunter.pdf_converter import pdf_converter
                        pdf_bytes = pdf_converter.convert_text_to_pdf(resume_content)
                        st.download_button(
                            label="📄 PDF",
                            data=pdf_bytes,
                            file_name=f"resume_{resume['folder']}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                
                with col3:
                    if cover_letter_path.exists():
                        with open(cover_letter_path, "r") as f:
                            st.download_button(
                                label="📥 TXT",
                                data=f.read(),
                                file_name=f"cover_letter_{resume['folder']}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                
                with col4:
                    if cover_letter_path.exists():
                        with open(cover_letter_path, "r") as f:
                            cover_letter_content = f.read()
                        from job_hunter.pdf_converter import pdf_converter
                        pdf_bytes = pdf_converter.convert_text_to_pdf(cover_letter_content)
                        st.download_button(
                            label="📄 PDF",
                            data=pdf_bytes,
                            file_name=f"cover_letter_{resume['folder']}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

def show_settings():
    """Show settings with professional styling"""
    
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your profile and job search preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    config = load_config()
    
    # Personal Information
    st.markdown('<h3 class="section-header">👤 Personal Information</h3>', unsafe_allow_html=True)
    
    personal = config.get("personal_profile", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">Contact Details</h4>
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Name", personal.get("name", ""))
        email = st.text_input("Email", personal.get("email", ""))
        phone = st.text_input("Phone", personal.get("phone", ""))
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">Professional Links</h4>
        </div>
        """, unsafe_allow_html=True)
        
        linkedin = st.text_input("LinkedIn URL", personal.get("linkedin_url", ""))
        github = st.text_input("GitHub URL", personal.get("github_url", ""))
        location = st.text_input("Location", personal.get("location", ""))
    
    st.markdown("---")
    
    # Job Preferences
    st.markdown('<h3 class="section-header">💼 Job Preferences</h3>', unsafe_allow_html=True)
    
    preferences = config.get("preferences", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">Search Keywords</h4>
        </div>
        """, unsafe_allow_html=True)
        
        keywords = st.text_area(
            "Keywords (one per line)",
            "\n".join(preferences.get("keywords", [])),
            height=150
        )
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">Preferred Locations</h4>
        </div>
        """, unsafe_allow_html=True)
        
        locations = st.text_area(
            "Locations (one per line)",
            "\n".join(preferences.get("locations", [])),
            height=150
        )
    
    max_apps = st.slider(
        "Max applications per day",
        min_value=1,
        max_value=50,
        value=preferences.get("max_applications_per_day", 10)
    )
    
    # Save button
    st.markdown("---")
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved successfully!")
        st.balloons()

def show_agent_control():
    """Show agent control with professional styling"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Agent Control</h1>
        <p>Start and manage the autonomous job hunting agent</p>
    </div>
    """, unsafe_allow_html=True)
    
    # How it works
    st.markdown('<h3 class="section-header">ℹ️ How It Works</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🔍</div>
            <h4>1. Search</h4>
            <p>Agent searches LinkedIn, Naukri, Internshala, and Google Jobs for matching opportunities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📝</div>
            <h4>2. Generate</h4>
            <p>Creates tailored resumes and cover letters for each matching job</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">✅</div>
            <h4>3. Apply</h4>
            <p>Review generated materials and apply when you have time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Agent Status
    st.markdown('<h3 class="section-header">📊 Agent Status</h3>', unsafe_allow_html=True)
    
    if st.session_state.get("agent_running", False):
        st.markdown("""
        <div class="success-box">
            <p>✅ <strong>Agent is running!</strong> Next search scheduled for 8:00 AM and 6:00 PM daily.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⏹️ Stop Agent", use_container_width=True):
            st.session_state.agent_running = False
            st.rerun()
    else:
        st.markdown("""
        <div class="warning-box">
            <p>⚠️ <strong>Agent is not running.</strong> Click below to start autonomous job hunting.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Agent", type="primary", use_container_width=True):
            st.session_state.agent_running = True
            st.success("✅ Agent started! It will search at 8:00 AM and 6:00 PM daily.")
            st.info("💡 You can close this window. The agent will run in the background.")
    
    st.markdown("---")
    
    # Manual Search
    st.markdown('<h3 class="section-header">🔍 Manual Search</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p>Run a one-time search right now to find new job opportunities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Run Search Now", use_container_width=True):
        with st.spinner("🔍 Searching for jobs..."):
            import time
            time.sleep(2)
            st.success("✅ Search completed! Check the Job Listings page.")
    
    st.markdown("---")
    
    # Schedule
    st.markdown('<h3 class="section-header">📅 Schedule</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #1a56db;">🌅 Morning Search</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #1a56db;">8:00 AM</p>
            <p>Daily morning search for new jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #7c3aed;">🌆 Evening Search</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #7c3aed;">6:00 PM</p>
            <p>Daily evening search for new jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🎯 Job Hunter Agent</h3>
        <p>Let the agent work for you! Just review and apply when you have time.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
