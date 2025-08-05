import os

LANG_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".php": "PHP",
    ".rb": "Ruby",
    ".go": "Go",
    ".cpp": "C++",
    ".c": "C",
}

FRAMEWORK_KEYWORDS = {
    "fastapi": "FastAPI",
    "flask": "Flask",
    "express": "Express",
    "react": "React",
    "vue": "Vue.js",
    "django": "Django",
    "springboot": "Spring Boot",
    "laravel": "Laravel",
}


def detect_languages(path):
    extensions = set()

    for root, _, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in LANG_EXTENSIONS:
                extensions.add(LANG_EXTENSIONS[ext])

    return sorted(extensions)


def detect_frameworks(path):
    frameworks = set()

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                    for keyword, name in FRAMEWORK_KEYWORDS.items():
                        if keyword in content:
                            frameworks.add(name)
            except:
                pass

    return sorted(frameworks)


def generate_project_overview(path):
    langs = detect_languages(path)
    frameworks = detect_frameworks(path)

    # Basic purpose inference
    if "FastAPI" in frameworks or "Flask" in frameworks:
        purpose = "Provides a REST API with route handlers and utilities."
    elif "React" in frameworks:
        purpose = "Frontend application with component-based structure."
    else:
        purpose = "General-purpose codebase with script and function utilities."

    return f"""### Project Overview

**Language(s):** {", ".join(langs) if langs else "Unknown"}  
**Frameworks Detected:** {", ".join(frameworks) if frameworks else "None"}  
**Purpose:** {purpose}
"""
