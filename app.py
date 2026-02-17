# app.py

from flask import Flask, render_template, request
import os
import json
from utils.resume_parser import extract_text_from_resume, extract_skills

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load predefined job roles
with open('job_data.json') as f:
    job_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract text and skills
        resume_text = extract_text_from_resume(filepath)
        user_skills = extract_skills(resume_text)

        # Match jobs based on skills
        matched_jobs = []
        for job in job_data:
            match_count = len(set(job['skills']) & set(user_skills))
            if match_count > 0:
                job['match_percent'] = int((match_count / len(job['skills'])) * 100)
                matched_jobs.append(job)

        # Sort by best match
        matched_jobs = sorted(matched_jobs, key=lambda x: x['match_percent'], reverse=True)

        return render_template('results.html', jobs=matched_jobs, skills=user_skills)

    return "Please upload a valid resume."

if __name__ == '__main__':
    app.run(debug=True)
