from flask import Flask, request, jsonify, send_file
from builder import generate_summary, generate_structured_resume
from parser import parse_resume
from main import save_outputs, clean_raw_json
import tempfile
import os
import json
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def build_resume_files(data):
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone', '')
    raw_text = data.get('raw_text', '')
    summary = generate_summary(raw_text)
    profile = {'personal_info': {'name': name, 'email': email, 'phone': phone}, 'skills': [], 'experience': []}
    raw_json_str = generate_structured_resume(profile, summary, raw_text)
    raw_json_str = re.sub(r'<think>.*?</think>', '', raw_json_str, flags=re.DOTALL).strip()
    clean_json = clean_raw_json(raw_json_str)
    resume = parse_resume(clean_json)
    # Save to temp files
    temp_dir = tempfile.mkdtemp()
    md_path = os.path.join(temp_dir, 'resume.md')
    json_path = os.path.join(temp_dir, 'raw_resume.json')
    pdf_path = os.path.join(temp_dir, 'resume.pdf')
    save_outputs(resume, json_path, md_path, pdf_path)
    return summary, clean_json, md_path, json_path, pdf_path

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    summary, clean_json, md_path, json_path, pdf_path = build_resume_files(data)
    # Return summary, JSON, and file download URLs (for demo, just send files inline)
    with open(json_path) as f:
        resume_json = json.load(f)
    with open(md_path) as f:
        resume_md = f.read()
    return jsonify({
        'summary': summary,
        'resume_json': resume_json,
        'resume_md': resume_md,
        'pdf_url': '/download/pdf',
        'md_url': '/download/md',
        'json_url': '/download/json',
        'temp_dir': os.path.basename(os.path.dirname(md_path))
    })

@app.route('/download/<filetype>')
def download(filetype):
    temp_dir = request.args.get('temp_dir')
    if not temp_dir:
        return 'Missing temp_dir', 400
    base = os.path.join(tempfile.gettempdir(), temp_dir)
    if filetype == 'pdf':
        path = os.path.join(base, 'resume.pdf')
        return send_file(path, as_attachment=True)
    elif filetype == 'md':
        path = os.path.join(base, 'resume.md')
        return send_file(path, as_attachment=True)
    elif filetype == 'json':
        path = os.path.join(base, 'raw_resume.json')
        return send_file(path, as_attachment=True)
    else:
        return 'Invalid filetype', 400

if __name__ == '__main__':
    app.run(debug=True)
