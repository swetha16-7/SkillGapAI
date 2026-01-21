from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from document_parser import DocumentParser
from skill_extractor import SkillExtractor
from skill_gap_analyzer import SkillGapAnalyzer
import json
from report_generator import ReportGenerator
from chatbot import SkillAnalysisChatbot

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Initialize chatbot
chatbot = SkillAnalysisChatbot()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'resume' not in request.files or 'job_description' not in request.files:
            return jsonify({'error': 'Both resume and job description files are required'}), 400

        resume_file = request.files['resume']
        jd_file = request.files['job_description']

        if resume_file.filename == '' or jd_file.filename == '':
            return jsonify({'error': 'No files selected'}), 400

        if not (allowed_file(resume_file.filename) and allowed_file(jd_file.filename)):
            return jsonify({'error': 'Invalid file format. Supported: PDF, DOCX, TXT'}), 400

        # Save files
        resume_filename = secure_filename(resume_file.filename)
        jd_filename = secure_filename(jd_file.filename)

        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)

        resume_file.save(resume_path)
        jd_file.save(jd_path)

        # Parse documents
        parser = DocumentParser()
        resume_text = parser.parse(resume_path)
        jd_text = parser.parse(jd_path)

        # Validate that we have actual content
        if not resume_text.strip():
            return jsonify({'error': 'Resume file appears to be empty or could not be read'}), 400

        if not jd_text.strip():
            return jsonify({'error': 'Job description file appears to be empty or could not be read'}), 400

        # Debug logging
        import hashlib
        resume_hash = hashlib.md5(resume_text.encode()).hexdigest()[:8]
        jd_hash = hashlib.md5(jd_text.encode()).hexdigest()[:8]

        print(f"Resume file: {resume_filename}, size: {len(resume_text)} chars, hash: {resume_hash}")
        print(f"Resume text preview: {resume_text[:200]}...")
        print(f"JD file: {jd_filename}, size: {len(jd_text)} chars, hash: {jd_hash}")
        print(f"JD text preview: {jd_text[:200]}...")

        # Extract skills
        skill_extractor = SkillExtractor()
        resume_skills = skill_extractor.extract_skills(resume_text)
        jd_skills = skill_extractor.extract_skills(jd_text)

        print(f"Resume skills: {resume_skills}")
        print(f"JD skills: {jd_skills}")

        # Analyze skill gap
        analyzer = SkillGapAnalyzer()
        analysis_result = analyzer.analyze(resume_skills, jd_skills)

        print(f"Analysis result: {analysis_result}")

        # Store analysis data in session for chatbot access
        session['analysis_data'] = {
            'resume_skills': resume_skills,
            'jd_skills': jd_skills,
            'analysis': analysis_result
        }

        # Clean up uploaded files
        os.remove(resume_path)
        os.remove(jd_path)

        return jsonify({
            'success': True,
            'resume_skills': resume_skills,
            'jd_skills': jd_skills,
            'analysis': analysis_result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Supported: PDF, DOCX, TXT'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Parse the document using the same parser used for analysis
            parser = DocumentParser()
            text_content = parser.parse(file_path)

            # Clean up the temporary file
            os.remove(file_path)

            # Limit preview to reasonable size for display
            max_length = 5000
            if len(text_content) > max_length:
                text_content = text_content[:max_length] + '\n\n[... Content truncated for preview ...]'

            return jsonify({
                'success': True,
                'content': text_content,
                'filename': filename,
                'file_size': len(text_content)
            })

        except Exception as parse_error:
            # Clean up file even if parsing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': f'Failed to parse file: {str(parse_error)}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_report', methods=['POST'])
def export_report():
    try:
        data = request.json
        report_type = data.get('type', 'pdf')  # pdf or csv

        generator = ReportGenerator()

        if report_type == 'pdf':
            report_path = generator.generate_pdf_report(data)
            return send_file(report_path, as_attachment=True, download_name='skill_gap_report.pdf')
        elif report_type == 'csv':
            report_path = generator.generate_csv_report(data)
            return send_file(report_path, as_attachment=True, download_name='skill_gap_report.csv')
        else:
            return jsonify({'error': 'Invalid report type'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Get analysis data from session
        analysis_data = session.get('analysis_data')

        # Fallback: accept analysis data from the client (e.g., dashboard reload without session)
        if not analysis_data:
            analysis_data = data.get('analysis_data')

        if analysis_data:
            chatbot.set_analysis_data(analysis_data)
            # Refresh session copy so subsequent requests keep it
            session['analysis_data'] = analysis_data

        # Get chatbot response
        response = chatbot.get_response(user_message)

        return jsonify({
            'response': response,
            'timestamp': json.dumps({'timestamp': str(datetime.now())})
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
