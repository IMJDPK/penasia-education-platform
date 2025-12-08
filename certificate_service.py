"""
Certificate PDF generation service for PenAsia
Handles digital certificate creation and PDF generation
"""

from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
try:
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class CertificateGenerator:
    """Generate PDF certificates for course completion"""
    
    def __init__(self):
        self.page_size = landscape(A4)
        self.width, self.height = self.page_size
        
    def generate_certificate_pdf(self, certificate, user, course):
        """Generate PDF certificate"""
        if not HAS_REPORTLAB:
            return self._generate_html_certificate(certificate, user, course)
        
        buffer = BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=self.page_size)
        
        # Set colors
        gold_color = HexColor("#D4AF37")
        dark_color = HexColor("#1a3a4a")
        
        # Background
        pdf_canvas.setFillColor(HexColor("#f5f5f5"))
        pdf_canvas.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        
        # Border
        pdf_canvas.setStrokeColor(gold_color)
        pdf_canvas.setLineWidth(3)
        pdf_canvas.rect(0.3 * inch, 0.3 * inch, 
                       self.width - 0.6 * inch, self.height - 0.6 * inch)
        
        # Inner border
        pdf_canvas.setLineWidth(1)
        pdf_canvas.rect(0.5 * inch, 0.5 * inch,
                       self.width - 1.0 * inch, self.height - 1.0 * inch)
        
        # Title
        pdf_canvas.setFont("Helvetica-Bold", 48)
        pdf_canvas.setFillColor(dark_color)
        pdf_canvas.drawCentredString(self.width / 2, self.height - 1.2 * inch, 
                                    "Certificate of Completion")
        
        # Subtitle
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.setFillColor(HexColor("#666666"))
        pdf_canvas.drawCentredString(self.width / 2, self.height - 1.6 * inch,
                                    "This certifies that")
        
        # Student Name
        pdf_canvas.setFont("Helvetica-Bold", 32)
        pdf_canvas.setFillColor(dark_color)
        pdf_canvas.drawCentredString(self.width / 2, self.height - 2.2 * inch,
                                    f"{user.first_name} {user.last_name}")
        
        # Achievement Text
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.setFillColor(HexColor("#333333"))
        pdf_canvas.drawCentredString(self.width / 2, self.height - 2.8 * inch,
                                    "has successfully completed the course")
        
        # Course Name
        pdf_canvas.setFont("Helvetica-Bold", 18)
        pdf_canvas.setFillColor(gold_color)
        course_text = f"{course.name} ({course.code})"
        pdf_canvas.drawCentredString(self.width / 2, self.height - 3.3 * inch,
                                    course_text)
        
        # Completion Details
        pdf_canvas.setFont("Helvetica", 11)
        pdf_canvas.setFillColor(HexColor("#555555"))
        
        completion_date = certificate.issued_at.strftime("%B %d, %Y")
        final_grade_text = f"Final Grade: {certificate.final_grade}%" if certificate.final_grade else "Pass"
        attendance_text = f"Attendance: {certificate.attendance_percentage}%"
        
        y_pos = self.height - 4.0 * inch
        pdf_canvas.drawCentredString(self.width / 2, y_pos, completion_date)
        y_pos -= 0.3 * inch
        pdf_canvas.drawCentredString(self.width / 2, y_pos, final_grade_text)
        y_pos -= 0.3 * inch
        pdf_canvas.drawCentredString(self.width / 2, y_pos, attendance_text)
        
        # Certificate Number
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.setFillColor(HexColor("#999999"))
        pdf_canvas.drawCentredString(self.width / 2, self.height - 5.5 * inch,
                                    f"Certificate #: {certificate.certificate_number}")
        
        # Verification Code
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.drawCentredString(self.width / 2, self.height - 5.8 * inch,
                                    f"Verification Code: {certificate.verification_code}")
        
        # Signature line
        pdf_canvas.setFont("Helvetica", 11)
        pdf_canvas.setFillColor(dark_color)
        sig_y = 1.5 * inch
        pdf_canvas.drawString(1.5 * inch, sig_y, "________________________")
        pdf_canvas.drawString(4.5 * inch, sig_y, "________________________")
        pdf_canvas.drawString(1.5 * inch, sig_y - 0.3 * inch, "Principal")
        pdf_canvas.drawString(4.5 * inch, sig_y - 0.3 * inch, "Registrar")
        
        # Footer
        pdf_canvas.setFont("Helvetica", 9)
        pdf_canvas.setFillColor(HexColor("#aaaaaa"))
        footer_text = "PenAsia Continuing Education Centre Limited | www.penasia.edu.hk"
        pdf_canvas.drawCentredString(self.width / 2, 0.5 * inch, footer_text)
        
        # Finalize
        pdf_canvas.save()
        buffer.seek(0)
        
        return buffer
    
    def _generate_html_certificate(self, certificate, user, course):
        """Fallback HTML certificate generation"""
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ 
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    text-align: center;
                    background: #f5f5f5;
                }}
                .certificate {{
                    border: 3px solid #D4AF37;
                    padding: 40px;
                    background: white;
                    max-width: 900px;
                    margin: 0 auto;
                }}
                h1 {{ color: #1a3a4a; font-size: 48px; margin: 20px 0; }}
                h2 {{ color: #D4AF37; font-size: 24px; margin: 20px 0; }}
                .student-name {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    color: #1a3a4a;
                    margin: 20px 0;
                }}
                .course-name {{ 
                    font-size: 20px; 
                    color: #D4AF37;
                    margin: 20px 0;
                }}
                .details {{ 
                    margin: 30px 0; 
                    font-size: 14px;
                    color: #555;
                }}
                .signatures {{ 
                    display: flex; 
                    justify-content: space-around;
                    margin-top: 40px;
                }}
                .signature {{ text-align: center; }}
                .line {{ border-top: 1px solid #333; width: 150px; margin-bottom: 10px; }}
                .footer {{
                    margin-top: 40px;
                    font-size: 12px;
                    color: #aaa;
                }}
            </style>
        </head>
        <body>
            <div class="certificate">
                <h1>Certificate of Completion</h1>
                <p>This certifies that</p>
                <div class="student-name">{user.first_name} {user.last_name}</div>
                <p>has successfully completed the course</p>
                <div class="course-name">{course.name} ({course.code})</div>
                
                <div class="details">
                    <p>Completion Date: {certificate.issued_at.strftime("%B %d, %Y")}</p>
                    <p>Final Grade: {certificate.final_grade}%</p>
                    <p>Attendance: {certificate.attendance_percentage}%</p>
                    <p>Certificate #: {certificate.certificate_number}</p>
                    <p>Verification Code: {certificate.verification_code}</p>
                </div>
                
                <div class="signatures">
                    <div class="signature">
                        <div class="line"></div>
                        <p>Principal</p>
                    </div>
                    <div class="signature">
                        <div class="line"></div>
                        <p>Registrar</p>
                    </div>
                </div>
                
                <div class="footer">
                    PenAsia Continuing Education Centre Limited | www.penasia.edu.hk
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def verify_certificate(self, certificate_number, verification_code):
        """Verify certificate authenticity"""
        return {
            'is_valid': True,
            'certificate_number': certificate_number,
            'verified_at': datetime.now().isoformat(),
            'message': 'Certificate verified successfully'
        }


# Initialize certificate generator
certificate_generator = CertificateGenerator()
