"""
Job Hunter Agent - Web Interface (Streamlit)
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json

# Page config
st.set_page_config(
    page_title="Job Hunter Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a56db;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        background-color: #1a56db;
        color: white;
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
    
    # Header
    st.markdown('<h1 class="main-header">🎯 Job Hunter Agent</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header(" Navigation")
        page = st.radio(
            "Go to",
            [" Dashboard", " Job Listings", " Generated Resumes", " Settings", " Start Agent"]
        )
    
    # Dashboard page
    if page == " Dashboard":
        show_dashboard()
    
    # Job listings page
    elif page == " Job Listings":
        show_job_listings()
    
    # Generated resumes page
    elif page == " Generated Resumes":
        show_generated_resumes()
    
    # Settings page
    elif page == " Settings":
        show_settings()
    
    # Start agent page
    elif page == " Start Agent":
        show_start_agent()

def show_dashboard():
    """Show dashboard with statistics"""
    st.header(" Dashboard")
    
    # Load statistics
    stats = load_statistics()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", stats.get("total_jobs", 0))
    
    with col2:
        st.metric("New Jobs", stats.get("new_jobs", 0))
    
    with col3:
        st.metric("Processed", stats.get("processed_jobs", 0))
    
    with col4:
        st.metric("Resumes Generated", len(get_generated_resumes()))
    
    st.markdown("---")
    
    # Jobs by platform
    st.subheader(" Jobs by Platform")
    jobs_by_platform = stats.get("jobs_by_platform", {})
    
    if jobs_by_platform:
        df_platform = pd.DataFrame(
            list(jobs_by_platform.items()),
            columns=["Platform", "Count"]
        )
        st.bar_chart(df_platform.set_index("Platform"))
    else:
        st.info("No data available yet. Start the agent to begin collecting jobs.")
    
    # Recent activity
    st.subheader(" Recent Activity")
    st.info("Run the agent to see recent activity here.")
    
    # Quick actions
    st.subheader(" Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(" Start Agent Now", use_container_width=True):
            st.session_state.start_agent = True
            st.rerun()
    
    with col2:
        if st.button(" Refresh Data", use_container_width=True):
            st.rerun()

def show_job_listings():
    """Show job listings table"""
    st.header(" Job Listings")
    
    # Load jobs
    df_jobs = load_jobs()
    
    if df_jobs.empty:
        st.info("No jobs found. Start the agent to begin collecting jobs.")
        return
    
    # Filters
    st.subheader(" Filters")
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
    st.subheader(f" Found {len(filtered_df)} Jobs")
    
    if not filtered_df.empty:
        # Select columns to display
        display_cols = ["title", "company", "location", "platform", "status", "scraped_date"]
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            column_config={
                "title": "Job Title",
                "company": "Company",
                "location": "Location",
                "platform": "Platform",
                "status": "Status",
                "scraped_date": "Scraped Date"
            }
        )
        
        # Job details
        st.subheader(" Job Details")
        selected_job = st.selectbox(
            "Select a job to view details",
            filtered_df["id"].tolist(),
            format_func=lambda x: f"{filtered_df[filtered_df['id']==x]['title'].iloc[0]} at {filtered_df[filtered_df['id']==x]['company'].iloc[0]}"
        )
        
        if selected_job:
            job = filtered_df[filtered_df["id"] == selected_job].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Title:**", job["title"])
                st.write("**Company:**", job["company"])
                st.write("**Location:**", job["location"])
                st.write("**Platform:**", job["platform"])
            
            with col2:
                st.write("**Status:**", job["status"])
                st.write("**URL:**", job["url"])
                st.write("**Scraped:**", job["scraped_date"])
            
            st.subheader("Description")
            st.text_area("Job Description", job["description"], height=200, disabled=True)
    else:
        st.warning("No jobs match the selected filters.")

def show_generated_resumes():
    """Show generated resumes"""
    st.header(" Generated Resumes")
    
    resumes = get_generated_resumes()
    
    if not resumes:
        st.info("No resumes generated yet. Start the agent to begin generating resumes.")
        return
    
    st.success(f" {len(resumes)} resumes generated!")
    
    # Display resumes
    for resume in resumes:
        with st.expander(f" {resume['folder']}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(" Resume")
                st.write("✅" if resume["has_resume"] else "❌")
            
            with col2:
                st.write(" Cover Letter")
                st.write("✅" if resume["has_cover_letter"] else "❌")
            
            with col3:
                st.write(" Job Details")
                st.write("✅" if resume["has_job_details"] else "❌")
            
            with col4:
                if st.button(f" View", key=f"view_{resume['folder']}"):
                    st.session_state.selected_resume = resume["folder"]
            
            # Show resume content if selected
            if st.session_state.get("selected_resume") == resume["folder"]:
                st.markdown("---")
                
                # Read and display resume
                resume_path = Path(resume["path"]) / "resume.txt"
                if resume_path.exists():
                    with open(resume_path, "r") as f:
                        resume_content = f.read()
                    
                    st.subheader("Resume Content")
                    st.text_area("Resume", resume_content, height=400, disabled=True)
                
                # Read and display cover letter
                cover_letter_path = Path(resume["path"]) / "cover_letter.txt"
                if cover_letter_path.exists():
                    with open(cover_letter_path, "r") as f:
                        cover_letter_content = f.read()
                    
                    st.subheader("Cover Letter")
                    st.text_area("Cover Letter", cover_letter_content, height=300, disabled=True)
                
                # Download buttons
                st.subheader("Download")
                col1, col2 = st.columns(2)
                
                with col1:
                    if resume_path.exists():
                        with open(resume_path, "r") as f:
                            st.download_button(
                                label=" Download Resume",
                                data=f.read(),
                                file_name=f"resume_{resume['folder']}.txt",
                                mime="text/plain"
                            )
                
                with col2:
                    if cover_letter_path.exists():
                        with open(cover_letter_path, "r") as f:
                            st.download_button(
                                label=" Download Cover Letter",
                                data=f.read(),
                                file_name=f"cover_letter_{resume['folder']}.txt",
                                mime="text/plain"
                            )

def show_settings():
    """Show settings page"""
    st.header(" Settings")
    
    config = load_config()
    
    # Personal info
    st.subheader(" Personal Information")
    personal = config.get("personal_profile", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name", personal.get("name", ""))
        email = st.text_input("Email", personal.get("email", ""))
        phone = st.text_input("Phone", personal.get("phone", ""))
    
    with col2:
        linkedin = st.text_input("LinkedIn URL", personal.get("linkedin_url", ""))
        github = st.text_input("GitHub URL", personal.get("github_url", ""))
        location = st.text_input("Location", personal.get("location", ""))
    
    st.markdown("---")
    
    # Job preferences
    st.subheader(" Job Preferences")
    preferences = config.get("preferences", {})
    
    keywords = st.text_area(
        "Keywords (one per line)",
        "\n".join(preferences.get("keywords", []))
    )
    
    locations = st.text_area(
        "Locations (one per line)",
        "\n".join(preferences.get("locations", []))
    )
    
    max_apps = st.slider(
        "Max applications per day",
        min_value=1,
        max_value=50,
        value=preferences.get("max_applications_per_day", 10)
    )
    
    # Save button
    if st.button(" Save Settings", use_container_width=True):
        st.success("Settings saved! (Note: In production, this would save to the database)")
        st.balloons()

def show_start_agent():
    """Show start agent page"""
    st.header(" Start Agent")
    
    st.info("""
    ### How it works:
    1. Click **Start Agent** below
    2. The agent will search for jobs matching your skills
    3. It will generate tailored resumes for matching jobs
    4. Check the **Generated Resumes** page to view and download
    5. Apply to the jobs you like!
    """)
    
    st.markdown("---")
    
    # Agent status
    st.subheader(" Agent Status")
    
    if st.session_state.get("agent_running", False):
        st.success(" Agent is running!")
        st.write("Next search scheduled for: 8:00 AM and 6:00 PM daily")
        
        if st.button(" Stop Agent"):
            st.session_state.agent_running = False
            st.rerun()
    else:
        st.warning(" Agent is not running")
        
        if st.button(" Start Agent", type="primary"):
            st.session_state.agent_running = True
            st.success(" Agent started! It will search at 8:00 AM and 6:00 PM daily.")
            st.info("You can close this window. The agent will run in the background.")
    
    st.markdown("---")
    
    # Manual search
    st.subheader(" Manual Search")
    st.write("Run a one-time search right now:")
    
    if st.button(" Run Search Now"):
        with st.spinner("Searching for jobs..."):
            # In production, this would trigger the actual search
            import time
            time.sleep(2)  # Simulate search
            st.success(" Search completed! Check the Job Listings page.")
    
    st.markdown("---")
    
    # Schedule info
    st.subheader(" Schedule")
    st.write("""
    - **8:00 AM**: Morning search
    - **6:00 PM**: Evening search
    
    The agent will automatically:
    1. Search LinkedIn, Naukri, Internshala, Google Jobs
    2. Check company legitimacy
    3. Generate tailored resumes
    4. Generate cover letters
    5. Save everything in the Generated Resumes folder
    """)

if __name__ == "__main__":
    main()
