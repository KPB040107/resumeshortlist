import re

import pdfplumber


SKILL_VOCAB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "react", "reactjs", "react.js", "angular", "vue", "node", "node.js", "nodejs",
    "express", "express.js", "django", "flask", "fastapi", "spring", "spring boot",
    "mongodb", "mysql", "postgresql", "postgres", "sql", "redis", "firebase",
    "html", "css", "tailwind", "bootstrap", "sass", "git", "github", "docker",
    "kubernetes", "aws", "azure", "gcp", "rest api", "rest apis", "graphql",
    "microservices", "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "tensorflow", "pytorch", "scikit-learn", "linux", "bash", "ci/cd", "jenkins",
    "agile", "scrum",
]

ALIASES = {
    "reactjs": "react",
    "react.js": "react",
    "node.js": "node",
    "nodejs": "node",
    "express.js": "express",
    "postgres": "postgresql",
    "rest apis": "rest api",
}


def _clean_text(raw_text: str) -> str:
    text = raw_text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_pdf_text(path: str) -> str:
    chunks = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                chunks.append(page.extract_text() or "")
    except Exception as error:
        print(f"[extractor] Could not read {path}: {error}")
        return ""
    return _clean_text("\n".join(chunks))


def extract_jd_text(jd_path: str) -> str:
    return _extract_pdf_text(jd_path)


def extract_resume_text(path: str) -> str:
    return _extract_pdf_text(path)


def extract_skills(text: str) -> list[str]:
    lower_text = text.lower()
    found = set()
    for skill in SKILL_VOCAB:
        pattern = rf"(?<![a-zA-Z0-9]){re.escape(skill)}(?![a-zA-Z0-9])"
        if re.search(pattern, lower_text):
            found.add(ALIASES.get(skill, skill))
    return sorted(found)
