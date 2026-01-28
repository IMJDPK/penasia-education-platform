from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateField, EmailField, PasswordField, BooleanField, IntegerField, DecimalField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from models import User, Course


class LoginForm(FlaskForm):
    """User login form"""
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """User registration form"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email address already registered. Please use a different email.')


class ProfileForm(FlaskForm):
    """User profile update form"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
    emergency_contact_name = StringField('Emergency Contact Name', validators=[Optional(), Length(max=100)])
    emergency_contact_phone = StringField('Emergency Contact Phone', validators=[Optional(), Length(max=20)])


class CourseForm(FlaskForm):
    """Form for creating and editing courses"""
    course_code = StringField('Course Code', validators=[DataRequired(), Length(min=2, max=20)])
    title = StringField('Course Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20, max=5000)])
    
    duration_weeks = IntegerField('Duration (Weeks)', validators=[DataRequired(), NumberRange(min=1, max=104)])
    duration_hours = IntegerField('Duration (Hours)', validators=[DataRequired(), NumberRange(min=1, max=2000)])
    
    fee_hkd = DecimalField('Course Fee (HKD)', validators=[DataRequired(), NumberRange(min=0)])
    cef_eligible = BooleanField('CEF Eligible')
    cef_fee_hkd = DecimalField('CEF Fee (HKD)', validators=[Optional(), NumberRange(min=0)])
    
    max_students = IntegerField('Maximum Students', validators=[DataRequired(), NumberRange(min=1, max=100)])
    min_students = IntegerField('Minimum Students', validators=[DataRequired(), NumberRange(min=1, max=100)])
    
    language = SelectField('Language', validators=[DataRequired()], choices=[
        ('English', 'English'),
        ('Cantonese', 'Cantonese'),
        ('Mandarin', 'Mandarin'),
        ('English & Cantonese', 'English & Cantonese'),
        ('Other', 'Other')
    ])
    
    level = SelectField('Level', validators=[DataRequired()], choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Professional', 'Professional'),
        ('All Levels', 'All Levels')
    ])
    
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('Business', 'Business'),
        ('Culinary', 'Culinary'),
        ('Professional', 'Professional Development'),
        ('Language', 'Language'),
        ('Technology', 'Technology'),
        ('Healthcare', 'Healthcare'),
        ('Hospitality', 'Hospitality'),
        ('Other', 'Other')
    ])
    
    delivery_mode = SelectField('Delivery Mode', validators=[DataRequired()], choices=[
        ('offline', 'In-Person (Offline)'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid (Online & In-Person)')
    ], default='offline')
    
    prerequisites = TextAreaField('Prerequisites', validators=[Optional(), Length(max=1000)])
    learning_outcomes = TextAreaField('Learning Outcomes', validators=[Optional(), Length(max=2000)])
    course_content = TextAreaField('Course Content', validators=[Optional(), Length(max=5000)])
    assessment_method = TextAreaField('Assessment Method', validators=[Optional(), Length(max=1000)])
    certification = StringField('Certification', validators=[Optional(), Length(max=200)])
    
    is_active = BooleanField('Active')
    is_featured = BooleanField('Featured')


class CourseApplicationForm(FlaskForm):
    """Course application form"""
    course_id = SelectField('Course', validators=[DataRequired()], coerce=int)
    schedule_id = SelectField('Schedule', validators=[Optional()], coerce=int)
    
    # Personal details - additional fields for comprehensive application
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    
    education_level = SelectField('Education Level', validators=[DataRequired()], choices=[
        ('', 'Select Education Level'),
        ('form3', 'Form 3 (Grade 9)'),
        ('form5', 'Form 5 (Grade 11)'), 
        ('form6', 'Form 6 (Grade 12)'),
        ('diploma', 'Diploma'),
        ('degree', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('other', 'Other')
    ])
    
    english_level = SelectField('English Level', validators=[DataRequired()], choices=[
        ('', 'Select English Level'),
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('native', 'Native/Fluent'),
        ('ielts4', 'IELTS 4.0-4.5'),
        ('ielts5', 'IELTS 5.0-5.5'),
        ('ielts6', 'IELTS 6.0+')
    ])
    
    work_experience = TextAreaField('Work Experience', validators=[Optional(), Length(max=500)])
    motivation = TextAreaField('Why do you want to take this course?', validators=[
        DataRequired(), Length(min=50, max=1000, message='Please provide at least 50 characters explaining your motivation')
    ])
    
    # Documents upload
    documents = FileField('Upload Documents (CV, Certificates, ID)', 
                        validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents allowed!')])
    
    # Payment method
    payment_method = SelectField('Preferred Payment Method', validators=[DataRequired()], choices=[
        ('', 'Select Payment Method'),
        ('full', 'Full Payment'),
        ('installments', 'Installments'),
        ('cef', 'CEF Reimbursement'),
        ('company', 'Company Sponsorship')
    ])
    
    special_requirements = TextAreaField('Special Requirements or Accommodations', validators=[Optional(), Length(max=500)])
    

class AssignmentSubmissionForm(FlaskForm):
    """Assignment submission form"""
    submission_text = TextAreaField('Assignment Content', validators=[
        DataRequired(message='Please provide your assignment content'),
        Length(min=10, max=10000, message='Assignment content must be between 10 and 10000 characters')
    ], description='Enter your assignment text or description here')
    
    file_upload = FileField('Upload File', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip'], 
                   'Only PDF, Word, PowerPoint, and ZIP files are allowed')
    ], description='Upload supporting files (optional)')
    
    comments = TextAreaField('Additional Comments', validators=[
        Optional(), 
        Length(max=1000, message='Comments cannot exceed 1000 characters')
    ], description='Any additional comments for your instructor (optional)')


class AssignmentSubmissionForm(FlaskForm):
    """Assignment submission form"""
    submission_text = TextAreaField('Submission Content', validators=[
        DataRequired(message='Please provide your submission content'),
        Length(min=10, max=10000, message='Submission must be between 10 and 10,000 characters')
    ])
    file_upload = FileField('Upload File', validators=[
        Optional(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip'], 
                   'Only PDF, Word, PowerPoint, and ZIP files are allowed')
    ])
    comments = TextAreaField('Additional Comments', validators=[
        Optional(), 
        Length(max=1000, message='Comments cannot exceed 1000 characters')
    ])


class CourseApplicationForm(FlaskForm):
    """Course application form"""
    course_id = SelectField('Course', validators=[DataRequired()], coerce=int)
    schedule_id = SelectField('Schedule', validators=[Optional()], coerce=int)
    
    # Personal details - additional fields for comprehensive application
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    
    how_did_you_hear = SelectField('How did you hear about us?', validators=[DataRequired()], choices=[
        ('', 'Select Option'),
        ('website', 'Website Search'),
        ('social_media', 'Social Media'),
        ('friend_referral', 'Friend/Family Referral'),
        ('newspaper', 'Newspaper Advertisement'),
        ('education_fair', 'Education Fair'),
        ('government_website', 'Government Website'),
        ('other', 'Other')
    ])
    
    # CEF application
    cef_application = BooleanField('Apply for Continuing Education Fund (CEF) Subsidy')
    hkid_number = StringField('Hong Kong ID Number (Required for CEF)', validators=[Optional(), Length(max=20)])
    
    # Terms and conditions
    terms_accepted = BooleanField('I accept the terms and conditions', validators=[DataRequired()])
    
    def validate_hkid_number(self, hkid_number):
        if self.cef_application.data and not hkid_number.data:
            raise ValidationError('Hong Kong ID number is required for CEF applications.')


class ContactForm(FlaskForm):
    """Contact form"""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    subject = SelectField('Subject', validators=[DataRequired()], choices=[
        ('', 'Select Subject'),
        ('course_inquiry', 'Course Inquiry'),
        ('application_status', 'Application Status'),
        ('payment_issue', 'Payment Issue'),
        ('technical_support', 'Technical Support'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other')
    ])
    course_interest = SelectField('Course of Interest', validators=[Optional()], coerce=int)
    message = TextAreaField('Message', validators=[
        DataRequired(), 
        Length(min=20, max=2000, message='Message must be between 20 and 2000 characters')
    ])
    preferred_contact_method = SelectField('Preferred Contact Method', validators=[Optional()], choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('either', 'Either Email or Phone')
    ])


class CourseForm(FlaskForm):
    """Admin form for creating/editing courses"""
    course_code = StringField('Course Code', validators=[DataRequired(), Length(min=3, max=20)])
    title = StringField('Course Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=2000)])
    duration_weeks = IntegerField('Duration (Weeks)', validators=[DataRequired(), NumberRange(min=1, max=52)])
    duration_hours = IntegerField('Total Hours', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    fee_hkd = DecimalField('Course Fee (HKD)', validators=[DataRequired(), NumberRange(min=0)])
    cef_eligible = BooleanField('CEF Eligible')
    cef_fee_hkd = DecimalField('CEF Fee (HKD)', validators=[Optional(), NumberRange(min=0)])
    
    max_students = IntegerField('Maximum Students', validators=[DataRequired(), NumberRange(min=1, max=100)])
    min_students = IntegerField('Minimum Students', validators=[DataRequired(), NumberRange(min=1, max=50)])
    language = StringField('Language', validators=[Optional(), Length(max=50)], default='English')
    level = SelectField('Level', validators=[Optional()], choices=[
        ('', 'Select Level'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all_levels', 'All Levels')
    ])
    
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('', 'Select Category'),
        ('culinary', 'Culinary Arts'),
        ('business', 'Business Management'),
        ('professional', 'Professional Development'),
        ('technology', 'Technology'),
        ('language', 'Language'),
        ('other', 'Other')
    ])
    
    prerequisites = TextAreaField('Prerequisites', validators=[Optional(), Length(max=1000)])
    learning_outcomes = TextAreaField('Learning Outcomes', validators=[Optional(), Length(max=2000)])
    course_content = TextAreaField('Course Content', validators=[Optional(), Length(max=3000)])
    assessment_method = TextAreaField('Assessment Method', validators=[Optional(), Length(max=1000)])
    certification = StringField('Certification', validators=[Optional(), Length(max=200)])
    
    is_active = BooleanField('Active', default=True)
    is_featured = BooleanField('Featured Course')


class CourseScheduleForm(FlaskForm):
    """Admin form for creating course schedules"""
    course_id = SelectField('Course', validators=[DataRequired()], coerce=int)
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    day_of_week = SelectField('Day of Week', validators=[DataRequired()], choices=[
        ('', 'Select Day'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    instructor = StringField('Instructor', validators=[Optional(), Length(max=100)])
    
    registration_start = DateField('Registration Start Date', validators=[DataRequired()])
    registration_end = DateField('Registration End Date', validators=[DataRequired()])
    
    is_active = BooleanField('Active', default=True)
    
    def validate_end_date(self, end_date):
        if end_date.data <= self.start_date.data:
            raise ValidationError('End date must be after start date.')
    
    def validate_end_time(self, end_time):
        if end_time.data <= self.start_time.data:
            raise ValidationError('End time must be after start time.')
    
    def validate_registration_end(self, registration_end):
        if registration_end.data <= self.registration_start.data:
            raise ValidationError('Registration end date must be after registration start date.')
        if registration_end.data >= self.start_date.data:
            raise ValidationError('Registration must end before course starts.')


class SearchForm(FlaskForm):
    """Course search form"""
    search_query = StringField('Search Courses')
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('culinary', 'Culinary Arts'),
        ('business', 'Business Management'),
        ('professional', 'Professional Development'),
        ('technology', 'Technology'),
        ('language', 'Language'),
        ('other', 'Other')
    ])
    level = SelectField('Level', choices=[
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all_levels', 'All Levels')
    ])
    cef_eligible = BooleanField('CEF Eligible Only')
    max_fee = DecimalField('Maximum Fee (HKD)', validators=[Optional(), NumberRange(min=0)])


class ConsultationBookingForm(FlaskForm):
    """Consultation booking form"""
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    
    # Consultation Preferences
    consultation_type = SelectField('Consultation Type', validators=[DataRequired()], choices=[
        ('course_info', 'Course Information'),
        ('career_guidance', 'Career Guidance'),
        ('admission_help', 'Admission Assistance'),
        ('financial_aid', 'Financial Aid & CEF Information'),
        ('general_inquiry', 'General Inquiry')
    ])
    
    preferred_date = DateField('Preferred Date', validators=[DataRequired()])
    preferred_time = SelectField('Preferred Time', validators=[DataRequired()], choices=[
        ('09:00', '9:00 AM'),
        ('09:30', '9:30 AM'),
        ('10:00', '10:00 AM'),
        ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('14:00', '2:00 PM'),
        ('14:30', '2:30 PM'),
        ('15:00', '3:00 PM'),
        ('15:30', '3:30 PM'),
        ('16:00', '4:00 PM'),
        ('16:30', '4:30 PM'),
        ('17:00', '5:00 PM'),
        ('17:30', '5:30 PM'),
        ('18:00', '6:00 PM')
    ])
    
    meeting_type = SelectField('Meeting Type', validators=[DataRequired()], choices=[
        ('online', 'Online (Zoom/Teams)'),
        ('in_person', 'In-Person (Kwai Chung Campus)'),
        ('phone', 'Phone Call')
    ])
    
    # Course Interest (Optional)
    course_id = SelectField('Course of Interest (Optional)', coerce=lambda x: int(x) if x else None, choices=[], validators=[Optional()])
    
    # Additional Information
    message = TextAreaField('Additional Questions/Message', validators=[Optional(), Length(max=1000)])
    special_requirements = TextAreaField('Special Requirements/Accessibility Needs', validators=[Optional(), Length(max=500)])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate course choices
        self.course_id.choices = [(None, 'No specific course')] + [
            (c.id, f"{c.title} ({c.course_code})")
            for c in Course.query.filter_by(is_active=True).order_by(Course.title).all()
        ]
    
    def validate_preferred_date(self, preferred_date):
        from datetime import date, timedelta
        if preferred_date.data < date.today():
            raise ValidationError('Please select a future date.')
        if preferred_date.data > date.today() + timedelta(days=60):
            raise ValidationError('Please select a date within the next 60 days.')


class AssignmentSubmissionForm(FlaskForm):
    """Assignment submission form"""
    submission_text = TextAreaField('Submission Content', validators=[
        DataRequired(message='Please provide your submission content'),
        Length(min=10, max=10000, message='Submission must be between 10 and 10,000 characters')
    ])
    file_upload = FileField('Upload File', validators=[
        Optional(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip'], 
                   'Only PDF, Word, PowerPoint, and ZIP files are allowed')
    ])
    comments = TextAreaField('Additional Comments', validators=[
        Optional(), 
        Length(max=1000, message='Comments cannot exceed 1000 characters')
    ])


class ContactForm(FlaskForm):
    """Contact form"""
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=100, message='First name must be between 2 and 100 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=100, message='Last name must be between 2 and 100 characters')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(max=20, message='Phone number must be less than 20 characters')
    ])
    subject = SelectField('Subject', validators=[
        DataRequired(message='Please select a subject')
    ], choices=[
        ('', 'Choose a subject...'),
        ('general', 'General Inquiry'),
        ('admissions', 'Admissions Information'),
        ('programs', 'Program Details'),
        ('facilities', 'Facilities Tour'),
        ('fees', 'Fees and Payment'),
        ('cef', 'CEF Information'),
        ('other', 'Other')
    ])
    program_interest = SelectField('Program of Interest', validators=[Optional()], choices=[
        ('', 'Select a program...'),
        ('169', 'Hotel Culinary Management Diploma'),
        ('171', 'Certificate in Western Bakery & Pastry'),
        ('179', 'Certificate in Starter and Main Course')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=2000, message='Message must be between 10 and 2000 characters')
    ])
    subscribe_newsletter = BooleanField('I would like to receive updates about programs and events')
