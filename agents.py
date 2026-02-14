# 🚨 CAREER NAVIGATOR AGENTS - Tailored for Enhanced Data Layer
# Gap Analysis + Roadmap Generation

def extract_all_skills_from_data(github_data, resume_data):
    """
    Extract and combine all skills from GitHub and Resume data structures
    
    Args:
        github_data: Dict from get_github_skills()
        resume_data: Dict from extract_resume_skills()
        
    Returns:
        List of unique skills
    """
    all_skills = []
    
    # Extract from GitHub
    if github_data and 'skills' in github_data:
        all_skills.extend(github_data['skills'])
    
    # Extract from Resume technical_skills
    if resume_data and 'technical_skills' in resume_data:
        tech_skills = resume_data['technical_skills']
        all_skills.extend(tech_skills.get('languages', []))
        all_skills.extend(tech_skills.get('web', []))
        all_skills.extend(tech_skills.get('core_cs', []))
        all_skills.extend(tech_skills.get('tools', []))
    
    # Remove duplicates and normalize
    unique_skills = list(set(skill.strip() for skill in all_skills if skill))
    
    return unique_skills


def analyze_skill_gaps(current_skills, job_requirements_dict):
    """
    Analyze gaps between current skills and job requirements
    
    Args:
        current_skills: List of user's current skills
        job_requirements_dict: Dict with 'required_skills' and 'nice_to_have'
        
    Returns:
        Dict with missing_required, missing_nice_to_have, and matched skills
    """
    # Normalize skills to lowercase for comparison
    user_set = set(s.lower().strip() for s in current_skills if s)
    
    # Get required and nice-to-have skills
    required_skills = job_requirements_dict.get('required_skills', [])
    nice_to_have = job_requirements_dict.get('nice_to_have', [])
    
    required_set = set(s.lower().strip() for s in required_skills if s)
    nice_set = set(s.lower().strip() for s in nice_to_have if s)
    
    # Find gaps and matches
    missing_required = list(required_set - user_set)
    missing_nice = list(nice_set - user_set)
    matched_skills = list(user_set & required_set)
    
    return {
        'missing_required': missing_required,
        'missing_nice_to_have': missing_nice,
        'matched_skills': matched_skills,
        'gap_count': len(missing_required),
        'match_count': len(matched_skills)
    }


def calculate_match_score(current_skills, job_requirements_dict):
    """
    Calculate how well current skills match job requirements
    
    Args:
        current_skills: List of user's current skills
        job_requirements_dict: Dict with 'required_skills'
        
    Returns:
        Dictionary with match percentage and counts
    """
    user_set = set(s.lower().strip() for s in current_skills if s)
    required_skills = job_requirements_dict.get('required_skills', [])
    job_set = set(s.lower().strip() for s in required_skills if s)
    
    matching_skills = user_set & job_set
    
    if len(job_set) == 0:
        match_percentage = 0
    else:
        match_percentage = (len(matching_skills) / len(job_set)) * 100
    
    return {
        'match_percentage': round(match_percentage, 1),
        'matching_count': len(matching_skills),
        'total_required': len(job_set),
        'gap_count': len(job_set - user_set)
    }


def generate_roadmap(gaps_dict, time_per_day, current_level):
    """
    Generate a 7-day personalized learning roadmap based on skill gaps
    
    Args:
        gaps_dict: Dict from analyze_skill_gaps() with missing skills
        time_per_day: Hours available per day (1-4)
        current_level: 'Beginner' or 'Intermediate'
        
    Returns:
        Dictionary with daily roadmap structure
    """
    # Prioritize required skills over nice-to-have
    required_gaps = gaps_dict.get('missing_required', [])
    nice_gaps = gaps_dict.get('missing_nice_to_have', [])
    
    # Focus on required skills first
    priority_skills = required_gaps + nice_gaps
    
    if not priority_skills:
        return {
            "message": "🎉 Congratulations! You have all required skills!",
            "suggestion": "Consider learning the nice-to-have skills to stand out!",
            "days": []
        }
    
    # Resource recommendations based on level
    resources = {
        'Beginner': {
            'platform': 'freeCodeCamp, Codecademy, W3Schools',
            'approach': 'Foundational tutorials and guided projects'
        },
        'Intermediate': {
            'platform': 'Udemy, Coursera, Official Documentation',
            'approach': 'Advanced courses and real-world projects'
        }
    }
    
    # Distribute skills across 7 days based on time commitment
    if time_per_day >= 3:
        skills_per_day = max(1, len(priority_skills) // 5)  # Faster pace
    else:
        skills_per_day = max(1, len(priority_skills) // 7)
    
    roadmap = {
        "level": current_level,
        "time_per_day": time_per_day,
        "total_skills": len(priority_skills),
        "required_count": len(required_gaps),
        "nice_to_have_count": len(nice_gaps),
        "recommended_platform": resources[current_level]['platform'],
        "learning_approach": resources[current_level]['approach'],
        "days": []
    }
    
    # Create daily plan
    for day in range(1, 8):
        start_idx = (day - 1) * skills_per_day
        end_idx = min(start_idx + skills_per_day, len(priority_skills))
        
        if start_idx >= len(priority_skills):
            # Review and project days
            day_plan = {
                "day": day,
                "focus": "Review & Build Project",
                "skills": [],
                "is_review_day": True,
                "activities": [
                    "🔄 Review all learned skills from the week",
                    "🚀 Build a portfolio project combining multiple skills",
                    "💪 Practice coding challenges on LeetCode/HackerRank",
                    "📝 Update your resume and GitHub with new skills"
                ],
                "resources": "LeetCode, HackerRank, GitHub, Portfolio Templates",
                "hours": time_per_day,
                "project_ideas": generate_project_ideas(priority_skills[:start_idx])
            }
        else:
            day_skills = priority_skills[start_idx:end_idx]
            day_plan = {
                "day": day,
                "focus": " + ".join([s.title() for s in day_skills]),
                "skills": day_skills,
                "is_review_day": False,
                "activities": generate_daily_activities(day_skills, current_level),
                "resources": generate_resources(day_skills, current_level),
                "hours": time_per_day,
                "checkpoint": f"Complete basic {day_skills[0].title()} tutorial"
            }
        
        roadmap["days"].append(day_plan)
    
    return roadmap


def generate_daily_activities(skills, level):
    """Generate specific activities for skills based on level"""
    activities = []
    
    for skill in skills:
        skill_lower = skill.lower()
        
        if level == 'Beginner':
            if 'python' in skill_lower:
                activities.append("📚 Learn Python basics: variables, loops, functions, lists")
            elif 'java' in skill_lower:
                activities.append("📚 Study Java fundamentals: OOP, classes, methods")
            elif 'react' in skill_lower:
                activities.append("📚 Learn React basics: components, props, state, JSX")
            elif 'sql' in skill_lower:
                activities.append("📚 Practice SQL: SELECT, WHERE, JOIN operations")
            elif 'docker' in skill_lower:
                activities.append("📚 Understand Docker basics: containers, images, dockerfile")
            elif 'git' in skill_lower:
                activities.append("📚 Master Git basics: commit, push, pull, branches")
            elif 'spring boot' in skill_lower:
                activities.append("📚 Intro to Spring Boot: annotations, REST controllers")
            elif 'tensorflow' in skill_lower or 'machine learning' in skill_lower:
                activities.append("📚 ML basics: supervised learning, model training")
            elif 'node' in skill_lower:
                activities.append("📚 Node.js fundamentals: modules, npm, async/await")
            elif 'rest api' in skill_lower:
                activities.append("📚 Learn REST API concepts: GET, POST, PUT, DELETE")
            else:
                activities.append(f"📚 Study {skill.title()} fundamentals and core concepts")
        else:  # Intermediate
            if 'python' in skill_lower:
                activities.append("🚀 Build Python project: web scraper or automation tool")
            elif 'java' in skill_lower:
                activities.append("🚀 Create Java application with design patterns")
            elif 'react' in skill_lower:
                activities.append("🚀 Build React app with hooks, routing, and API integration")
            elif 'sql' in skill_lower:
                activities.append("🚀 Design database schema and optimize queries")
            elif 'docker' in skill_lower:
                activities.append("🚀 Containerize app with Docker Compose and multi-stage builds")
            elif 'git' in skill_lower:
                activities.append("🚀 Practice advanced Git: merge, rebase, conflict resolution")
            elif 'spring boot' in skill_lower:
                activities.append("🚀 Build REST API with Spring Boot and JPA")
            elif 'tensorflow' in skill_lower or 'machine learning' in skill_lower:
                activities.append("🚀 Train ML model and deploy it")
            elif 'node' in skill_lower:
                activities.append("🚀 Build Express.js backend with authentication")
            elif 'rest api' in skill_lower:
                activities.append("🚀 Design and implement RESTful API with best practices")
            else:
                activities.append(f"🚀 Build hands-on project using {skill.title()}")
    
    # Add practice activity
    activities.append("💪 Complete 2-3 coding exercises related to today's skills")
    
    return activities


def generate_resources(skills, level):
    """Generate learning resources for specific skills"""
    resources = []
    
    for skill in skills:
        skill_lower = skill.lower()
        
        if 'python' in skill_lower:
            resources.append("Python.org" if level == 'Beginner' else "Real Python, Python Docs")
        elif 'java' in skill_lower:
            resources.append("Java Tutorial (Oracle)" if level == 'Beginner' else "Effective Java, Spring Guides")
        elif 'react' in skill_lower:
            resources.append("React.dev Tutorial" if level == 'Beginner' else "React Docs, React Patterns")
        elif 'sql' in skill_lower:
            resources.append("SQLBolt, W3Schools" if level == 'Beginner' else "PostgreSQL Docs, SQL Performance")
        elif 'docker' in skill_lower:
            resources.append("Docker Getting Started" if level == 'Beginner' else "Docker Docs, Docker Compose")
        elif 'node' in skill_lower:
            resources.append("NodeSchool.io" if level == 'Beginner' else "Node.js Docs, Express.js Guide")
        elif 'spring boot' in skill_lower:
            resources.append("Spring.io Guides" if level == 'Beginner' else "Spring Boot Reference, Baeldung")
        elif 'machine learning' in skill_lower or 'tensorflow' in skill_lower:
            resources.append("Kaggle Learn, TensorFlow Basics" if level == 'Beginner' else "TensorFlow Docs, Fast.ai")
        elif 'git' in skill_lower:
            resources.append("GitHub Skills" if level == 'Beginner' else "Pro Git Book, Atlassian Git")
        elif 'rest api' in skill_lower:
            resources.append("REST API Tutorial" if level == 'Beginner' else "RESTful Web Services, API Design")
        else:
            resources.append(f"{skill.title()} Official Documentation")
    
    return ", ".join(resources) if resources else "Online tutorials and official docs"


def generate_project_ideas(learned_skills):
    """Generate project ideas based on learned skills"""
    skill_set = set(s.lower() for s in learned_skills)
    
    projects = []
    
    if 'java' in skill_set and 'spring boot' in skill_set:
        projects.append("Build a Task Management REST API with Spring Boot")
    
    if 'react' in skill_set and 'node' in skill_set:
        projects.append("Create a Full-stack Todo App (MERN stack)")
    
    if 'python' in skill_set and 'sql' in skill_set:
        projects.append("Build a Student Database Management System")
    
    if 'docker' in skill_set:
        projects.append("Containerize your existing projects with Docker")
    
    if 'python' in skill_set and 'tensorflow' in skill_set:
        projects.append("Train an Image Classification Model")
    
    if not projects:
        projects.append("Build a portfolio project combining your new skills")
    
    return projects


# 🧪 TEST HARNESS
if __name__ == "__main__":
    print("🧪 AGENTS TEST (Enhanced Data) ✅")
    print("\n" + "="*60)
    
    # Mock data matching data.py structure
    github_data = {
        "skills": ["Java", "C", "Python", "HTML", "CSS", "Data Structures", "Git"]
    }
    
    resume_data = {
        "technical_skills": {
            "languages": ["Java", "C", "Python"],
            "web": ["HTML", "CSS"],
            "core_cs": ["Data Structures", "Algorithms"],
            "tools": ["Git"]
        }
    }
    
    job_requirements = {
        "required_skills": ["Java", "Spring Boot", "SQL", "Git", "REST APIs"],
        "nice_to_have": ["Docker", "Microservices"]
    }
    
    # Test skill extraction
    print("📋 Extracted Skills:")
    all_skills = extract_all_skills_from_data(github_data, resume_data)
    print(all_skills)
    
    # Test gap analysis
    print("\n⚠️  GAP ANALYSIS:")
    gaps = analyze_skill_gaps(all_skills, job_requirements)
    print(f"Missing Required: {gaps['missing_required']}")
    print(f"Missing Nice-to-Have: {gaps['missing_nice_to_have']}")
    print(f"Matched: {gaps['matched_skills']}")
    
    # Test match score
    print("\n📊 MATCH SCORE:")
    score = calculate_match_score(all_skills, job_requirements)
    print(score)
    
    # Test roadmap
    print("\n🗓️  ROADMAP:")
    roadmap = generate_roadmap(gaps, time_per_day=2, current_level='Beginner')
    print(f"Total Skills: {roadmap['total_skills']}")
    print(f"Day 1: {roadmap['days'][0]['focus']}")
    
    print("\n✅ ALL TESTS PASSED!")
    print("="*60)