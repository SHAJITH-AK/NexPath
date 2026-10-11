"""
Generates data/career_config.json  (career -> relevant skills -> target score).

How the targets are chosen (no invented numbers):
  * For every career class in career_skill_prediction_250.csv we compute the
    average score of each skill for students labelled with that career.
  * The 6 skills whose class average is furthest ABOVE the all-student average
    (and whose class average is at least 6/10) are the "relevant skills".
  * Target score = that class average rounded to the nearest whole number.

The result is written once and can then be EDITED BY HAND (descriptions, targets,
skills, job page).  Re-running this script overwrites your edits, so it refuses to
run if the file already exists unless you pass --force.
"""
import json, sys
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "career_skill_prediction_250.csv"
OUT = BASE / "data" / "career_config.json"

DESCRIPTIONS = {
 "Backend Developer": "Builds the server-side logic, APIs and databases that power web and mobile applications.",
 "Cloud Engineer": "Designs, deploys and maintains applications and infrastructure on cloud platforms such as AWS or Google Cloud.",
 "Computer Vision Engineer": "Builds systems that understand images and video, for example face detection, object recognition and medical imaging.",
 "Cyber Security Engineer": "Protects systems, networks and data by finding vulnerabilities, monitoring threats and responding to incidents.",
 "Data Analyst": "Collects, cleans and analyses data to find patterns, then presents insights through reports and dashboards that help businesses decide.",
 "Data Engineer": "Builds and maintains the data pipelines and storage systems that make clean, reliable data available to analysts and data scientists.",
 "Data Scientist": "Uses statistics and machine learning to build models that explain data and predict outcomes.",
 "Database Engineer": "Designs, optimises and secures databases, and makes sure data is stored reliably and can be queried quickly.",
 "DevOps Engineer": "Connects development and operations by automating builds, deployments and infrastructure so software ships reliably.",
 "Frontend Developer": "Builds the visual, interactive part of websites and web apps that users see and use in the browser.",
 "Full Stack Developer": "Works on both the user interface and the server side of an application, from the database to the browser.",
 "Generative AI Engineer": "Builds applications on top of large language models and other generative AI systems.",
 "ML Specialist": "Trains, evaluates and deploys machine learning models to solve practical prediction and classification problems.",
 "NLP Engineer": "Builds systems that understand and generate human language, such as chatbots, search and text analysis tools.",
 "Network Engineer": "Plans, configures and troubleshoots computer networks so that systems can communicate securely and reliably.",
 "Software Engineer": "Designs, writes, tests and maintains software, applying core programming, problem solving and system design skills.",
 "UI UX Designer": "Designs how digital products look and feel, using user research, wireframes and prototypes to make them easy to use.",
}
JOB_PAGES = {
 "Backend Developer": "backend-developer", "Cloud Engineer": "cloud-engineer",
 "Computer Vision Engineer": "computer-vision-engineer", "Cyber Security Engineer": "cyber-security-engineer",
 "Data Analyst": "data-analyst", "Data Engineer": "data-engineer", "Data Scientist": "data-scientist",
 "Database Engineer": "database-engineer", "DevOps Engineer": "devops-engineer",
 "Frontend Developer": "frontend-developer", "Full Stack Developer": "full-stack-developer",
 "Generative AI Engineer": "generative-ai-engineer", "ML Specialist": "Ml_Specialists",
 "NLP Engineer": "nlp-engineer", "Network Engineer": "network-engineer",
 "Software Engineer": "software-engineer", "UI UX Designer": "ui-ux-designer",
}
# Order in which skills appear on a learning roadmap (foundations first).
SKILL_ORDER = ["Communication", "Problem Solving", "Python", "Java", "C++", "Git", "Linux", "Networking",
 "HTML", "CSS", "JavaScript", "React", "SQL", "MongoDB", "Statistics", "Data Analysis", "Machine Learning",
 "Deep Learning", "Computer Vision", "NLP", "Cloud Computing", "Cyber Security", "UI UX Design", "Figma", "System Design"]
# skill -> course key (matches data-name in courses.html). closest=True means "nearest match, not a dedicated course".
SKILL_COURSES = {
 "Python": ("python programming", "Python Programming", False),
 "Java": ("java programming", "Java Programming", False),
 "C++": ("c++ programming", "C++ Programming", False),
 "HTML": ("html css responsive web design", "Responsive Web Design", False),
 "CSS": ("html css responsive web design", "Responsive Web Design", False),
 "JavaScript": ("javascript", "JavaScript", False),
 "React": ("full stack development", "Full-Stack Web Development", True),
 "SQL": ("sql relational database", "SQL & Relational Databases", False),
 "MongoDB": ("mongodb database", "MongoDB Fundamentals", False),
 "Git": ("git github version control", "Git & GitHub", False),
 "Linux": ("devops docker kubernetes", "DevOps & Containers", True),
 "Networking": ("ethical hacking", "Ethical Hacking Foundations", True),
 "Cyber Security": ("cybersecurity", "Cybersecurity Fundamentals", False),
 "Cloud Computing": ("aws cloud", "AWS Cloud Foundations", False),
 "Machine Learning": ("machine learning", "Machine Learning", False),
 "Deep Learning": ("machine learning", "Machine Learning", True),
 "Data Analysis": ("data analysis pandas python", "Data Analysis with Python", False),
 "Statistics": ("data analysis pandas python", "Data Analysis with Python", True),
 "UI UX Design": ("ui ux design", "UI/UX Design", False),
 "Figma": ("ui ux design", "UI/UX Design", False),
 "Computer Vision": ("machine learning", "Machine Learning", True),
 "NLP": ("generative ai artificial intelligence", "Generative AI Fundamentals", True),
 "System Design": ("full stack development", "Full-Stack Web Development", True),
}
SKILL_LINKS = {  # skills with no course on the Courses page: practise with NexPath's Aptitude Test instead
 "Communication": ("aptitude.php", "Verbal Ability practice (NexPath Aptitude Test)"),
 "Problem Solving": ("aptitude.php", "Logical Reasoning practice (NexPath Aptitude Test)"),
}

def main():
    if OUT.exists() and "--force" not in sys.argv:
        print(f"{OUT} already exists (it may contain your manual edits). Use --force to overwrite.")
        return
    df = pd.read_csv(CSV)
    X = df.drop(columns="Role")
    overall = X.mean()
    careers = {}
    for role, grp in df.groupby("Role"):
        means = grp.drop(columns="Role").mean()
        lift = (means - overall).sort_values(ascending=False)
        chosen = [s for s in lift.index if means[s] >= 6][:6]
        chosen.sort(key=SKILL_ORDER.index)
        careers[role] = {
            "description": DESCRIPTIONS[role],
            "job_page": f"Jobs/{JOB_PAGES[role]}.html",
            "skills": {s: int(min(10, max(1, round(means[s])))) for s in chosen},
        }
    config = {
        "_about": "Editable career -> skill targets. 'skills' = relevant skills with a target score out of 10. "
                  "Targets were first generated from the dataset's per-career averages (python/generate_career_config.py); edit freely.",
        "strong_margin": 1,   # a skill counts as "Strong" when score >= target - strong_margin
        "skill_order": SKILL_ORDER,
        "skill_courses": {k: {"course": v[0], "title": v[1], "closest": v[2]} for k, v in SKILL_COURSES.items()},
        "skill_links": {k: {"link": v[0], "title": v[1]} for k, v in SKILL_LINKS.items()},
        "careers": careers,
    }
    OUT.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
