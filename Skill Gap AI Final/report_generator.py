from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import csv
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_pdf_report(self, data):
        """Generate PDF report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"skill_gap_report_{timestamp}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Skill Gap Analysis Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary Section
        summary_style = ParagraphStyle(
            'SummaryStyle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        analysis = data.get('analysis', {})
        summary = analysis.get('summary', {})
        
        story.append(Paragraph("Executive Summary", summary_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Overall Match Percentage', f"{analysis.get('match_percentage', 0)}%"],
            ['Total Resume Skills', str(summary.get('total_resume_skills', 0))],
            ['Total Job Description Skills', str(summary.get('total_jd_skills', 0))],
            ['Matched Skills', str(summary.get('matched_count', 0))],
            ['Missing Skills', str(summary.get('missing_count', 0))]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Matched Skills
        story.append(Paragraph("Matched Skills", summary_style))
        matched = analysis.get('matched', {})
        matched_tech = ', '.join(matched.get('technical', [])) or 'None'
        matched_soft = ', '.join(matched.get('soft', [])) or 'None'
        
        story.append(Paragraph(f"<b>Technical:</b> {matched_tech}", styles['Normal']))
        story.append(Paragraph(f"<b>Soft Skills:</b> {matched_soft}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Missing Skills
        story.append(Paragraph("Missing Skills", summary_style))
        missing = analysis.get('missing', {})
        missing_tech = ', '.join(missing.get('technical', [])) or 'None'
        missing_soft = ', '.join(missing.get('soft', [])) or 'None'
        
        story.append(Paragraph(f"<b>Technical:</b> {missing_tech}", styles['Normal']))
        story.append(Paragraph(f"<b>Soft Skills:</b> {missing_soft}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Partially Matched Skills
        partially_matched = analysis.get('partially_matched', {})
        if partially_matched.get('technical') or partially_matched.get('soft'):
            story.append(Paragraph("Partially Matched Skills", summary_style))
            
            for pm in partially_matched.get('technical', []):
                story.append(Paragraph(
                    f"<b>{pm['jd_skill']}</b> (similar to {pm['resume_skill']}, {pm['similarity']*100:.1f}% match)",
                    styles['Normal']
                ))
            
            for pm in partially_matched.get('soft', []):
                story.append(Paragraph(
                    f"<b>{pm['jd_skill']}</b> (similar to {pm['resume_skill']}, {pm['similarity']*100:.1f}% match)",
                    styles['Normal']
                ))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)
        ))
        
        doc.build(story)
        return filepath
    
    def generate_csv_report(self, data):
        """Generate CSV report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"skill_gap_report_{timestamp}.csv"
        filepath = os.path.join(self.reports_dir, filename)
        
        analysis = data.get('analysis', {})
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow(['Skill Gap Analysis Report'])
            # Excel can show "####" when it auto-formats date/time into a too-narrow column.
            # Prefix with an apostrophe so Excel treats it as text (apostrophe is not displayed).
            generated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(['Generated:', f"'{generated_at}"])
            writer.writerow([])
            
            # Summary
            writer.writerow(['Summary'])
            writer.writerow(['Match Percentage', f"{analysis.get('match_percentage', 0)}%"])
            summary = analysis.get('summary', {})
            writer.writerow(['Total Resume Skills', summary.get('total_resume_skills', 0)])
            writer.writerow(['Total JD Skills', summary.get('total_jd_skills', 0)])
            writer.writerow(['Matched Skills', summary.get('matched_count', 0)])
            writer.writerow(['Missing Skills', summary.get('missing_count', 0)])
            writer.writerow([])
            
            # Matched Skills
            writer.writerow(['Matched Technical Skills'])
            matched = analysis.get('matched', {})
            for skill in matched.get('technical', []):
                writer.writerow([skill])
            writer.writerow([])
            
            writer.writerow(['Matched Soft Skills'])
            for skill in matched.get('soft', []):
                writer.writerow([skill])
            writer.writerow([])
            
            # Missing Skills
            writer.writerow(['Missing Technical Skills'])
            missing = analysis.get('missing', {})
            for skill in missing.get('technical', []):
                writer.writerow([skill])
            writer.writerow([])
            
            writer.writerow(['Missing Soft Skills'])
            for skill in missing.get('soft', []):
                writer.writerow([skill])
            writer.writerow([])
            
            # Partially Matched
            partially_matched = analysis.get('partially_matched', {})
            if partially_matched.get('technical') or partially_matched.get('soft'):
                writer.writerow(['Partially Matched Skills'])
                writer.writerow(['JD Skill', 'Resume Skill', 'Similarity %'])
                
                for pm in partially_matched.get('technical', []):
                    writer.writerow([pm['jd_skill'], pm['resume_skill'], f"{pm['similarity']*100:.1f}%"])
                
                for pm in partially_matched.get('soft', []):
                    writer.writerow([pm['jd_skill'], pm['resume_skill'], f"{pm['similarity']*100:.1f}%"])
        
        return filepath
