import pdfplumber


async def analyze_resume(file_path: str):

    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    skills = []

    skill_keywords = [
        "Python",
        "Java",
        "C++",
        "FastAPI",
        "MongoDB",
        "SQL",
        "Docker",
        "AWS",
        "React",
        "Git",
    ]

    for skill in skill_keywords:
        if skill.lower() in text.lower():
            skills.append(skill)

    score = min(100, len(skills) * 10)

    suggestions = []

    if "Docker" not in skills:
        suggestions.append("Add Docker skills")

    if "AWS" not in skills:
        suggestions.append("Add AWS skills")

    if "Git" not in skills:
        suggestions.append("Add Git/GitHub projects")

    return {
        "score": score,
        "skills": skills,
        "education": [],
        "experience": [],
        "suggestions": suggestions,
    }