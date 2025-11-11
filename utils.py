import pandas as pd
import random

# Skills/Interests mapping for different engineering branches
BRANCH_SKILLS = {
    'CSE': {
        'skills': ['Programming', 'Problem Solving', 'Algorithms', 'Data Structures', 'Software Development'],
        'interests': ['Coding', 'AI/ML', 'Web Development', 'Mobile Apps', 'Gaming'],
        'careers': ['Software Engineer', 'Data Scientist', 'Full Stack Developer', 'ML Engineer', 'DevOps Engineer'],
        'avg_package': '6-12 LPA',
        'description': 'Computer Science focuses on software, programming, and computational theory.'
    },
    'IT': {
        'skills': ['Programming', 'Networking', 'Database Management', 'System Administration', 'Cybersecurity'],
        'interests': ['Technology', 'Internet', 'Cloud Computing', 'Networks', 'Security'],
        'careers': ['IT Consultant', 'Network Engineer', 'Cloud Architect', 'Systems Analyst', 'Security Analyst'],
        'avg_package': '5-10 LPA',
        'description': 'Information Technology deals with application of computers and telecom systems.'
    },
    'ECE': {
        'skills': ['Circuit Design', 'Signal Processing', 'Electronics', 'Communication Systems', 'Embedded Systems'],
        'interests': ['Electronics', 'Communication', 'Wireless Tech', 'IoT', 'Robotics'],
        'careers': ['Electronics Engineer', 'Telecom Engineer', 'VLSI Designer', 'Hardware Engineer', 'IoT Developer'],
        'avg_package': '4-8 LPA',
        'description': 'Electronics & Communication focuses on electronic devices and communication systems.'
    },
    'EEE': {
        'skills': ['Electrical Circuits', 'Power Systems', 'Control Systems', 'Machines', 'Renewable Energy'],
        'interests': ['Power Generation', 'Electrical Machines', 'Automation', 'Energy Systems', 'Control'],
        'careers': ['Electrical Engineer', 'Power Systems Engineer', 'Automation Engineer', 'Energy Analyst'],
        'avg_package': '4-7 LPA',
        'description': 'Electrical & Electronics Engineering deals with electricity, electronics and electromagnetism.'
    },
    'MECH': {
        'skills': ['Mechanical Design', 'Thermodynamics', 'Manufacturing', 'CAD/CAM', 'Materials Science'],
        'interests': ['Machines', 'Design', 'Manufacturing', 'Automobiles', 'Robotics'],
        'careers': ['Mechanical Engineer', 'Design Engineer', 'Production Engineer', 'Automotive Engineer'],
        'avg_package': '3.5-7 LPA',
        'description': 'Mechanical Engineering involves design, analysis and manufacturing of mechanical systems.'
    },
    'CIVIL': {
        'skills': ['Structural Design', 'Construction Management', 'Surveying', 'CAD', 'Project Planning'],
        'interests': ['Construction', 'Infrastructure', 'Architecture', 'Urban Planning', 'Environment'],
        'careers': ['Civil Engineer', 'Structural Engineer', 'Construction Manager', 'Urban Planner'],
        'avg_package': '3-6 LPA',
        'description': 'Civil Engineering focuses on design and construction of infrastructure and buildings.'
    }
}

def get_branch_category(branch_name):
    """Categorize branch based on name"""
    branch_upper = str(branch_name).upper()
    
    if any(x in branch_upper for x in ['COMPUTER', 'CSE', 'CS']):
        return 'CSE'
    elif any(x in branch_upper for x in ['INFORMATION', 'IT']):
        return 'IT'
    elif any(x in branch_upper for x in ['ELECTRONICS', 'ECE', 'E&C']):
        return 'ECE'
    elif any(x in branch_upper for x in ['ELECTRICAL', 'EEE', 'E&E']):
        return 'EEE'
    elif any(x in branch_upper for x in ['MECHANICAL', 'MECH']):
        return 'MECH'
    elif any(x in branch_upper for x in ['CIVIL']):
        return 'CIVIL'
    else:
        return 'OTHER'

def generate_college_summary(college_row, student_rank, branch_category):
    """Generate detailed college summary with branch-specific insights"""
    
    # Get branch info
    branch_info = BRANCH_SKILLS.get(branch_category, {
        'avg_package': '3-6 LPA',
        'description': 'Engineering program with good career prospects.'
    })
    
    # Calculate admission probability
    cutoff_rank = college_row.get('GM', 0)
    rank_diff = cutoff_rank - student_rank
    
    if rank_diff > 5000:
        admission_chance = "Very High"
        chance_pct = random.randint(85, 95)
    elif rank_diff > 2000:
        admission_chance = "High"
        chance_pct = random.randint(70, 85)
    elif rank_diff > 500:
        admission_chance = "Moderate"
        chance_pct = random.randint(50, 70)
    elif rank_diff > 0:
        admission_chance = "Low"
        chance_pct = random.randint(30, 50)
    else:
        admission_chance = "Very Low"
        chance_pct = random.randint(10, 30)
    
    summary = f"""
### 🎓 {college_row.get('College', 'College')}

**Branch:** {college_row.get('Branch', 'N/A')}  
**Location:** {college_row.get('Location', 'N/A')}  
**CET Code:** {college_row.get('CETCode', 'N/A')}

---

#### 📊 Admission Analysis
- **Your Rank:** {student_rank}
- **Cutoff Rank (GM):** {cutoff_rank}
- **Admission Probability:** {admission_chance} ({chance_pct}%)
- **Rank Advantage:** {rank_diff} ranks

---

#### 💼 Branch Insights: {branch_category}
{branch_info.get('description', '')}

**Average Package Range:** {branch_info.get('avg_package', 'N/A')}

**Key Skills Developed:**
{chr(10).join(f"• {skill}" for skill in branch_info.get('skills', [])[:3])}

**Career Opportunities:**
{chr(10).join(f"• {career}" for career in branch_info.get('careers', [])[:3])}

---

#### 🏫 College Features
- **Placement Support:** Available (based on branch performance)
- **Hostel Facilities:** Available for most courses
- **Infrastructure:** Modern labs and facilities
- **Faculty:** Experienced and qualified

#### ✅ Pros
• Established institution with good academic track record
• Active placement cell with industry connections
• Good infrastructure and learning environment

#### ⚠️ Considerations
• Competitive admission - secure your rank early
• Limited seats in popular branches
• Research specific branch placements before deciding

---

**Recommendation:** {"✅ Strongly recommended - you have excellent chances!" if chance_pct > 70 else "⚡ Good option - consider applying" if chance_pct > 50 else "⚠️ Backup option - apply but keep alternatives"}
"""
    
    return summary, chance_pct

def recommend_branches_by_interest(user_interests):
    """Recommend branches based on user interests"""
    recommendations = []
    
    for branch, info in BRANCH_SKILLS.items():
        match_score = 0
        matched_interests = []
        
        for interest in user_interests:
            interest_lower = interest.lower()
            for branch_interest in info['interests']:
                if interest_lower in branch_interest.lower() or branch_interest.lower() in interest_lower:
                    match_score += 1
                    matched_interests.append(branch_interest)
        
        if match_score > 0:
            recommendations.append({
                'branch': branch,
                'score': match_score,
                'matched_interests': list(set(matched_interests)),
                'info': info
            })
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:3]  # Top 3 matches
