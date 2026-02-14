import streamlit as st
import json
import time
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Career Navigator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Cinematic Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1147 50%, #0f2167 100%);
        background-attachment: fixed;
    }
    
    /* Floating background blobs */
    .stApp::before {
        content: '';
        position: fixed;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(103,58,183,0.3) 0%, transparent 70%);
        border-radius: 50%;
        top: -200px;
        right: -200px;
        animation: float 20s infinite ease-in-out;
        z-index: 0;
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(33,150,243,0.2) 0%, transparent 70%);
        border-radius: 50%;
        bottom: -150px;
        left: -150px;
        animation: float 15s infinite ease-in-out reverse;
        z-index: 0;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(50px, 50px) scale(1.1); }
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(103,58,183,0.3); }
        50% { box-shadow: 0 0 40px rgba(103,58,183,0.6); }
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa 0%, #ec4899 50%, #6366f1 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 3s ease infinite;
        text-align: center;
        margin-bottom: 0;
        filter: drop-shadow(0 0 30px rgba(167,139,250,0.5));
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255,255,255,0.7);
        text-align: center;
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1.5rem 0;
        animation: fadeIn 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(167,139,250,0.3);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(167,139,250,0.2) 0%, rgba(236,72,153,0.2) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        animation: fadeIn 0.8s ease-out;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        height: 3.5em;
        font-size: 1.2em;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: glow 2s infinite;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 50px rgba(103,58,183,0.8);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 14, 39, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #a78bfa;
        font-weight: 700;
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* Tables */
    .stTable {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
        border-radius: 8px;
    }
    
    /* Warning/Success boxes */
    .stAlert {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
    }
    
    /* Gap warning card */
    .gap-card {
        background: rgba(239,68,68,0.1);
        border: 2px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 2rem;
        animation: fadeIn 1s ease-out;
        box-shadow: 0 0 30px rgba(239,68,68,0.2);
    }
    
    /* Timeline roadmap */
    .roadmap-item {
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #a78bfa;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        animation: fadeIn 1.2s ease-out;
    }
    
    /* JSON display */
    pre {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Mock data functions
def analyze_github(username):
    return {"languages": ["Python", "JavaScript", "TypeScript"], "projects": 12, "commits": 347, "stars": 89}

def parse_resume(file):
    return {"skills": ["React", "Python", "SQL", "Docker"], "experience": "2 years", "education": "B.Tech CS"}

def get_role_skills(role):
    skills_db = {
        'Software Engineer': ['Python', 'Java', 'Git', 'Docker', 'Kubernetes', 'APIs', 'System Design'],
        'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'TensorFlow', 'Visualization'],
        'Fullstack Developer': ['React', 'Node.js', 'MongoDB', 'REST APIs', 'CSS', 'TypeScript', 'GraphQL']
    }
    return skills_db.get(role, [])

# Hero Section
st.markdown('<h1 class="hero-title">Personal Career Navigator 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">An AI career co-pilot that reasons, plans, and evolves with you.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("<br>", unsafe_allow_html=True)
    
    github_username = st.text_input("🔗 GitHub Username", placeholder="yourusername")
    resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=['pdf'])
    dream_role = st.selectbox("💼 Dream Role", ['Software Engineer', 'Data Scientist', 'Fullstack Developer'])
    hours_per_day = st.slider("⏰ Hours/Day", 1, 4, 2)
    level = st.selectbox("📊 Current Level", ['Beginner', 'Intermediate', 'Advanced'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🎯 ANALYZE CAREER")

# Main Content
if analyze_button:
    if not github_username:
        st.error("⚠️ Please enter your GitHub username to continue")
    else:
        with st.spinner("🔮 AI is analyzing your career trajectory..."):
            time.sleep(2.5)
        
        st.success("✨ Analysis Complete! Your personalized roadmap is ready.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Metrics Row
        github_data = analyze_github(github_username)
        resume_data = parse_resume(resume_file) if resume_file else {"skills": ["Git", "Python", "React"], "experience": "1 year"}
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(resume_data["skills"])}</div><div class="metric-label">Skills</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{github_data["projects"]}</div><div class="metric-label">Projects</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{github_data["commits"]}</div><div class="metric-label">Commits</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{github_data["stars"]}</div><div class="metric-label">Stars</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Profile Analysis Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Profile Analysis")
        profile_data = {
            "github_insights": github_data,
            "resume_summary": resume_data,
            "skill_level": level,
            "learning_capacity": f"{hours_per_day} hours/day"
        }
        st.json(profile_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Role Skills Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💼 Dream Role Requirements")
        role_skills = get_role_skills(dream_role)
        st.table({"Required Skills": role_skills, "Priority": ["High"] * len(role_skills)})
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Skill Gaps Card
        user_skills = set(resume_data["skills"])
        required_skills = set(role_skills)
        gaps = list(required_skills - user_skills)
        
        if gaps:
            st.markdown('<div class="gap-card">', unsafe_allow_html=True)
            st.markdown(f"### ⚠️ Skill Gaps Identified: {len(gaps)}")
            st.table({"Missing Skill": gaps, "Impact": ["Critical"] * len(gaps), "Est. Time": [f"{hours_per_day*3}hrs"] * len(gaps)})
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🎉 No Critical Gaps!")
            st.write("You're ready to apply for this role!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Roadmap Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🗺️ 7-Day Personalized Roadmap")
        
        for i, skill in enumerate(gaps[:7] if gaps else ["Advanced Topics"]):
            day_name = (datetime.now() + timedelta(days=i+1)).strftime("%A")
            st.markdown(f'''
            <div class="roadmap-item">
                <strong>Day {i+1} • {day_name}</strong><br>
                🎯 Master {skill}<br>
                ⏱️ {hours_per_day} hours • {level} level content
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.balloons()

else:
    # Welcome State
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🌟 Welcome to Your Career Journey")
    st.write("Fill in your details in the control panel and click **ANALYZE CAREER** to unlock your personalized roadmap.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="glass-card" style="text-align: center;">🎯<br><strong>AI Analysis</strong><br>Deep GitHub & resume insights</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card" style="text-align: center;">💼<br><strong>Role Matching</strong><br>Compare with dream jobs</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass-card" style="text-align: center;">🗺️<br><strong>Smart Roadmap</strong><br>Personalized learning path</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.4); font-size: 0.9rem;">Built with ❤️ for Bengaluru CS Hackathon 2026 | Powered by AI</p>', unsafe_allow_html=True)