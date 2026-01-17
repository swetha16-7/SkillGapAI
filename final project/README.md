# SkillGap AI - Resume & Job Description Skill Gap Analysis

A user-friendly web application that automatically analyzes resumes and job descriptions to identify skill gaps, matching skills, and provide actionable insights for both candidates and recruiters.

## Features

- **Multi-format Document Support**: Upload resumes and job descriptions in PDF, DOCX, or TXT formats
- **Intelligent Skill Extraction**: Automatically extracts technical and soft skills using NLP
- **Advanced Skill Gap Analysis**: Uses BERT embeddings for semantic matching to identify:
  - Fully matched skills
  - Partially matched skills
  - Missing skills
  - Extra skills in resume
- **Interactive Dashboard**: Visual representation of skill gaps with charts and graphs
- **Report Export**: Generate comprehensive reports in PDF or CSV format
- **Real-time Analysis**: Get instant results with detailed insights

## Technology Stack

### Frontend
- HTML5
- CSS3 (with modern gradients and animations)
- JavaScript (ES6+)
- Chart.js for visualizations

### Backend
- Python 3.8+
- Flask (Web framework)
- PyPDF2 / pdfplumber (PDF parsing)
- python-docx (DOCX parsing)
- spaCy (NLP preprocessing)
- Sentence Transformers / BERT (Semantic skill embeddings)
- scikit-learn (Cosine similarity)
- ReportLab (PDF report generation)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "Skill gap ai"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### Step 5: Create Required Directories
The application will automatically create `uploads/` and `reports/` directories when you run it.

## Running the Application

### Start the Flask Server
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Open in Browser
Navigate to `http://localhost:5000` in your web browser.

## Usage

1. **Upload Documents**:
   - Upload your resume (PDF, DOCX, or TXT)
   - Upload the job description (PDF, DOCX, or TXT)

2. **Analyze**:
   - Click "Analyze Skill Gap" button
   - Wait for the analysis to complete (usually takes 10-30 seconds)

3. **View Results**:
   - See overall match percentage
   - Review matched, partially matched, and missing skills
   - View skill distribution charts
   - Check extra skills in your resume

4. **Export Reports**:
   - Click "Export PDF Report" for a detailed PDF report
   - Click "Export CSV Report" for spreadsheet-compatible data
   - Use reports for interview preparation or candidate evaluation

## Project Structure

```
Skill gap ai/
├── app.py                 # Flask application main file
├── document_parser.py     # Document parsing module
├── skill_extractor.py     # Skill extraction using NLP
├── skill_gap_analyzer.py  # BERT-based skill gap analysis
├── report_generator.py    # PDF/CSV report generation
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── main.js      # Frontend JavaScript
├── uploads/              # Temporary file storage (auto-created)
└── reports/              # Generated reports (auto-created)
```

## Key Features Explained

### 1. Document Parsing
- Supports multiple formats (PDF, DOCX, TXT)
- Robust text extraction with error handling
- Automatic format detection

### 2. Skill Extraction
- Pre-built database of common technical and soft skills
- NLP-based extraction for additional skills
- Categorization into technical and soft skills

### 3. Skill Gap Analysis
- Semantic matching using BERT embeddings
- Cosine similarity for skill comparison
- Identifies exact matches, partial matches, and gaps
- Calculates overall match percentage

### 4. Visualization
- Pie charts for skill distribution
- Color-coded skill tags
- Interactive dashboard

### 5. Report Generation
- Professional PDF reports with detailed analysis
- CSV exports for data analysis
- Includes recommendations and insights

## Troubleshooting

### Issue: spaCy model not found
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: SentenceTransformer model download
**Solution**: The model will download automatically on first use. Ensure you have internet connection.

### Issue: File upload fails
**Solution**: 
- Check file size (max 16MB)
- Ensure file format is PDF, DOCX, or TXT
- Check file is not corrupted

### Issue: Analysis takes too long
**Solution**: 
- First run may take longer due to model downloads
- Large documents may take more time
- Ensure sufficient system resources

## Future Enhancements

- User authentication and profile management
- Historical analysis tracking
- Integration with job boards
- Advanced upskilling recommendations
- Multi-language support
- API endpoints for integration

## Contributing

This is a project by Team D. For contributions or suggestions, please contact the team.

## License

This project is developed for educational and professional use.

## Team

- Tejaswini
- Mayuri
- Bhavya
- Swetha
- Rishitha

---

**SkillGap AI** - Making hiring smarter and career growth data-driven.
