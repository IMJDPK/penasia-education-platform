from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and student/admin accounts"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    
    # User role and status
    role = db.Column(db.String(20), nullable=False, default='student')  # student, admin, staff
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', foreign_keys='Application.user_id', backref='applicant', lazy=True, cascade='all, delete-orphan')
    reviewed_applications = db.relationship('Application', foreign_keys='Application.reviewed_by', backref='reviewer', lazy=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}"
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'

class SiteSettings(db.Model):
    """Global site settings controlled by admin (admissions banner, etc.)"""
    id = db.Column(db.Integer, primary_key=True)

    # Admissions control
    admissions_open = db.Column(db.Boolean, default=False, nullable=False)
    intake_semester = db.Column(db.String(50), default='Fall 2025')
    application_deadline = db.Column(db.Date)

    # Banner customization
    banner_title = db.Column(db.String(200))
    banner_message = db.Column(db.Text)
    banner_enabled = db.Column(db.Boolean, default=True)

    # Metadata
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<SiteSettings admissions_open={self.admissions_open}>'


class Course(db.Model):
    """Course model for managing educational programs"""
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer, nullable=False)
    duration_hours = db.Column(db.Integer, nullable=False)
    fee_hkd = db.Column(db.Numeric(10, 2), nullable=False)
    cef_eligible = db.Column(db.Boolean, default=False)
    cef_fee_hkd = db.Column(db.Numeric(10, 2))
    
    # Course details
    max_students = db.Column(db.Integer, default=20)
    min_students = db.Column(db.Integer, default=8)
    language = db.Column(db.String(50), default='English')
    level = db.Column(db.String(50))  # Beginner, Intermediate, Advanced
    prerequisites = db.Column(db.Text)
    
    # Course content
    learning_outcomes = db.Column(db.Text)
    course_content = db.Column(db.Text)
    assessment_method = db.Column(db.Text)
    certification = db.Column(db.String(200))
    
    # Status and visibility
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(100))  # Culinary, Business, Professional, etc.
    delivery_mode = db.Column(db.String(20), default='offline')  # online, offline, hybrid
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schedules = db.relationship('CourseSchedule', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='course', lazy=True, cascade='all, delete-orphan')
    
    @property
    def current_enrollments(self):
        """Get current active enrollments"""
        return Enrollment.query.filter_by(course_id=self.id, status='active').count()
    
    @property
    def available_spots(self):
        """Calculate available spots"""
        return max(0, self.max_students - self.current_enrollments)
    
    @property
    def is_full(self):
        """Check if course is full"""
        return self.current_enrollments >= self.max_students
    
    @property
    def total_fee(self):
        """Get total course fee as integer for calculations"""
        return int(self.fee_hkd)
    
    @property
    def is_cef_eligible(self):
        """Check if course is CEF eligible"""
        return self.cef_eligible
    
    # Phase 2 LMS Properties
    @property
    def total_modules(self):
        """Get total number of modules in this course"""
        return len(self.modules)
    
    @property
    def published_modules(self):
        """Get only published modules"""
        return [module for module in self.modules if module.is_published]
    
    @property
    def total_lessons(self):
        """Get total number of lessons across all modules"""
        return sum(module.lesson_count for module in self.modules)
    
    @property
    def estimated_duration_hours(self):
        """Calculate total estimated learning time in hours"""
        total_minutes = sum(module.total_duration_minutes for module in self.modules)
        return round(total_minutes / 60, 1) if total_minutes > 0 else 0
    
    @property
    def has_content(self):
        """Check if course has learning content (modules and lessons)"""
        return self.total_modules > 0 and self.total_lessons > 0
    
    def __repr__(self):
        return f'<Course {self.course_code}: {self.title}>'


class CourseSchedule(db.Model):
    """Course schedule for specific course runs"""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Schedule details
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200))
    instructor = db.Column(db.String(100))
    
    # Registration periods
    registration_start = db.Column(db.Date, nullable=False)
    registration_end = db.Column(db.Date, nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, completed, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_registration_open(self):
        """Check if registration is currently open"""
        today = datetime.now().date()
        return (self.registration_start <= today <= self.registration_end and 
                self.is_active and self.status == 'upcoming')
    
    def __repr__(self):
        return f'<Schedule {self.course_id}: {self.start_date}>'


class Application(db.Model):
    """Course application model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('course_schedule.id'))
    
    # Application details
    education_level = db.Column(db.String(100))
    work_experience = db.Column(db.Text)
    motivation = db.Column(db.Text)
    special_requirements = db.Column(db.Text)
    how_did_you_hear = db.Column(db.String(200))
    
    # CEF details (if applicable)
    cef_application = db.Column(db.Boolean, default=False)
    hkid_number = db.Column(db.String(20))
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, waitlist
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_notes = db.Column(db.Text)
    
    # Payment tracking
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_method = db.Column(db.String(50))
    payment_reference = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schedule = db.relationship('CourseSchedule', backref='applications')
    
    def __repr__(self):
        return f'<Application {self.id}: {self.course.title} - {self.applicant.full_name}>'


class Consultation(db.Model):
    """Model for managing consultation bookings"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Contact Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    # Consultation Details
    consultation_type = db.Column(db.String(50), nullable=False)  # 'course_info', 'career_guidance', 'admission_help'
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, default=30)  # Duration in minutes
    
    # Course Interest (optional)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    
    # Additional Information
    message = db.Column(db.Text)
    special_requirements = db.Column(db.Text)
    
    # Status and Management
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    meeting_link = db.Column(db.String(500))  # For online consultations
    meeting_location = db.Column(db.String(200))  # For in-person consultations
    meeting_type = db.Column(db.String(20), default='online')  # online, in_person
    
    # Staff Assignment
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmation_sent = db.Column(db.DateTime)
    
    # Relationships
    interested_course = db.relationship('Course', backref='consultations', lazy=True)
    assigned_staff = db.relationship('User', backref='assigned_consultations', lazy=True)
    
    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def consultation_datetime(self):
        """Combine date and time"""
        return datetime.combine(self.preferred_date, self.preferred_time)
    
    @property
    def formatted_date(self):
        """Format date for display"""
        return self.preferred_date.strftime('%B %d, %Y')
    
    @property
    def formatted_time(self):
        """Format time for display"""
        return self.preferred_time.strftime('%I:%M %p')
    
    def __repr__(self):
        return f'<Consultation {self.id}: {self.full_name} - {self.consultation_type}>'


class Enrollment(db.Model):
    """Student enrollment in courses"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), unique=True)
    
    # Enrollment details
    enrollment_date = db.Column(db.Date, default=datetime.utcnow().date)
    start_date = db.Column(db.Date)
    expected_completion = db.Column(db.Date)
    actual_completion = db.Column(db.Date)
    
    # Status and progress
    status = db.Column(db.String(20), default='active')  # active, completed, withdrawn, suspended
    attendance_percentage = db.Column(db.Numeric(5, 2), default=0.00)
    final_grade = db.Column(db.String(5))  # A, B, C, D, F
    certificate_issued = db.Column(db.Boolean, default=False)
    certificate_number = db.Column(db.String(50))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    application = db.relationship('Application', backref=db.backref('enrollment', uselist=False))
    
    def __repr__(self):
        return f'<Enrollment {self.user_id} in {self.course_id}>'


# Removed duplicate ContactInquiry model to avoid SQLAlchemy class name conflict.


# ============================================================================
# PHASE 2 LMS MODELS - Learning Content Management System
# ============================================================================

class Module(db.Model):
    """Course modules/chapters for organizing lessons"""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    estimated_hours = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref=db.backref('modules', lazy=True, order_by='Module.order_index'))
    lessons = db.relationship('Lesson', backref='module', lazy=True, order_by='Lesson.order_index', cascade='all, delete-orphan')
    
    @property
    def lesson_count(self):
        """Get total number of lessons in this module"""
        return len(self.lessons)
    
    @property
    def published_lessons(self):
        """Get only published lessons"""
        return [lesson for lesson in self.lessons if lesson.is_published]
    
    @property
    def total_duration_minutes(self):
        """Calculate total duration of all lessons in minutes"""
        return sum(lesson.duration_minutes or 0 for lesson in self.lessons)
    
    def __repr__(self):
        return f'<Module {self.id}: {self.title}>'


class Lesson(db.Model):
    """Individual lessons within modules"""
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50), nullable=False)  # 'video', 'text', 'document', 'quiz', 'assignment'
    
    # Content storage
    content_text = db.Column(db.Text)  # For text-based lessons
    video_url = db.Column(db.String(500))  # For video lessons
    document_path = db.Column(db.String(500))  # For document downloads
    external_url = db.Column(db.String(500))  # For external resources
    
    # Lesson properties
    order_index = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, default=0)
    is_mandatory = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress_records = db.relationship('StudentProgress', backref='lesson', lazy=True, cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='lesson', lazy=True, cascade='all, delete-orphan')
    
    @property
    def completion_rate(self):
        """Calculate percentage of students who completed this lesson"""
        if not self.progress_records:
            return 0
        completed = sum(1 for record in self.progress_records if record.completed)
        return (completed / len(self.progress_records)) * 100
    
    def __repr__(self):
        return f'<Lesson {self.id}: {self.title}>'


class StudentProgress(db.Model):
    """Track student progress through lessons"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    
    # Progress tracking
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)
    time_spent_minutes = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Study analytics
    access_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)  # Student notes for this lesson
    bookmarked = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', backref='learning_progress')
    enrollment = db.relationship('Enrollment', backref='progress_records')
    
    # Ensure unique progress record per student/lesson/enrollment
    __table_args__ = (db.UniqueConstraint('student_id', 'lesson_id', 'enrollment_id'),)
    
    def mark_complete(self):
        """Mark lesson as completed"""
        if not self.completed:
            self.completed = True
            self.completion_date = datetime.utcnow()
            db.session.commit()
    
    def add_time_spent(self, minutes):
        """Add time spent on this lesson"""
        self.time_spent_minutes += minutes
        self.last_accessed = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Progress: Student {self.student_id} - Lesson {self.lesson_id}>'


# ============================================================================
# PHASE 2 ASSESSMENT MODELS - Quiz and Testing System  
# ============================================================================

class Quiz(db.Model):
    """Quiz assessments for lessons"""
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)  # Can be standalone
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Quiz details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    
    # Quiz settings
    time_limit_minutes = db.Column(db.Integer)  # NULL means no time limit
    attempts_allowed = db.Column(db.Integer, default=1)
    passing_score = db.Column(db.Float, default=70.0)  # Percentage
    randomize_questions = db.Column(db.Boolean, default=False)
    show_results_immediately = db.Column(db.Boolean, default=True)
    
    # Status
    is_published = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref='quizzes')
    questions = db.relationship('Question', backref='quiz', lazy=True, order_by='Question.order_index', cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total_points(self):
        """Calculate total possible points for this quiz"""
        return sum(question.points for question in self.questions)
    
    @property
    def question_count(self):
        """Get total number of questions"""
        return len(self.questions)
    
    def __repr__(self):
        return f'<Quiz {self.id}: {self.title}>'


class Question(db.Model):
    """Quiz questions"""
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    # Question content
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'multiple_choice', 'true_false', 'essay', 'short_answer'
    order_index = db.Column(db.Integer, nullable=False)
    
    # Scoring
    points = db.Column(db.Float, default=1.0)
    
    # Multiple choice options (stored as JSON)
    options = db.Column(db.JSON)  # For multiple choice: [{"id": "A", "text": "Option A"}, ...]
    correct_answer = db.Column(db.Text)  # Correct answer(s)
    explanation = db.Column(db.Text)  # Explanation shown after answer
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_answers = db.relationship('StudentAnswer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_type}>'


class QuizAttempt(db.Model):
    """Student quiz attempts"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    
    # Attempt details
    attempt_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, etc.
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)
    time_spent_minutes = db.Column(db.Integer)
    
    # Results
    score = db.Column(db.Float)  # Points earned
    percentage = db.Column(db.Float)  # Percentage score
    passed = db.Column(db.Boolean)
    is_submitted = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', backref='quiz_attempts')
    enrollment = db.relationship('Enrollment', backref='quiz_attempts')
    answers = db.relationship('StudentAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    
    def calculate_score(self):
        """Calculate and update the score for this attempt"""
        total_points = 0
        earned_points = 0
        
        for answer in self.answers:
            total_points += answer.question.points
            earned_points += answer.points_earned or 0
        
        self.score = earned_points
        self.percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        self.passed = self.percentage >= self.quiz.passing_score
        
        db.session.commit()
        return self.percentage
    
    def __repr__(self):
        return f'<QuizAttempt {self.id}: Student {self.student_id} - Quiz {self.quiz_id}>'


class StudentAnswer(db.Model):
    """Individual student answers to quiz questions"""
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    # Answer content
    answer_text = db.Column(db.Text)  # Student's answer
    selected_option = db.Column(db.String(10))  # For multiple choice (A, B, C, D)
    
    # Grading
    is_correct = db.Column(db.Boolean)
    points_earned = db.Column(db.Float, default=0.0)
    instructor_feedback = db.Column(db.Text)  # Manual feedback for essay questions
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def auto_grade(self):
        """Automatically grade objective questions"""
        if self.question.question_type in ['multiple_choice', 'true_false']:
            if self.question.question_type == 'multiple_choice':
                self.is_correct = self.selected_option == self.question.correct_answer
            else:  # true_false
                self.is_correct = self.answer_text.lower() == self.question.correct_answer.lower()
                
            self.points_earned = self.question.points if self.is_correct else 0
            db.session.commit()
    
    def __repr__(self):
        return f'<StudentAnswer {self.id}: Attempt {self.attempt_id} - Question {self.question_id}>'


# Assignment Management Models

class Assignment(db.Model):
    """Assignment model for course assignments and homework"""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assignment_type = db.Column(db.String(50), default='homework')  # homework, project, essay, lab
    max_points = db.Column(db.Integer, default=100)
    due_date = db.Column(db.DateTime)
    instructions = db.Column(db.Text)
    attachment_path = db.Column(db.String(500))  # For assignment files/resources
    is_published = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref='assignments')
    submissions = db.relationship('AssignmentSubmission', backref='assignment', cascade='all, delete-orphan')
    
    @property
    def is_overdue(self):
        """Check if assignment is past due date"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date
    
    @property
    def days_until_due(self):
        """Calculate days until due date"""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.utcnow()
        return delta.days if delta.days >= 0 else 0
    
    @property
    def submission_count(self):
        """Count total submissions"""
        return len(self.submissions)
    
    def get_student_submission(self, student_id):
        """Get specific student's submission"""
        return AssignmentSubmission.query.filter_by(
            assignment_id=self.id,
            student_id=student_id
        ).first()
    
    def __repr__(self):
        return f'<Assignment {self.id}: {self.title}>'


class AssignmentSubmission(db.Model):
    """Student assignment submissions"""
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    
    # Submission content
    submission_text = db.Column(db.Text)
    attachment_path = db.Column(db.String(500))  # For uploaded files
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Grading
    grade = db.Column(db.Numeric(5, 2))  # Grade out of max_points
    feedback = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted')  # submitted, graded, returned
    is_late = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', backref='assignment_submissions')
    enrollment = db.relationship('Enrollment', backref='assignment_submissions')
    
    @property
    def grade_percentage(self):
        """Calculate grade as percentage"""
        if not self.grade or not self.assignment.max_points:
            return None
        return (float(self.grade) / self.assignment.max_points) * 100
    
    @property
    def grade_letter(self):
        """Convert grade to letter grade"""
        percentage = self.grade_percentage
        if percentage is None:
            return 'N/A'
        elif percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def __repr__(self):
        return f'<AssignmentSubmission {self.id}: Student {self.student_id} - Assignment {self.assignment_id}>'


class ClassSchedule(db.Model):
    """Class schedule and timetable"""
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    class_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200))
    instructor = db.Column(db.String(100))
    topic = db.Column(db.String(300))
    description = db.Column(db.Text)
    class_type = db.Column(db.String(50), default='lecture')  # lecture, lab, seminar, exam
    max_participants = db.Column(db.Integer, default=20)
    is_cancelled = db.Column(db.Boolean, default=False)
    online_meeting_url = db.Column(db.String(500))
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref='class_schedules')
    
    @property
    def is_today(self):
        """Check if class is today"""
        return self.class_date.date() == datetime.utcnow().date()
    
    @property
    def is_upcoming(self):
        """Check if class is in the future"""
        return self.class_date > datetime.utcnow()
    
    @property
    def time_until_class(self):
        """Calculate time until class starts"""
        if not self.is_upcoming:
            return None
        delta = self.class_date - datetime.utcnow()
        return delta
    
    @property
    def duration_minutes(self):
        """Calculate class duration in minutes"""
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        delta = end_datetime - start_datetime
        return int(delta.total_seconds() / 60)
    
    @property
    def duration_hours(self):
        """Calculate class duration in hours"""
        return round(self.duration_minutes / 60, 1)
    
    @property
    def is_tomorrow(self):
        """Check if class is tomorrow"""
        from datetime import timedelta
        tomorrow = datetime.utcnow().date() + timedelta(days=1)
        return self.class_date.date() == tomorrow
    
    @property
    def days_until(self):
        """Calculate days until class"""
        delta = self.class_date.date() - datetime.utcnow().date()
        return delta.days
    
    def __repr__(self):
        return f'<ClassSchedule {self.id}: {self.course.course_code} on {self.class_date.strftime("%Y-%m-%d")}>'


# ============================================================================
# PHASE 2 ENHANCEMENTS: Communication & Tracking Features
# ============================================================================

class Notification(db.Model):
    """Notification system for user alerts and updates"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Notification content
    type = db.Column(db.String(50), nullable=False)  # assignment, grade, schedule, application, course, message, announcement
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link_url = db.Column(db.String(500))  # Optional link to related content
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    # Metadata
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    category = db.Column(db.String(50))  # For filtering/grouping
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    @property
    def time_ago(self):
        """Human-readable time since notification was created"""
        delta = datetime.utcnow() - self.created_at
        
        if delta.days > 365:
            return f"{delta.days // 365} year{'s' if delta.days // 365 > 1 else ''} ago"
        elif delta.days > 30:
            return f"{delta.days // 30} month{'s' if delta.days // 30 > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hour{'s' if delta.seconds // 3600 > 1 else ''} ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60} minute{'s' if delta.seconds // 60 > 1 else ''} ago"
        else:
            return "Just now"
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.type} for User {self.user_id}>'


class Message(db.Model):
    """Direct messaging system for student-instructor-admin communication"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Sender and recipient
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Message content
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    # Threading (for replies)
    parent_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    
    # Status tracking
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    is_deleted_by_sender = db.Column(db.Boolean, default=False)
    is_deleted_by_recipient = db.Column(db.Boolean, default=False)
    
    # Priority and categorization
    priority = db.Column(db.String(20), default='normal')  # low, normal, high
    category = db.Column(db.String(50))  # academic, administrative, technical, general
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    parent_message = db.relationship('Message', remote_side=[id], backref='replies')
    attachments = db.relationship('MessageAttachment', backref='message', lazy=True, cascade='all, delete-orphan')
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()
    
    @property
    def time_ago(self):
        """Human-readable time since message was sent"""
        delta = datetime.utcnow() - self.created_at
        
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hour{'s' if delta.seconds // 3600 > 1 else ''} ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60} minute{'s' if delta.seconds // 60 > 1 else ''} ago"
        else:
            return "Just now"
    
    @property
    def has_attachments(self):
        """Check if message has attachments"""
        return len(self.attachments) > 0
    
    @property
    def is_thread(self):
        """Check if this is the start of a thread"""
        return self.parent_message_id is None and len(self.replies) > 0
    
    def __repr__(self):
        return f'<Message {self.id}: From {self.sender_id} to {self.recipient_id}>'


class MessageAttachment(db.Model):
    """File attachments for messages"""
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    
    # File information
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # Size in bytes
    mime_type = db.Column(db.String(100))
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def file_size_formatted(self):
        """Return human-readable file size"""
        if not self.file_size:
            return "Unknown"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def __repr__(self):
        return f'<MessageAttachment {self.id}: {self.original_filename}>'


class Attendance(db.Model):
    """Attendance tracking for class sessions"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Student and class information
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_schedule_id = db.Column(db.Integer, db.ForeignKey('class_schedule.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Attendance details
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='present')  # present, absent, late, excused
    
    # Additional information
    marked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Instructor/Admin who marked
    check_in_time = db.Column(db.DateTime)
    notes = db.Column(db.Text)  # Reason for absence, late arrival, etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='attendance_records')
    class_schedule = db.relationship('ClassSchedule', backref='attendance_records')
    course = db.relationship('Course', backref='attendance_records')
    marker = db.relationship('User', foreign_keys=[marked_by])
    
    @property
    def is_present(self):
        """Check if student was present"""
        return self.status == 'present'
    
    @property
    def is_absent(self):
        """Check if student was absent"""
        return self.status == 'absent'
    
    @property
    def is_late(self):
        """Check if student was late"""
        return self.status == 'late'
    
    @property
    def is_excused(self):
        """Check if absence was excused"""
        return self.status == 'excused'
    
    def __repr__(self):
        return f'<Attendance {self.id}: Student {self.student_id} - {self.status}>'


class Certificate(db.Model):
    """Digital certificates for course completion"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Student and course information
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'))
    
    # Certificate details
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    verification_code = db.Column(db.String(100), unique=True, nullable=False)
    
    # Completion information
    issue_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    completion_date = db.Column(db.Date, nullable=False)
    final_grade = db.Column(db.Numeric(5, 2))  # Percentage or GPA
    grade_letter = db.Column(db.String(5))  # A, B+, etc.
    
    # Certificate file
    pdf_path = db.Column(db.String(500))
    pdf_generated_at = db.Column(db.DateTime)
    
    # Verification and validation
    is_verified = db.Column(db.Boolean, default=True)
    issued_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who issued
    revoked = db.Column(db.Boolean, default=False)
    revoked_at = db.Column(db.DateTime)
    revoked_reason = db.Column(db.Text)
    
    # Additional details
    honors = db.Column(db.String(100))  # Distinction, Merit, Pass
    attendance_percentage = db.Column(db.Numeric(5, 2))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='certificates')
    course = db.relationship('Course', backref='certificates')
    enrollment = db.relationship('Enrollment', backref='certificate', uselist=False)
    issuer = db.relationship('User', foreign_keys=[issued_by])
    
    @property
    def is_valid(self):
        """Check if certificate is valid (not revoked)"""
        return self.is_verified and not self.revoked
    
    @property
    def display_grade(self):
        """Return formatted grade display"""
        if self.grade_letter:
            return f"{self.grade_letter} ({self.final_grade}%)"
        elif self.final_grade:
            return f"{self.final_grade}%"
        return "Pass"
    
    @property
    def verification_url(self):
        """Generate verification URL"""
        from flask import url_for
        return url_for('verify_certificate', code=self.verification_code, _external=True)
    
    def generate_certificate_number(self):
        """Generate unique certificate number"""
        import random
        import string
        year = datetime.utcnow().year
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"PENASIA-{year}-{random_str}"
    
    def generate_verification_code(self):
        """Generate unique verification code"""
        import hashlib
        import uuid
        unique_string = f"{self.user_id}{self.course_id}{uuid.uuid4()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:32]
    
    def __repr__(self):
        return f'<Certificate {self.certificate_number}: User {self.user_id} - Course {self.course_id}>'


class Announcement(db.Model):
    """System and course announcements"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Announcement content
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Author and targeting
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))  # Null = institution-wide
    target_audience = db.Column(db.String(50), default='all')  # all, students, instructors, specific_course
    
    # Display settings
    is_pinned = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    category = db.Column(db.String(50))  # academic, administrative, event, deadline
    
    # Scheduling
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # Optional expiration
    
    # Status
    is_published = db.Column(db.Boolean, default=True)
    is_draft = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='announcements')
    course = db.relationship('Course', backref='announcements')
    
    @property
    def is_active(self):
        """Check if announcement is currently active"""
        now = datetime.utcnow()
        if not self.is_published or self.is_draft:
            return False
        if self.expires_at and self.expires_at < now:
            return False
        return True
    
    @property
    def is_expired(self):
        """Check if announcement has expired"""
        return self.expires_at and self.expires_at < datetime.utcnow()
    
    @property
    def time_ago(self):
        """Human-readable time since announcement"""
        delta = datetime.utcnow() - self.published_at
        
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hour{'s' if delta.seconds // 3600 > 1 else ''} ago"
        else:
            return f"{delta.seconds // 60} minute{'s' if delta.seconds // 60 > 1 else ''} ago"
    
    def __repr__(self):
        return f'<Announcement {self.id}: {self.title}>'


class ContactInquiry(db.Model):
    """Contact form inquiries"""
    __tablename__ = 'contact_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    program_interest = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    subscribe_newsletter = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='new')  # new, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_notes = db.Column(db.Text)
    
    # Relationship
    resolved_by = db.relationship('User', backref='resolved_inquiries', foreign_keys=[resolved_by_id])
    
    def __repr__(self):
        return f'<ContactInquiry {self.id}: {self.first_name} {self.last_name} - {self.subject}>'
