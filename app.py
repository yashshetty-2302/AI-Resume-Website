import streamlit as st
from groq import Groq
import PyPDF2
import json
import base64
import os
from dotenv import load_dotenv

# --- LOAD ENV FILE ---
load_dotenv()

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Portfolio", layout="wide", page_icon="✨")

# --- CSS & STYLING (DARK THEME ENGINE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* --- GLOBAL DARK THEME SETUP --- */
    .stApp {
        background-color: #0f172a; /* Slate 900 */
        background-image: 
            radial-gradient(at 0% 0%, #1e293b 0px, transparent 50%), 
            radial-gradient(at 100% 0%, #312e81 0px, transparent 50%), /* Indigo tint */
            radial-gradient(at 100% 100%, #0f172a 0px, transparent 50%);
        background-attachment: fixed;
        background-size: cover;
        font-family: 'Inter', sans-serif;
        color: #f1f5f9; /* Slate 100 Text */
    }

    /* Sidebar - Glassy Dark Blend */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.6);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
    }
    
    /* Fix Sidebar Text Colors */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] p {
        color: #cbd5e1 !important; /* Slate 300 */
    }

    /* Headers & Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .glow-header {
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1000px;
    }

    /* --- COMPONENT STYLES --- */

    /* HERO SECTION */
    .hero-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        margin-bottom: 40px;
    }
    .hero-avatar {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid rgba(96, 165, 250, 0.5);
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.2);
        margin-bottom: 20px;
    }
    .hero-name {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 10px;
        color: #f8fafc;
    }
    .hero-title {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 24px;
    }

    /* SOCIAL LINKS */
    .social-links-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
    }
    .social-link {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px 24px;
        border-radius: 50px;
        color: #e2e8f0;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
    }
    .social-link:hover {
        background: rgba(96, 165, 250, 0.1);
        transform: translateY(-3px);
        border-color: #60a5fa;
        color: #60a5fa;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.4);
    }

    /* TIMELINE */
    .timeline-container {
        position: relative;
        padding-left: 35px;
        border-left: 2px solid #334155;
        margin-left: 10px;
        margin-bottom: 30px;
    }
    .timeline-dot {
        position: absolute;
        left: -8.5px;
        top: 24px;
        width: 15px;
        height: 15px;
        background: #60a5fa;
        border: 3px solid #0f172a;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(96, 165, 250, 0.4);
    }
    
    /* CARDS */
    .resume-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .resume-card:hover {
        background: rgba(30, 41, 59, 0.7);
        border-color: #475569;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* TYPOGRAPHY IN CARDS */
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }
    .card-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    .card-bullets li {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 6px;
    }
    .resume-card a {
        color: #60a5fa !important;
    }

    /* --- FIXED SKILLS PILLS (WITH GLOW) --- */
    .skill-category {
        font-weight: 700;
        color: #94a3b8;
        margin-bottom: 15px; /* Adjusted margin */
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 1.2px;
    }
    
    /* Technical Skills - Blue Glow */
    .skill-pill {
        display: inline-block;
        background: rgba(96, 165, 250, 0.1);
        color: #e2e8f0;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 6px 10px 0;
        border: 1px solid rgba(96, 165, 250, 0.3);
        box-shadow: 0 0 10px rgba(96, 165, 250, 0.2); /* Blue Glow */
        transition: all 0.3s ease;
    }
    .skill-pill:hover {
        background: rgba(96, 165, 250, 0.2);
        border-color: #60a5fa;
        color: #fff;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.5);
    }

    /* Soft Skills - Green Glow */
    .soft-skill-pill {
        display: inline-block;
        background: rgba(52, 211, 153, 0.1);
        color: #e2e8f0;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 6px 10px 0;
        border: 1px solid rgba(52, 211, 153, 0.3);
        box-shadow: 0 0 10px rgba(52, 211, 153, 0.2); /* Green Glow */
        transition: all 0.3s ease;
    }
    .soft-skill-pill:hover {
        background: rgba(52, 211, 153, 0.2);
        border-color: #34d399;
        color: #fff;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.5);
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #334155;
        padding-bottom: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #94a3b8;
        padding: 12px 24px;
        background: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.05);
        color: #60a5fa !important;
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid #60a5fa;
    }
    
    /* Fix File Uploader Dark Mode */
    [data-testid="stFileUploader"] {
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        padding: 20px;
        border: 1px dashed rgba(255,255,255,0.2);
    }
    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def clean_json_string(json_str):
    if "```json" in json_str:
        json_str = json_str.replace("```json", "").replace("```", "")
    elif "```" in json_str:
        json_str = json_str.replace("```", "")
    return json_str.strip()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def parse_resume_with_ai(text, client):
    """Parses resume text using Groq."""
    system_prompt = """
    You are an expert Resume Parser. Extract data into VALID JSON using strict logic.
    Ensure "description" fields are always lists of strings.
    If a summary is missing, generate a professional one based on the experience.
    
    REQUIRED JSON STRUCTURE:
    {
        "personal_info": { "name": "String", "email": "String", "phone": "String", "linkedin": "String", "github": "String", "location": "String", "summary": "String" },
        "experience": [ { "title": "String", "company": "String", "date": "String", "description": ["Bullet 1"] } ],
        "projects": [ { "title": "String", "tech_stack": "String", "link": "String (optional)", "description": ["Bullet 1"] } ],
        "education": [ { "degree": "String", "school": "String", "year": "String", "description": ["Optional bullet"] } ],
        "skills": { "languages": ["String"], "frameworks": ["String"], "developer_tools": ["String"], "soft_skills": ["String"] },
        "certifications": [ { "name": "String", "issuer": "String", "year": "String" } ]
    }
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"RESUME TEXT:\n{text}"}
            ],
            temperature=0.0, 
            response_format={"type": "json_object"} 
        )
        return json.loads(clean_json_string(response.choices[0].message.content))
    except Exception as e:
        st.error(f"Parsing Error: {e}")
        return None

# --- INITIALIZE CLIENT ---
if not GROQ_API_KEY:
    st.warning("⚠️ Please set your GROQ_API_KEY in the .env file")
    st.stop()
    
groq_client = Groq(api_key=GROQ_API_KEY)

# --- MAIN APP LOGIC ---

# Sidebar for upload
with st.sidebar:
    st.title("⚙️ Config")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")
    st.info("Upload your resume to generate the portfolio.")
    st.divider()
    st.caption("Made with ❤️ using Streamlit & Groq")

if uploaded_file:
    with st.spinner("Analyzing Resume & Generating Portfolio..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        if raw_text:
            data = parse_resume_with_ai(raw_text, groq_client)
            
            if data:
                # =========================================================
                # 🚀 FORCE LINKS (HARDCODED OVERRIDES)
                # This block overwrites whatever the AI found with your real links
                # =========================================================
                
                # 1. Force Social Media Links
                if 'personal_info' not in data: data['personal_info'] = {}
                data['personal_info']['linkedin'] = "[https://www.linkedin.com/in/yash-shetty-5614b62ab/](https://www.linkedin.com/in/yash-shetty-5614b62ab/)"
                data['personal_info']['github'] = "[https://github.com/yashshetty-2302](https://github.com/yashshetty-2302)"

                # 2. Force Project Links (Fuzzy Match Logic)
                if 'projects' in data:
                    for p in data['projects']:
                        t_lower = p.get('title', '').lower()
                        # Match "Report to Plate"
                        if "plate" in t_lower or "report" in t_lower:
                            p['link'] = "[https://github.com/yashshetty-2302/Report_Plate_AI](https://github.com/yashshetty-2302/Report_Plate_AI)"
                        # Match "Heart Disease"
                        elif "heart" in t_lower or "disease" in t_lower:
                            p['link'] = "[https://github.com/yashshetty-2302/heartdiseaseclassification](https://github.com/yashshetty-2302/heartdiseaseclassification)"

                # =========================================================
                # 🎨 RENDER UI
                # =========================================================

                # --- HERO SECTION ---
                p_info = data.get('personal_info', {})
                
                # Image Logic
                local_img = get_base64_image("profile_pic.jpg")
                img_src = f"data:image/jpg;base64,{local_img}" if local_img else "[https://cdn-icons-png.flaticon.com/512/3135/3135715.png](https://cdn-icons-png.flaticon.com/512/3135/3135715.png)"
                
                # Build Links HTML
                links_html = ""
                if p_info.get('email'):
                    links_html += f'<a href="mailto:{p_info["email"]}" class="social-link">📩 Email</a>'
                
                # We use the Hardcoded keys here
                links_html += f'<a href="{p_info["linkedin"]}" target="_blank" class="social-link">🔗 LinkedIn</a>'
                links_html += f'<a href="{p_info["github"]}" target="_blank" class="social-link">💻 GitHub</a>'

                st.markdown(f"""
                <div class="hero-card">
                    <img src="{img_src}" class="hero-avatar">
                    <div class="hero-name"><span class="glow-header">{p_info.get('name', 'Name Not Found')}</span></div>
                    <div class="hero-title">{p_info.get('location', 'Location')} • Open to Work</div>
                    <div style="margin-bottom: 25px; color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; max-width: 800px; margin-left: auto; margin-right: auto;">
                        {p_info.get('summary', '')}
                    </div>
                    <div class="social-links-container">
                        {links_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --- MAIN TABS ---
                tab1, tab2, tab3, tab4 = st.tabs(["💼 Experience", "🚀 Projects", "🛠 Skills", "🎓 Education"])

                # --- TAB 1: EXPERIENCE ---
                with tab1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    exps = data.get('experience', [])
                    if not exps:
                        st.info("No experience listed.")
                    
                    for exp in exps:
                        bullets = "".join([f"<li>{item}</li>" for item in exp.get('description', [])])
                        st.markdown(f"""
                        <div class="timeline-container">
                            <div class="timeline-dot"></div>
                            <div class="resume-card">
                                <div class="card-title">{exp.get('title')}</div>
                                <div class="card-subtitle">
                                    <span style="color: #94a3b8;">🏢 {exp.get('company')}</span>
                                    <span style="color: #60a5fa;">📅 {exp.get('date')}</span>
                                </div>
                                <ul class="card-bullets">{bullets}</ul>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # --- TAB 2: PROJECTS ---
                with tab2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    projects = data.get('projects', [])
                    if not projects:
                        st.info("No projects listed.")
                    
                    # Create grid
                    for i in range(0, len(projects), 2):
                        col1, col2 = st.columns(2)
                        
                        def render_project(proj):
                            bullets = "".join([f"<li>{item}</li>" for item in proj.get('description', [])])
                            
                            # Check for the Overridden Link
                            proj_link = proj.get('link')
                            link_html = ""
                            
                            if proj_link and proj_link not in ["#", "null", "None"]:
                                link_html = f"""
                                <div style="margin-top:15px;">
                                    <a href="{proj_link}" target="_blank" style="
                                        display: inline-block;
                                        background: rgba(96, 165, 250, 0.1);
                                        color: #60a5fa;
                                        padding: 8px 16px;
                                        border-radius: 8px;
                                        text-decoration: none;
                                        font-weight: 600;
                                        border: 1px solid rgba(96, 165, 250, 0.3);
                                        transition: all 0.2s;
                                    ">
                                    🔗 View Project
                                    </a>
                                </div>
                                """
                            
                            return f"""
                            <div class="resume-card" style="height: 100%; display: flex; flex-direction: column;">
                                <div class="card-title">{proj.get('title')}</div>
                                <div class="card-subtitle" style="color: #60a5fa;">🛠 {proj.get('tech_stack', 'Tech Stack')}</div>
                                <ul class="card-bullets" style="flex-grow: 1;">{bullets}</ul>
                                {link_html}
                            </div>
                            """
                        
                        with col1:
                            if i < len(projects):
                                st.markdown(render_project(projects[i]), unsafe_allow_html=True)
                        with col2:
                            if i + 1 < len(projects):
                                st.markdown(render_project(projects[i+1]), unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

                # --- TAB 3: SKILLS ---
                with tab3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    skills = data.get('skills', {})
                    
                    if isinstance(skills, dict):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown(f"""
                            <div class="resume-card">
                                <div class="skill-category">💻 Languages & Core</div>
                            """, unsafe_allow_html=True)
                            for s in skills.get('languages', []) + skills.get('technical', []):
                                st.markdown(f'<span class="skill-pill">{s}</span>', unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)

                            st.markdown(f"""
                            <div class="resume-card">
                                <div class="skill-category">🔧 Frameworks</div>
                            """, unsafe_allow_html=True)
                            for s in skills.get('frameworks', []):
                                st.markdown(f'<span class="skill-pill">{s}</span>', unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)

                        with col_b:
                            st.markdown(f"""
                            <div class="resume-card">
                                <div class="skill-category">⚙️ Developer Tools</div>
                            """, unsafe_allow_html=True)
                            for s in skills.get('developer_tools', []):
                                st.markdown(f'<span class="skill-pill">{s}</span>', unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)

                            st.markdown(f"""
                            <div class="resume-card">
                                <div class="skill-category">🤝 Soft Skills</div>
                            """, unsafe_allow_html=True)
                            for s in skills.get('soft_skills', []) + skills.get('soft', []):
                                st.markdown(f'<span class="soft-skill-pill">{s}</span>', unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)

                # --- TAB 4: EDUCATION & CERTS ---
                with tab4:
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("Education")
                        edu_list = data.get('education', [])
                        for edu in edu_list:
                             st.markdown(f"""
                            <div class="timeline-container">
                                <div class="timeline-dot" style="background: #a78bfa;"></div>
                                <div class="resume-card">
                                    <div class="card-title">{edu.get('degree')}</div>
                                    <div class="card-subtitle">
                                        <span>🏛 {edu.get('school')}</span>
                                        <span>🎓 {edu.get('year')}</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    with col2:
                        st.subheader("Certifications")
                        certs = data.get('certifications', [])
                        for cert in certs:
                            st.markdown(f"""
                            <div class="resume-card" style="padding: 20px;">
                                <div style="font-weight: 700; font-size: 1rem; color: #f1f5f9;">{cert.get('name')}</div>
                                <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 6px;">
                                    <span style="background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 4px;">{cert.get('issuer')}</span> 
                                    <span style="float: right;">{cert.get('year')}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
else:
    # --- LANDING PAGE STATE ---
    st.markdown("""
    <div style="text-align: center; margin-top: 100px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 20px;"><span class="glow-header">AI Resume Portfolio</span></h1>
        <p style="color: #94a3b8; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Upload your PDF resume to instantly generate a professional, interactive portfolio website powered by Llama 3.
        </p>
    </div>
    """, unsafe_allow_html=True)