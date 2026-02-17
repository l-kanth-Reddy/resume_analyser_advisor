# utils/resume_parser.py

import os
import re
import docx2txt
from PyPDF2 import PdfReader

# Sample skill set to compare with resume
COMMON_SKILLS = [
    'python', 'flask', 'html', 'css', 'javascript', 'react', 'sql',
    'pandas', 'numpy', 'machine learning', 'java', 'c++'
]

def extract_text_from_resume(file_path):
    """Extracts raw text from PDF or DOCX resume file."""
    text = ""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        text = docx2txt.process(file_path)
    return text.lower()

def extract_skills(text):
    """Extract skills by matching known skills in resume text."""
    found_skills = []
    for skill in COMMON_SKILLS:
        if skill.lower() in text:
            found_skills.append(skill.lower())
    return list(set(found_skills))
