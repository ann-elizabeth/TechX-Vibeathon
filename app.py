import streamlit as st
import pandas as pd
from data import extract_resume_skills, get_github_skills, load_job_requirements
from agents import (
    extract_all_skills_from_data, 
    analyze_skill_gaps, 
    generate_roadmap, 
    calculate_match_score
)

# Page config
st.set_page_config(
    page_title="Personal Career Navigator",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if 'roadmap_generated' not in st.session_state:
    st.session_state.roadmap_generated = False
if 'github_data' not in st.session_state:
    st.session_state.github_data = None
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'current_skills' not in st.session_state:
    st.session_state.current_skills = []
if 'gaps' not in st.session_state:
    st.session_state.gaps = {}
if 'roadmap' not in st.session_state:
    st.session_state.roadmap = {}
if 'match_score' not in st.session_state:
    st.session_state.match_score = {}

# Title
st.title("🚀 Personal Career Navigator")
st.markdown("*AI-powered career development roadmap generator*")

# Sidebar inputs
with st.sidebar:
    st.header("📋 Your Profile")
    
    # GitHub username
    github_username = st.text_input(
        "GitHub Username",
        placeholder="e.g., octocat",
        help="We'll analyze your repositories and contributions"
    )
    
    # Resume upload
    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=['pdf'],
        help="Upload your resume for skill extraction"
    )
    
    # Dream role
    dream_role = st.selectbox(
        "Dream Role",
        options=['Software Engineer', 'Data Scientist', 'Fullstack Developer', 'Backend Developer', 'AI Engineer'],
        help="Select your target career role"
    )
    
    # Time commitment
    time_per_day = st.slider(
        "Learning Time per Day (hours)",
        min_value=1,
        max_value=4,
        value=2,
        help="How much time can you dedicate daily?"
    )
    
    # Current level
    current_level = st.selectbox(
        "Current Level",
        options=['Beginner', 'Intermediate'],
        help="Select your current skill level"
    )
    
    st.divider()
    
    # Generate button
    generate_btn = st.button("🎯 Generate Roadmap", type="primary", use_container_width=True)

# Main content area
if generate_btn:
    if not github_username and not resume_file:
        st.warning("⚠️ Please provide at least GitHub username or resume to continue.")
    else:
        with st.spinner("🔍 Analyzing your profile..."):
            # 1️⃣ Extract data from GitHub and Resume
            github_data = get_github_skills(github_username) if github_username else None
            resume_data = extract_resume_skills(resume_file) if resume_file else None
            
            # 2️⃣ Extract all skills
            current_skills = extract_all_skills_from_data(github_data, resume_data)
            
            # 3️⃣ Load job requirements
            job_requirements = load_job_requirements(dream_role)
            
            # 4️⃣ Find gaps
            gaps = analyze_skill_gaps(current_skills, job_requirements)
            
            # 5️⃣ Calculate match score
            match_score = calculate_match_score(current_skills, job_requirements)
            
            # 6️⃣ Generate roadmap
            roadmap = generate_roadmap(gaps, time_per_day, current_level)
            
            # Store in session state
            st.session_state.roadmap_generated = True
            st.session_state.github_data = github_data
            st.session_state.resume_data = resume_data
            st.session_state.current_skills = current_skills
            st.session_state.gaps = gaps
            st.session_state.roadmap = roadmap
            st.session_state.match_score = match_score
            st.session_state.job_requirements = job_requirements
            
            st.success("✅ Analysis complete!")

# Section 1: Extracted Skills
st.header("📊 Extracted Skills")
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("From GitHub")
        if st.session_state.roadmap_generated and st.session_state.github_data:
            github_data = st.session_state.github_data
            
            # Show username and stats
            st.markdown(f"**Username:** {github_data.get('username', 'N/A')}")
            st.markdown(f"**Repos:** {github_data.get('repos_count', 0)} | **Level:** {github_data.get('experience_level', 'N/A')}")
            
            # Show top languages
            if 'top_languages' in github_data:
                st.markdown("**Top Languages:**")
                for lang, percent in github_data['top_languages'].items():
                    st.markdown(f"• {lang}: {percent}")
            
            # Show skills
            st.markdown("**Skills Detected:**")
            for skill in github_data.get('skills', []):
                st.markdown(f"✅ {skill}")
        else:
            st.info("Enter GitHub username to see skills extracted from your repositories")
        
    with col2:
        st.subheader("From Resume")
        if st.session_state.roadmap_generated and st.session_state.resume_data:
            resume_data = st.session_state.resume_data
            
            # Show education
            if 'education' in resume_data:
                edu = resume_data['education']
                st.markdown(f"**{edu.get('degree', 'N/A')}**")
                st.markdown(f"*{edu.get('institution', 'N/A')}*")
                st.markdown(f"CGPA: {edu.get('cgpa', 'N/A')}")
            
            # Show technical skills
            if 'technical_skills' in resume_data:
                tech = resume_data['technical_skills']
                st.markdown("**Technical Skills:**")
                
                if tech.get('languages'):
                    st.markdown(f"• Languages: {', '.join(tech['languages'])}")
                if tech.get('web'):
                    st.markdown(f"• Web: {', '.join(tech['web'])}")
                if tech.get('core_cs'):
                    st.markdown(f"• Core CS: {', '.join(tech['core_cs'])}")
                if tech.get('tools'):
                    st.markdown(f"• Tools: {', '.join(tech['tools'])}")
        else:
            st.info("Upload resume to see extracted skills")

st.divider()

# Section 2: Skill Gaps
st.header("🎯 Skill Gaps Analysis")
with st.container():
    st.info(f"Analyzing gaps for: **{dream_role}**")
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.roadmap_generated:
            st.metric(
                "Skills to Learn", 
                st.session_state.match_score['gap_count'],
                help="Required skills you need to learn"
            )
        else:
            st.metric("Skills to Learn", "-", help="Required skills you need to learn")
    
    with col2:
        if st.session_state.roadmap_generated:
            st.metric(
                "Skills Matched", 
                st.session_state.match_score['matching_count'],
                help="Skills you already have"
            )
        else:
            st.metric("Skills Matched", "-", help="Skills you already have")
    
    with col3:
        if st.session_state.roadmap_generated:
            st.metric(
                "Match Score", 
                f"{st.session_state.match_score['match_percentage']}%",
                help="Current fit percentage for target role"
            )
        else:
            st.metric("Match Score", "-", help="Current fit percentage for target role")

# Display skill gaps in detail
if st.session_state.roadmap_generated:
    gaps = st.session_state.gaps
    
    col1, col2 = st.columns(2)
    
    with col1:
        if gaps.get('missing_required'):
            st.subheader("🔴 Missing Required Skills")
            for skill in gaps['missing_required']:
                st.markdown(f"• **{skill.title()}**")
        
    with col2:
        if gaps.get('missing_nice_to_have'):
            st.subheader("🟡 Missing Nice-to-Have")
            for skill in gaps['missing_nice_to_have']:
                st.markdown(f"• {skill.title()}")

st.divider()

# Section 3: 7-Day Roadmap
st.header("🗓️ Your 7-Day Learning Roadmap")
with st.container():
    st.info(f"Personalized for **{current_level}** level • **{time_per_day}h/day** commitment")
    
    if st.session_state.roadmap_generated:
        roadmap = st.session_state.roadmap
        
        # Check if there's a completion message
        if roadmap.get('message'):
            st.success(roadmap['message'])
            if roadmap.get('suggestion'):
                st.info(roadmap['suggestion'])
        
        # Display roadmap summary
        if roadmap.get('days'):
            st.markdown(f"""
            **📋 Learning Plan Summary:**
            - 📚 **Platform:** {roadmap['recommended_platform']}
            - 🎯 **Approach:** {roadmap['learning_approach']}
            - 📊 **Total Skills:** {roadmap['total_skills']} ({roadmap.get('required_count', 0)} required + {roadmap.get('nice_to_have_count', 0)} nice-to-have)
            - ⏰ **Daily Commitment:** {roadmap['time_per_day']} hours
            """)
            
            st.divider()
            
            # Display daily roadmap
            for day_plan in roadmap['days']:
                # Different styling for review days
                if day_plan.get('is_review_day'):
                    icon = "🔄"
                    expanded = False
                else:
                    icon = "📅"
                    expanded = (day_plan['day'] == 1)
                
                with st.expander(
                    f"{icon} **Day {day_plan['day']}: {day_plan['focus']}** ({day_plan['hours']}h)", 
                    expanded=expanded
                ):
                    # Show skills to focus on
                    if day_plan.get('skills'):
                        st.markdown("**🎯 Skills to Focus On:**")
                        for skill in day_plan['skills']:
                            st.markdown(f"- {skill.title()}")
                        st.markdown("")
                    
                    # Show activities
                    st.markdown("**📋 Activities:**")
                    for activity in day_plan['activities']:
                        st.markdown(f"{activity}")
                    st.markdown("")
                    
                    # Show resources
                    st.markdown(f"**📚 Resources:** {day_plan['resources']}")
                    
                    # Show checkpoint or project ideas
                    if day_plan.get('checkpoint'):
                        st.markdown(f"**✅ Checkpoint:** {day_plan['checkpoint']}")
                    
                    if day_plan.get('project_ideas'):
                        st.markdown("**💡 Project Ideas:**")
                        for project in day_plan['project_ideas']:
                            st.markdown(f"- {project}")
    else:
        st.markdown("""
        *Your personalized roadmap will appear here once you generate it.*
        
        The roadmap will include:
        - ✅ Daily learning objectives tailored to your level
        - 📚 Recommended resources and tutorials
        - 💪 Practice projects and coding exercises
        - 🎯 Skill checkpoints and milestones
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    Built with ❤️ for TechX Hackathon | Powered by AI
</div>
""", unsafe_allow_html=True)