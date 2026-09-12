"""
Job Hunter Agent - Professional Web Interface with Cookie Upload
Works on Streamlit Cloud - no local browser needed
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import plotly.express as px
import io

st.set_page_config(page_title="Job Hunter Agent", page_icon="...", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; }
    .main-header { background: linear-gradient(135deg, #1a56db 0%, #7c3aed 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 10px 40px rgba(26, 86, 219, 0.3); }
    .main-header h1 { color: white; font-size: 2.5rem; font-weight: 700; margin: 0; text-align: center; }
    .main-header p { color: rgba(255,255,255,0.9); font-size: 1.1rem; text-align: center; margin-top: 0.5rem; }
    .metric-card { background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center; transition: transform 0.3s ease; border: 1px solid rgba(0,0,0,0.05); }
    .metric-card:hover { transform: translateY(-5px); }
    .metric-card h3 { color: #64748b; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; }
    .metric-card h1 { color: #1a56db; font-size: 2.5rem; font-weight: 700; margin: 0; }
    .metric-card p { color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem; }
    .section-header { color: #1e293b; font-size: 1.5rem; font-weight: 600; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 3px solid #1a56db; display: inline-block; }
    .feature-card { background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center; height: 100%; }
    .feature-card .icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .feature-card h4 { color: #1e293b; font-weight: 600; margin-bottom: 0.5rem; }
    .feature-card p { color: #64748b; font-size: 0.9rem; }
    .info-box { background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #1a56db; margin: 1rem 0; }
    .success-box { background: linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #22c55e; margin: 1rem 0; }
    .warning-box { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #f59e0b; margin: 1rem 0; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); }
    [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stRadio > div > div > label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: white !important; }
    .footer { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; padding: 2rem; border-radius: 15px; margin-top: 3rem; text-align: center; }
    .footer h3 { color: #1a56db; margin-bottom: 1rem; }
    .footer p { color: #94a3b8; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


# --------------------- DATA HELPERS ---------------------

COOKIES_DIR = Path("job_hunter/data/cookies")
COOKIES_DIR.mkdir(parents=True, exist_ok=True)

def save_cookie(platform: str, cookie_text: str):
    COOKIES_DIR.write_text(f"{platform.lower()}_cookies.txt")
    (COOKIES_DIR / f"{platform.lower()}_cookies.txt").write_text(cookie_text, encoding="utf-8")

def get_cookie(platform: str):
    f = COOKIES_DIR / f"{platform.lower()}_cookies.txt"
    return f.read_text(encoding="utf-8").strip() if f.exists() else None

def cookie_status():
    return {
        "LinkedIn": (COOKIES_DIR / "linkedin_cookies.txt").exists(),
        "Internshala": (COOKIES_DIR / "internshala_cookies.txt").exists(),
        "Unstop": (COOKIES_DIR / "unstop_cookies.txt").exists(),
    }

def load_jobs():
    jobs_file = Path("job_hunter/data/agent_jobs")
    all_jobs = []
    if jobs_file.exists():
        for f in jobs_file.glob("*.json"):
            try:
                all_jobs.extend(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass
    return all_jobs

def get_resumes():
    resumes_path = Path("job_hunter/resumes")
    if not resumes_path.exists(): return []
    resumes = []
    for folder in resumes_path.iterdir():
        if folder.is_dir() and (folder / "resume.txt").exists():
            info = {}
            det = folder / "job_details.txt"
            if det.exists():
                for line in det.read_text(encoding="utf-8").splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        info[k.strip()] = v.strip()
            resumes.append({"folder": folder.name, "path": str(folder), "info": info})
    return resumes

def text_to_pdf(text):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        ts = ParagraphStyle("T", parent=styles["Heading1"], fontSize=16, textColor="#1a56db", spaceAfter=12)
        ns = ParagraphStyle("N", parent=styles["Normal"], fontSize=10, spaceAfter=6)
        elems = []
        for line in text.split("\n"):
            if line.strip():
                elems.append(Paragraph(line.strip(), ts if line.isupper() or len(line) < 50 else ns))
            else:
                elems.append(Spacer(1, 6))
        doc.build(elems)
        return buf.getvalue()
    except ImportError:
        return None


# --------------------- SIDEBAR ---------------------

with st.sidebar:
    st.markdown('<div style="text-align:center;padding:1rem"><h2 style="color:white;margin:0">... Job Hunter</h2><p style="color:#94a3b8;font-size:0.85rem">AI-Powered Job Search Agent</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["... Dashboard", "... Connect Platforms", "... Job Listings", "... Resumes", "... How It Works"], label_visibility="collapsed")
    st.markdown("---")
    jobs = load_jobs()
    st.markdown(f'<div style="background:rgba(255,255,255,0.1);padding:1rem;border-radius:10px"><p style="color:#94a3b8;font-size:0.8rem;margin:0">Quick Stats</p><h3 style="color:white;margin:0.5rem 0">{len(jobs)} Jobs</h3></div>', unsafe_allow_html=True)


# --------------------- PAGES ---------------------

def show_dashboard():
    st.markdown('<div class="main-header"><h1>... Job Hunter Agent</h1><p>AI-Powered Autonomous Job Search & Resume Generation</p></div>', unsafe_allow_html=True)
    jobs = load_jobs()
    resumes = get_resumes()
    status = cookie_status()
    connected = sum(status.values())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Jobs", len(jobs))
    c2.metric("Platforms Connected", f"{connected}/3")
    c3.metric("Resumes Ready", len(resumes))
    c4.metric("Status", "Active" if connected else "Needs Setup")

    st.markdown("---")
    st.markdown('<h3 class="section-header">... Platform Status</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (name, ok) in zip([c1, c2, c3], status.items()):
        with col:
            icon = {"LinkedIn": "...", "Internshala": "...", "Unstop": "..."}[name]
            st.markdown(f'<div class="feature-card"><div class="icon">{icon}</div><h4>{name}</h4><p>{"... Connected" if ok else "... Not Connected"}</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 class="section-header">... How It Works</h3>', unsafe_allow_html=True)
    cols = st.columns(4)
    steps = [("...", "Paste Cookies", "Copy cookies from browser, paste here"), ("...", "Agent Runs", "Reads your recommended jobs automatically"), ("...", "Skill Matching", "Filters jobs matching AI/ML/DS/Python"), ("...", "Resumes", "Generates tailored resumes for each job")]
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f'<div class="feature-card"><div class="icon">{icon}</div><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)


def show_connect():
    st.markdown('<div class="main-header"><h1>... Connect Platforms</h1><p>Paste your session cookies to let the agent read your recommended jobs</p></div>', unsafe_allow_html=True)
    status = cookie_status()

    # --- HOW TO GET COOKIES ---
    st.markdown('<h3 class="section-header">... How To Get Your Cookies</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">3-Step Process (takes 2 minutes per platform)</h4>
    <ol>
    <li><b>Open the platform</b> in Chrome and <b>login</b> normally</li>
    <li>Press <b>F12</b> to open Developer Tools</li>
    <li>Go to <b>Network</b> tab, click any request, find the <b>Cookie</b> header, copy the full value</li>
    <li><b>Paste</b> it below and click Save</li>
    </ol>
    <p><b>Tip:</b> The cookie value is a long string like <code>_li_s=AQE...; li_at=AQ...; ...</code></p>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP-BY-STEP FOR EACH PLATFORM ---
    platforms = [
        ("LinkedIn", "...", "https://www.linkedin.com/feed/"),
        ("Internshala", "...", "https://internshala.com/dashboard"),
        ("Unstop", "...", "https://unstop.com/dashboard"),
    ]

    for name, icon, login_url in platforms:
        connected = status[name]
        with st.expander(f"{icon} {name}  {'... Connected' if connected else '... Not Connected'}", expanded=not connected):
            if connected:
                st.success(f"... {name} cookies are saved!")
                st.markdown(f"**Login URL:** [{login_url}]({login_url})")
                if st.button(f"... Remove {name} Cookies", key=f"del_{name}"):
                    (COOKIES_DIR / f"{name.lower()}_cookies.txt").unlink(missing_ok=True)
                    st.rerun()
            else:
                st.warning(f"... {name} not connected yet. Follow the steps below:")
                st.markdown(f"""
                1. Open **[{login_url}]({login_url})** and **login**
                2. Press **F12** to open Developer Tools
                3. Go to **Network** tab
                4. Refresh the page
                5. Click any request in the Network tab
                6. Find the **Request Headers** section
                7. Copy the full **Cookie** value (long string)
                8. Paste it in the box below
                """)

                cookie_input = st.text_area(
                    f"Paste {name} cookie value here",
                    height=100,
                    key=f"cookie_{name}",
                    placeholder=f"Paste your {name} cookie here..."
                )

                if st.button(f"... Save {name} Cookies", key=f"save_{name}", type="primary"):
                    if cookie_input.strip():
                        save_cookie(name, cookie_input.strip())
                        st.success(f"... {name} cookies saved!")
                        st.rerun()
                    else:
                        st.error("Please paste a cookie value first")

    # --- RUN AGENT ---
    st.markdown("---")
    any_connected = any(status.values())
    st.markdown('<h3 class="section-header">... Run Agent</h3>', unsafe_allow_html=True)

    if any_connected:
        st.success("... Ready to search! Click below to find jobs from connected platforms.")
        if st.button("... Run Agent Now", type="primary", use_container_width=True):
            with st.spinner("... Agent is reading your recommended jobs..."):
                from job_hunter.agent.cookie_agent import CookieAgent
                agent = CookieAgent()
                # Copy saved cookies to agent's cookie dir
                for p in ["LinkedIn", "Internshala", "Unstop"]:
                    c = get_cookie(p)
                    if c:
                        agent.save_cookies(p, c)
                total = agent.run_all()
                st.success(f"... Done! Found {total} relevant jobs. Check Job Listings page.")
    else:
        st.warning("Please connect to at least one platform above first.")


def show_jobs():
    st.markdown('<div class="main-header"><h1>... Job Listings</h1><p>Jobs found from your recommended feeds</p></div>', unsafe_allow_html=True)
    jobs = load_jobs()
    if not jobs:
        st.info("... No jobs found yet. Connect platforms and run the agent first.")
        return

    search = st.text_input("... Search by title or company")
    filtered = jobs
    if search:
        q = search.lower()
        filtered = [j for j in filtered if q in j.get("title", "").lower() or q in j.get("company", "").lower()]

    st.markdown(f'<h3 class="section-header">... {len(filtered)} Jobs Found</h3>', unsafe_allow_html=True)
    if filtered:
        df = pd.DataFrame([{"Title": j.get("title",""), "Company": j.get("company",""), "Platform": j.get("platform",""), "Location": j.get("location","")} for j in filtered])
        st.dataframe(df, use_container_width=True, height=400)

        sel = st.selectbox("Select a job to view", [f"{j.get('title','')} at {j.get('company','')}" for j in filtered])
        if sel:
            job = next((j for j in filtered if f"{j.get('title','')} at {j.get('company','')}" == sel), None)
            if job:
                st.write("**Title:**", job.get("title",""))
                st.write("**Company:**", job.get("company",""))
                st.write("**Platform:**", job.get("platform",""))
                st.write("**URL:**", job.get("url",""))
                st.text_area("Description", job.get("description",""), height=300, disabled=True)


def show_resumes():
    st.markdown('<div class="main-header"><h1>... Generated Resumes</h1><p>Download tailored resumes</p></div>', unsafe_allow_html=True)
    resumes = get_resumes()
    if not resumes:
        st.info("... No resumes yet. Run the agent to generate them.")
        return
    for r in resumes:
        info = r["info"]
        with st.expander(f"... {info.get('Job Title', r['folder'])} - {info.get('Company','')}"):
            rp = Path(r["path"]) / "resume.txt"
            if rp.exists():
                content = rp.read_text(encoding="utf-8")
                st.text_area("Resume", content, height=400, disabled=True, key=r["folder"])
                c1, c2 = st.columns(2)
                c1.download_button("... Download TXT", content, f"resume_{r['folder']}.txt", "text/plain", use_container_width=True)
                pdf = text_to_pdf(content)
                if pdf:
                    c2.download_button("... Download PDF", pdf, f"resume_{r['folder']}.pdf", "application/pdf", use_container_width=True)


def show_how():
    st.markdown('<div class="main-header"><h1>... How It Works</h1><p>Understanding the cookie-based agent</p></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">... Architecture</h4>
    <ol>
    <li><b>Cookie Upload:</b> You copy session cookies from your browser and paste into the web app</li>
    <li><b>API Calls:</b> Agent uses those cookies to call LinkedIn/Internshala/Unstop like your browser would</li>
    <li><b>Job Extraction:</b> Reads your recommended jobs from each platform</li>
    <li><b>Skill Matching:</b> Filters for AI/ML/Data Science/Python jobs only</li>
    <li><b>Resume Generation:</b> Creates tailored resumes for each matching job</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="success-box">
    <h4 style="margin-top:0">... Security</h4>
    <ul>
    <li>... Password is NEVER stored - only session cookie</li>
    <li>... Cookies stored in Streamlit's secure storage</li>
    <li>... You can remove cookies anytime</li>
    <li>... Cookies expire after ~30 days (just paste new ones)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


# --------------------- ROUTER ---------------------

if page == "... Dashboard":
    show_dashboard()
elif page == "... Connect Platforms":
    show_connect()
elif page == "... Job Listings":
    show_jobs()
elif page == "... Resumes":
    show_resumes()
elif page == "... How It Works":
    show_how()
