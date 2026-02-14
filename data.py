# 🚀 PERSON B: Career Navigator - Enhanced Data Layer
# Profile: B.Tech CSE (AI & ML), Bengaluru

import pandas as pd

# -------------------------------
# 📦 GitHub Profile Extractor
# -------------------------------

def get_github_skills(github_user):
    """Mock GitHub extraction - Hackathon MVP"""
    
    print(f"🔍 Analyzing GitHub: {github_user}")
    
    return {
        "username": github_user,
        "repos_count": 8,
        "experience_level": "beginner-intermediate",
        "top_languages": {
            "Java": "35%",
            "C": "25%",
            "Python": "20%",
            "JavaScript": "20%"
        },
        "skills": [
            "Java",
            "C",
            "Python",
            "HTML",
            "CSS",
            "Data Structures",
            "Git",
            "Algorithms"
        ],
        "activity_level": "consistent"
    }


# -------------------------------
# 📄 Resume Parser (Structured)
# -------------------------------

def extract_resume_skills(resume_text_or_path):
    """Mock Resume Parsing - Structured Output"""
    
    print("📄 Parsing resume...")
    
    return {
        "name": "CS Student",
        "education": {
            "degree": "B.Tech Computer Science (AI & ML)",
            "institution": "Bengaluru Engineering College",
            "year": "1st Year",
            "cgpa": 8.2
        },
        "technical_skills": {
            "languages": ["Java", "C", "Python"],
            "web": ["HTML", "CSS", "Basic JavaScript"],
            "core_cs": ["Data Structures", "Algorithms", "DBMS", "Operating Systems"],
            "tools": ["Git", "VS Code"]
        },
        "projects": [
            {
                "title": "Page Replacement Algorithm Simulator",
                "tech": ["Python"],
                "type": "Operating Systems Mini Project"
            },
            {
                "title": "Boutique Management DBMS System",
                "tech": ["SQL", "ER Diagram", "Oracle/MySQL"],
                "type": "Database Mini Project"
            },
            {
                "title": "Career Navigator Hackathon Prototype",
                "tech": ["Python", "Streamlit"],
                "type": "Hackathon Project"
            }
        ],
        "interests": [
            "AI/ML",
            "Backend Development",
            "Problem Solving",
            "Hackathons"
        ],
        "strengths": [
            "Quick Learner",
            "Strong Logical Thinking",
            "Team Collaboration"
        ]
    }


# -------------------------------
# 📊 Job Requirements Loader
# -------------------------------

def load_job_requirements(role=None):
    """Load job requirements - returns dict or filters by role"""
    
    job_data = {
        "Software Engineer": {
            "required_skills": ["Java", "Python", "React", "Docker", "SQL", "Git", "REST APIs", "Data Structures", "Algorithms", "Communication"],
            "nice_to_have": ["Spring Boot", "Microservices", "AWS", "CI/CD"],
            "experience": "0-2 years"
        },
        "Data Scientist": {
            "required_skills": ["Python", "Pandas", "NumPy", "Machine Learning", "SQL", "Statistics", "Data Visualization", "Jupyter", "TensorFlow", "Communication"],
            "nice_to_have": ["Deep Learning", "NLP", "Big Data", "Spark"],
            "experience": "0-2 years"
        },
        "Fullstack Developer": {
            "required_skills": ["React", "Node.js", "JavaScript", "MongoDB", "Express.js", "Git", "REST APIs", "HTML", "CSS", "Docker"],
            "nice_to_have": ["TypeScript", "GraphQL", "AWS", "Next.js"],
            "experience": "0-2 years"
        },
        "Backend Developer": {
            "required_skills": ["Java", "Spring Boot", "SQL", "Git", "Data Structures", "REST APIs", "Microservices"],
            "nice_to_have": ["Docker", "Kubernetes", "Redis", "PostgreSQL"],
            "experience": "0-2 years"
        },
        "AI Engineer": {
            "required_skills": ["Python", "TensorFlow", "Statistics", "Machine Learning", "Deep Learning", "PyTorch", "NumPy"],
            "nice_to_have": ["MLOps", "Computer Vision", "NLP", "Model Deployment"],
            "experience": "0-2 years"
        }
    }
    
    if role:
        return job_data.get(role, job_data["Software Engineer"])
    return job_data


# -------------------------------
# 🧪 TEST HARNESS
# -------------------------------

if __name__ == "__main__":
    
    print("🧪 PERSON B: ENHANCED DATA TEST\n")
    
    github_data = get_github_skills("your-github-username")
    print("\n📊 GitHub Data:")
    print(github_data)
    
    resume_data = extract_resume_skills("resume.pdf")
    print("\n📄 Resume Data:")
    print(resume_data)
    
    print("\n📋 Job Requirements:")
    jobs = load_job_requirements()
    for role, details in jobs.items():
        print(f"\n{role}:")
        print(f"  Required: {details['required_skills'][:3]}...")
    
    print("\n🎉 DATA MODULE READY FOR AGENTS!")
    print("=" * 60)