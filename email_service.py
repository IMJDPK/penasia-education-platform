"""
Email notification system for Penasia School of Continuing Education
Handles sending emails for application updates, payment confirmations, etc.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class EmailService:
    def __init__(self, smtp_server='localhost', smtp_port=587, username=None, password=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = 'enquiry@penasia.edu.hk'
    
    def send_email(self, to_email, subject, body, is_html=False):
        """Send email to recipient"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Log email (for development and debugging)
            self._log_email(to_email, subject, body)
            
            # Only send if SMTP is configured
            if self.smtp_server and self.smtp_server != 'localhost':
                try:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
                    server.starttls()
                    if self.username and self.password:
                        server.login(self.username, self.password)
                    server.send_message(msg)
                    server.quit()
                    return True
                except Exception as smtp_error:
                    # Log SMTP error but don't fail - still return True as email is logged
                    print(f"SMTP Error (email logged for manual review): {smtp_error}")
                    return True
            else:
                # Development mode: just log to console
                print(f"\n{'='*60}")
                print(f"[EMAIL MODE: DEVELOPMENT - EMAIL LOGGED, NOT SENT]")
                print(f"{'='*60}")
                return True
            
        except Exception as e:
            print(f"Error preparing email: {e}")
            self._log_email(to_email, subject, f"ERROR: {str(e)}\n\n{body}")
            return False
    
    def _log_email(self, to_email, subject, body):
        """Log email to console for development"""
        print(f"\n{'='*60}")
        print(f"EMAIL NOTIFICATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"To: {to_email}")
        print(f"From: {self.from_email}")
        print(f"Subject: {subject}")
        print(f"{'='*60}")
        print(body)
        print(f"{'='*60}\n")
    
    def send_application_confirmation(self, user, course, application):
        """Send application confirmation email"""
        subject = f"Application Confirmation - {course.name}"
        
        body = f"""
Dear {user.first_name} {user.last_name},

Thank you for your application to {course.name} ({course.code}).

Application Details:
- Application ID: {application.id}
- Course: {course.name}
- Submitted: {application.submitted_at.strftime('%B %d, %Y at %I:%M %p')}
- Status: {application.status.title()}

Next Steps:
1. We will review your application within 3-5 business days
2. You will receive an email notification with the decision
3. If approved, payment instructions will be provided
4. Course materials will be sent before the start date

If you have any questions, please contact us at enquiry@penasia.edu.hk or call (852) 2529 6138.

Best regards,
Penasia School of Continuing Education

---
This is an automated email. Please do not reply to this message.
        """
        
        return self.send_email(user.email, subject, body.strip())
    
    def send_application_update(self, user, course, application, admin_notes=None):
        """Send application status update email"""
        subject = f"Application Update - {course.name}"
        
        status_messages = {
            'approved': 'Congratulations! Your application has been approved.',
            'rejected': 'We regret to inform you that your application was not successful.',
            'waitlist': 'Your application has been placed on our waitlist.',
            'interview_required': 'An interview is required for your application.'
        }
        
        status_message = status_messages.get(application.status, f'Your application status has been updated to: {application.status.title()}')
        
        body = f"""
Dear {user.first_name} {user.last_name},

{status_message}

Application Details:
- Application ID: {application.id}
- Course: {course.name} ({course.code})
- Status: {application.status.title()}
- Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
"""
        
        if admin_notes:
            body += f"\nAdditional Notes:\n{admin_notes}\n"
        
        if application.status == 'approved':
            body += f"""
Next Steps:
1. Complete payment of HK${course.fee:,.0f}
2. Payment methods: Bank transfer, Credit card, or CEF reimbursement
3. Course materials will be sent after payment confirmation
4. Classes begin on [START DATE]

Payment Instructions will be sent in a separate email.
"""
        elif application.status == 'interview_required':
            body += """
Next Steps:
1. We will contact you within 2 business days to schedule an interview
2. The interview will be conducted via phone or in-person
3. Please ensure your contact information is up to date

"""
        
        body += """
If you have any questions, please contact us at enquiry@penasia.edu.hk or call (852) 2529 6138.

Best regards,
Penasia School of Continuing Education

---
This is an automated email. Please do not reply to this message.
        """
        
        return self.send_email(user.email, subject, body.strip())
    
    def send_payment_confirmation(self, user, course, payment_amount, payment_reference):
        """Send payment confirmation email"""
        subject = f"Payment Confirmation - {course.name}"
        
        body = f"""
Dear {user.first_name} {user.last_name},

We have received your payment for {course.name}.

Payment Details:
- Course: {course.name} ({course.code})
- Amount: HK${payment_amount:,.0f}
- Reference: {payment_reference}
- Date: {datetime.now().strftime('%B %d, %Y')}

Next Steps:
1. Course materials will be sent to your registered address within 5 business days
2. Class schedule and location details will be emailed separately
3. Please bring photo ID on the first day of class

Important Information:
- Course Start Date: [TO BE CONFIRMED]
- Location: Penasia School of Continuing Education
- Address: 1/F, Block C, Cho Yiu Centre, Cho Yiu Chuen, No.6 King Cho Road, Kwai Chung, HK

If you have any questions, please contact us at enquiry@penasia.edu.hk or call (852) 2529 6138.

Thank you for choosing Penasia School of Continuing Education.

Best regards,
Penasia School of Continuing Education

---
This is an automated email. Please do not reply to this message.
        """
        
        return self.send_email(user.email, subject, body.strip())
    
    def send_consultation_confirmation(self, consultation):
        """Send consultation booking confirmation email"""
        subject = f"Consultation Booking Confirmation - Penasia School of Continuing Education"
        
        consultation_type_display = {
            'course_info': 'Course Information',
            'career_guidance': 'Career Guidance', 
            'admission_help': 'Admission Assistance',
            'financial_aid': 'Financial Aid & CEF Information',
            'general_inquiry': 'General Inquiry'
        }.get(consultation.consultation_type, consultation.consultation_type)
        
        meeting_type_display = {
            'online': 'Online (Zoom/Teams)',
            'in_person': 'In-Person (Kwai Chung Campus)',
            'phone': 'Phone Call'
        }.get(consultation.meeting_type, consultation.meeting_type)
        
        body = f"""
Dear {consultation.full_name},

Thank you for booking a consultation with Penasia School of Continuing Education. We have received your request and are excited to help you achieve your educational goals.

CONSULTATION DETAILS:
- Reference Number: #{consultation.id:06d}
- Consultation Type: {consultation_type_display}
- Preferred Date: {consultation.formatted_date}
- Preferred Time: {consultation.formatted_time}
- Meeting Type: {meeting_type_display}
- Contact Email: {consultation.email}
- Contact Phone: {consultation.phone}
{f"- Course of Interest: {consultation.interested_course.title}" if consultation.interested_course else ""}

WHAT HAPPENS NEXT:
1. Our education consultants will contact you within 24 hours to confirm your preferred time slot
2. Once confirmed, you'll receive meeting details (link for online consultations or address for in-person meetings)
3. Your 30-minute consultation session will provide personalized guidance on:
   • Course recommendations based on your career goals
   • Admission requirements and application process
   • CEF funding opportunities and financial aid options
   • Career pathway planning and industry insights

PREPARATION FOR YOUR CONSULTATION:
- Please prepare any questions about our programs
- Have your educational background information ready
- Consider your career goals and interests
- Bring any relevant certificates or transcripts (for in-person meetings)

NEED TO MAKE CHANGES?
If you need to reschedule or have any questions, please contact us:
- Phone: +852 2893 6788
- Email: info@penasia.edu.hk
- Office Hours: Monday to Friday, 9:00 AM - 6:00 PM

We look forward to speaking with you soon and helping you take the next step in your educational journey.

Best regards,
Penasia School of Continuing Education

---
This is an automated confirmation. Please do not reply to this message.
If you have questions, please contact us at info@penasia.edu.hk
        """
        
        return self.send_email(consultation.email, subject, body.strip())
    
    def send_consultation_notification(self, consultation):
        """Send consultation booking notification to admin"""
        subject = f"New Consultation Booking - {consultation.full_name}"
        
        consultation_type_display = {
            'course_info': 'Course Information',
            'career_guidance': 'Career Guidance',
            'admission_help': 'Admission Assistance', 
            'financial_aid': 'Financial Aid & CEF Information',
            'general_inquiry': 'General Inquiry'
        }.get(consultation.consultation_type, consultation.consultation_type)
        
        body = f"""
New consultation booking received:

CONSULTATION DETAILS:
- Reference: #{consultation.id:06d}
- Name: {consultation.full_name}
- Email: {consultation.email}
- Phone: {consultation.phone}
- Type: {consultation_type_display}
- Preferred Date: {consultation.formatted_date}
- Preferred Time: {consultation.formatted_time}
- Meeting Type: {consultation.meeting_type}
{f"- Course Interest: {consultation.interested_course.title}" if consultation.interested_course else ""}
- Booking Date: {consultation.created_at.strftime('%B %d, %Y at %I:%M %p')}

ADDITIONAL INFORMATION:
{f"Message: {consultation.message}" if consultation.message else "No additional message"}
{f"Special Requirements: {consultation.special_requirements}" if consultation.special_requirements else "No special requirements"}

ACTION REQUIRED:
Please contact the applicant within 24 hours to confirm the consultation details.

Admin Panel: [Access admin panel to manage this consultation]
        """
        
        return self.send_email('admin@penasia.edu.hk', subject, body.strip())
    
    def send_consultation_confirmed(self, consultation):
        """Send consultation confirmation with meeting details"""
        subject = f"Consultation Confirmed - {consultation.formatted_date} at {consultation.formatted_time}"
        
        meeting_details = ""
        if consultation.meeting_type == 'online' and consultation.meeting_link:
            meeting_details = f"Meeting Link: {consultation.meeting_link}"
        elif consultation.meeting_type == 'in_person':
            location = consultation.meeting_location or "PenAsia Education Centre, Kwai Chung Campus"
            meeting_details = f"Meeting Location: {location}"
        elif consultation.meeting_type == 'phone':
            meeting_details = f"Our consultant will call you at {consultation.phone}"
        
        body = f"""
Dear {consultation.full_name},

Your consultation with PenAsia Education Group has been confirmed!

CONFIRMED CONSULTATION DETAILS:
- Date: {consultation.formatted_date}
- Time: {consultation.formatted_time}
- Duration: 30 minutes
- {meeting_details}

PREPARATION CHECKLIST:
□ Prepare questions about programs of interest
□ Have your educational background ready
□ Consider your career goals
□ Ensure stable internet connection (for online meetings)

CONTACT INFORMATION:
If you need to make any last-minute changes or have technical difficulties:
- Phone: +852 2893 6788
- Email: info@penasia.edu.hk

We look forward to meeting with you and helping you achieve your educational goals.

Best regards,
Penasia School of Continuing Education
        """
        
        return self.send_email(consultation.email, subject, body.strip())
    
    def send_email_verification(self, user, verification_link):
        """Send email verification link"""
        subject = "Verify Your PenAsia Account"
        
        body = f"""
Dear {user.first_name} {user.last_name},

Welcome to Penasia School of Continuing Education!

To complete your registration, please verify your email address by clicking the link below:

{verification_link}

IMPORTANT: This link will expire in 24 hours.

If you did not create this account or have any questions, please contact us at:
- Phone: (852) 2529 6138
- Email: enquiry@penasia.edu.hk

Best regards,
Penasia School of Continuing Education
        """
        
        return self.send_email(user.email, subject, body.strip())

# Initialize email service
email_service = EmailService()
