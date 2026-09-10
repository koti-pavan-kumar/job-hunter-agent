"""
PDF Converter - Convert text resumes to PDF format
"""
from pathlib import Path
from datetime import datetime
import io

class PDFConverter:
    """Convert text resumes to PDF format"""
    
    def __init__(self):
        self.font_name = "Helvetica"
        self.font_size = 10
        self.margin = 50
    
    def convert_text_to_pdf(self, text_content: str, output_path: str = None) -> bytes:
        """Convert text content to PDF bytes"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            
            # Create PDF in memory
            buffer = io.BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                textColor=colors.HexColor('#1a56db')
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=10,
                spaceBefore=15,
                textColor=colors.HexColor('#1a56db')
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=5,
                leading=14
            )
            
            bullet_style = ParagraphStyle(
                'CustomBullet',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=3,
                leftIndent=20,
                leading=13
            )
            
            # Build content
            content = []
            
            # Split text by lines and format
            lines = text_content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    content.append(Spacer(1, 5))
                    continue
                
                # Section headers (lines with ===)
                if line.startswith('==='):
                    continue
                
                # Main title (first non-empty line)
                if not content or (len(content) <= 2 and line != ''):
                    content.append(Paragraph(line, title_style))
                # Section headers
                elif line.isupper() and len(line) > 3:
                    content.append(Paragraph(line, heading_style))
                # Bullet points
                elif line.startswith('•') or line.startswith('-'):
                    content.append(Paragraph(line, bullet_style))
                # Regular text
                else:
                    content.append(Paragraph(line, body_style))
            
            # Build PDF
            doc.build(content)
            
            # Get PDF bytes
            buffer.seek(0)
            pdf_bytes = buffer.read()
            
            return pdf_bytes
            
        except ImportError:
            # Fallback: create simple text-based PDF
            return self._create_simple_pdf(text_content)
    
    def _create_simple_pdf(self, text_content: str) -> bytes:
        """Create a simple PDF without reportlab"""
        # Create a minimal PDF structure
        pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj

4 0 obj
<< /Length 500 >>
stream
BT
/F1 12 Tf
50 750 Td
(Job Hunter Agent - Resume) Tj
0 -30 Td
/F1 10 Tf
(Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) Tj
0 -20 Td
( ) Tj
0 -15 Td
(This is a text-based resume.) Tj
0 -15 Td
(For better formatting, install reportlab:) Tj
0 -15 Td
(pip install reportlab) Tj
ET
endstream
endobj

5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj

xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000818 00000 n 

trailer
<< /Size 6 /Root 1 0 R >>
startxref
895
%%EOF"""
        
        return pdf_content.encode('latin-1')
    
    def convert_resume_folder_to_pdf(self, folder_path: str) -> bytes:
        """Convert a resume folder's content to PDF"""
        folder = Path(folder_path)
        
        # Read resume content
        resume_path = folder / "resume.txt"
        if not resume_path.exists():
            raise FileNotFoundError(f"Resume not found: {resume_path}")
        
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_content = f.read()
        
        # Convert to PDF
        return self.convert_text_to_pdf(resume_content)
    
    def convert_cover_letter_to_pdf(self, folder_path: str) -> bytes:
        """Convert a cover letter to PDF"""
        folder = Path(folder_path)
        
        # Read cover letter content
        cover_letter_path = folder / "cover_letter.txt"
        if not cover_letter_path.exists():
            raise FileNotFoundError(f"Cover letter not found: {cover_letter_path}")
        
        with open(cover_letter_path, "r", encoding="utf-8") as f:
            cover_letter_content = f.read()
        
        # Convert to PDF
        return self.convert_text_to_pdf(cover_letter_content)

# Global instance
pdf_converter = PDFConverter()
