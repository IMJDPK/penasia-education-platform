from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import os
from datetime import datetime
from markupsafe import Markup

# Import models and forms
from models import db, User, Course, CourseSchedule, Application, Enrollment, ContactInquiry, Consultation, Module, Lesson, StudentProgress, Quiz, Question, QuizAttempt, StudentAnswer, Assignment, AssignmentSubmission, ClassSchedule, Notification, Message, MessageAttachment, Attendance, Certificate, Announcement
from forms import LoginForm, RegistrationForm, CourseApplicationForm, ConsultationBookingForm, AssignmentSubmissionForm, AssignmentSubmissionForm, ContactForm, CourseForm
from email_service import email_service
from payment_service import payment_processor
from certificate_service import certificate_generator

app = Flask(__name__)
app.secret_key = 'penasia-secret-key-2025'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "penasia.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Custom Jinja2 filters
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks"""
    if text:
        return Markup(text.replace('\n', '<br>\n'))
    return text

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'  # Will be set after we define the route
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Inject SiteSettings into all templates
@app.context_processor
def inject_site_settings():
    try:
        from models import SiteSettings
        settings = SiteSettings.query.first()
        return dict(site_settings=settings)
    except Exception:
        return dict(site_settings=None)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()
    # Ensure a SiteSettings row exists for admissions/banner controls
    try:
        from models import SiteSettings
        if not SiteSettings.query.first():
            db.session.add(SiteSettings())
            db.session.commit()
    except Exception:
        pass
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(email='admin@penasia.edu.hk').first()
    if not admin:
        admin = User(
            email='admin@penasia.edu.hk',
            first_name='Admin',
            last_name='User',
            role='admin',
            is_active=True,
            email_verified=True
        )
        admin.set_password('admin123')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
        print("Created admin user: admin@penasia.edu.hk / admin123")

# Routes
@app.route('/')
def index():
    # Get featured courses from database
    featured_courses = Course.query.filter_by(is_featured=True, is_active=True).limit(3).all()
    return render_template('index.html', featured_courses=featured_courses)

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    from forms import LoginForm
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            return redirect(next_page)
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

# Add alias route for /auth/login to match template links
@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    return login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    from forms import RegistrationForm
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            role='student',
            email_verified=False  # Require email verification
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Send verification email
        try:
            verification_link = url_for('verify_email', user_id=user.id, _external=True)
            email_service.send_email_verification(user, verification_link)
            flash('Registration successful! Please check your email to verify your account.', 'info')
        except Exception as e:
            print(f"Email verification error: {e}")
            # Allow login without email verification if service fails
            user.email_verified = True
            db.session.commit()
            flash('Registration successful! You can now log in. (Email verification skipped)', 'warning')
        
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/verify_email/<int:user_id>')
def verify_email(user_id):
    """Verify user email"""
    user = User.query.get_or_404(user_id)
    
    if user.email_verified:
        flash('Your email is already verified!', 'info')
        return redirect(url_for('login'))
    
    try:
        user.email_verified = True
        db.session.commit()
        flash('Email verified successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        print(f"Email verification error: {e}")
        flash('Error verifying email. Please try again or contact support.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    # Student dashboard
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    
    # Get assignments and schedules for enrolled courses
    from models import Assignment, ClassSchedule, AssignmentSubmission
    from sqlalchemy import and_
    from datetime import datetime, timedelta
    
    enrolled_course_ids = [e.course_id for e in enrollments]
    
    # Upcoming assignments (due within next 30 days)
    upcoming_assignments = Assignment.query.filter(
        and_(
            Assignment.course_id.in_(enrolled_course_ids),
            Assignment.due_date > datetime.utcnow(),
            Assignment.due_date <= datetime.utcnow() + timedelta(days=30),
            Assignment.is_published == True
        )
    ).order_by(Assignment.due_date).limit(5).all()
    
    # Upcoming classes (next 7 days)
    upcoming_classes = ClassSchedule.query.filter(
        and_(
            ClassSchedule.course_id.in_(enrolled_course_ids),
            ClassSchedule.class_date > datetime.utcnow(),
            ClassSchedule.class_date <= datetime.utcnow() + timedelta(days=7),
            ClassSchedule.is_cancelled == False
        )
    ).order_by(ClassSchedule.class_date).limit(10).all()
    
    # Assignment submissions for grade tracking
    my_submissions = AssignmentSubmission.query.filter_by(student_id=current_user.id).all()
    
    return render_template('dashboard/student.html', 
                         enrollments=enrollments, 
                         applications=applications,
                         upcoming_assignments=upcoming_assignments,
                         upcoming_classes=upcoming_classes,
                         my_submissions=my_submissions)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Student profile view/edit page"""
    # Admins should use admin panel for their settings
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    from forms import ProfileForm
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        # Update basic profile fields
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.address = form.address.data
        current_user.emergency_contact_name = form.emergency_contact_name.data
        current_user.emergency_contact_phone = form.emergency_contact_phone.data

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile'))

    return render_template('dashboard/profile.html', form=form)

@app.route('/assignments/<int:assignment_id>')
@login_required
def assignment_detail(assignment_id):
    """View assignment details"""
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Check if student is enrolled in the course
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=assignment.course_id
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get student's submission if exists
    submission = assignment.get_student_submission(current_user.id)
    
    return render_template('assignments/detail.html', 
                         assignment=assignment, 
                         enrollment=enrollment,
                         submission=submission)

@app.route('/assignments/<int:assignment_id>/submit', methods=['GET', 'POST'])
@login_required  
def submit_assignment(assignment_id):
    """Submit assignment"""
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=assignment.course_id
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if already submitted
    existing_submission = assignment.get_student_submission(current_user.id)
    if existing_submission:
        flash('You have already submitted this assignment.', 'warning')
        return redirect(url_for('assignment_detail', assignment_id=assignment_id))
    
    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        
        if not submission_text:
            flash('Please provide your assignment submission.', 'error')
            return redirect(url_for('submit_assignment', assignment_id=assignment_id))
        
        # Create submission
        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            student_id=current_user.id,
            enrollment_id=enrollment.id,
            submission_text=submission_text,
            is_late=assignment.is_overdue
        )
        
        db.session.add(submission)
        db.session.commit()
        
        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('assignment_detail', assignment_id=assignment_id))
    
    return render_template('assignments/submit.html', assignment=assignment)

@app.route('/schedule')
@login_required
def class_schedule():
    """View class schedule for enrolled courses"""
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    enrolled_course_ids = [e.course_id for e in enrollments]
    
    from datetime import datetime, timedelta
    
    # Get schedule for next 30 days
    end_date = datetime.utcnow() + timedelta(days=30)
    
    classes = ClassSchedule.query.filter(
        ClassSchedule.course_id.in_(enrolled_course_ids),
        ClassSchedule.class_date >= datetime.utcnow(),
        ClassSchedule.class_date <= end_date,
        ClassSchedule.is_cancelled == False
    ).order_by(ClassSchedule.class_date).all()
    
    return render_template('schedule/student.html', classes=classes, enrollments=enrollments)

@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    """Display course detail page"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user is logged in and has already applied
    has_applied = False
    if current_user.is_authenticated:
        has_applied = Application.query.filter_by(
            user_id=current_user.id,
            course_id=course_id
        ).first() is not None
    
    return render_template('courses/detail.html', course=course, has_applied=has_applied)


@app.route('/courses/<int:course_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_course(course_id):
    """Apply for a specific course"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user already has an application for this course
    existing_application = Application.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing_application:
        flash('You have already applied for this course.', 'info')
        return redirect(url_for('student_dashboard'))
    
    form = CourseApplicationForm()
    
    # Populate form with user data
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.address.data = current_user.address
    
    if form.validate_on_submit():
        try:
            # Create new application
            application = Application()
            application.user_id = current_user.id
            application.course_id = course_id
            application.education_level = form.education_level.data
            application.work_experience = form.work_experience.data
            application.motivation = form.motivation.data
            application.special_requirements = form.special_requirements.data
            application.how_did_you_hear = form.how_did_you_hear.data
            application.cef_application = form.cef_application.data
            application.hkid_number = form.hkid_number.data if form.cef_application.data else None
            application.payment_method = form.payment_method.data
            application.status = 'pending'
            application.submitted_at = datetime.utcnow()
            
            db.session.add(application)
            db.session.commit()
            
            # Create notifications for all admin users
            admin_users = User.query.filter_by(role='admin').all()
            for admin in admin_users:
                notification = Notification(
                    user_id=admin.id,
                    type='application',
                    title=f'New Application: {course.name}',
                    message=f'{current_user.first_name} {current_user.last_name} ({current_user.email}) has submitted an application for {course.name}. Phone: {current_user.phone or "N/A"}',
                    link_url=f'/admin/applications',
                    priority='high'
                )
                db.session.add(notification)
            
            db.session.commit()
            
            # Send confirmation email
            try:
                email_service.send_application_confirmation(current_user, course, application)
            except Exception as e:
                print(f"Error sending email: {e}")
            
            flash(f'Your application for {course.name} has been submitted successfully! We will review it within 3-5 business days and send you an email with the decision.', 'success')
            return redirect(url_for('student_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your application. Please try again.', 'error')
            print(f"Error submitting application: {e}")
    
    return render_template('courses/apply.html', form=form, course=course)


@app.route('/payment/<int:application_id>')
@login_required
def payment_checkout(application_id):
    """Payment checkout page"""
    application = Application.query.get_or_404(application_id)
    
    # Verify user owns this application
    if application.user_id != current_user.id:
        flash('Unauthorized access to payment page.', 'error')
        return redirect(url_for('student_dashboard'))
    
    # Verify application is approved
    if application.status != 'approved':
        flash('Payment is only available for approved applications.', 'error')
        return redirect(url_for('student_dashboard'))
    
    course = application.course
    payment_method = application.payment_method or 'credit_card'
    
    # Generate payment reference and get instructions
    payment_data = payment_processor.process_payment(
        current_user, course, course.fee, payment_method, application_id
    )
    
    instructions = payment_processor.get_payment_instructions(
        payment_method, course.fee, payment_data['reference']
    )
    
    return render_template('payment/checkout.html', 
                         course=course, 
                         application=application,
                         amount=course.fee,
                         payment_method=payment_method,
                         payment_reference=payment_data['reference'],
                         instructions=instructions)


@app.route('/api/process-payment', methods=['POST'])
@login_required
def process_payment_api():
    """API endpoint to process payment with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['reference', 'amount', 'method', 'application_id']):
            return jsonify({'status': 'error', 'message': 'Missing required payment information'}), 400
        
        application_id = data.get('application_id')
        application = Application.query.get_or_404(application_id)
        
        # Verify user owns this application
        if application.user_id != current_user.id:
            return jsonify({'status': 'error', 'message': 'Unauthorized payment attempt'}), 403
        
        # Process payment with validation
        payment_method = data.get('method')
        amount = float(data.get('amount'))
        
        # Validate payment method
        if payment_method not in payment_processor.supported_methods:
            return jsonify({'status': 'error', 'message': f'Invalid payment method: {payment_method}'}), 400
        
        # Process based on payment method
        if payment_method == 'credit_card':
            # For production: integrate with Stripe or similar gateway
            payment_result = {
                'status': 'pending_gateway',
                'message': 'Redirecting to payment gateway...',
                'reference': data.get('reference'),
                'amount': amount,
                'gateway': 'stripe',  # Configure with real Stripe key in production
                'requires_redirect': True
            }
        elif payment_method == 'bank_transfer':
            # Bank transfer: payment pending manual verification
            payment_result = {
                'status': 'pending_verification',
                'message': 'Please complete bank transfer and provide proof',
                'reference': data.get('reference'),
                'amount': amount,
                'bank_account': 'HSBC HK - Account: 123-456789-001',
                'requires_manual_verification': True
            }
        elif payment_method == 'cef':
            # CEF: payment pending verification
            payment_result = {
                'status': 'pending_cef_verification',
                'message': 'CEF application in progress',
                'reference': data.get('reference'),
                'amount': amount,
                'cef_eligible': application.cef_eligible
            }
        elif payment_method == 'installments':
            # Installment: first payment pending
            installment_schedule = payment_processor.calculate_installment_schedule(amount)
            payment_result = {
                'status': 'pending_installment',
                'message': 'Installment plan created',
                'reference': data.get('reference'),
                'amount': amount,
                'installment_schedule': [
                    {
                        'number': item['installment_number'],
                        'amount': item['amount'],
                        'due_date': item['due_date'].isoformat() if hasattr(item['due_date'], 'isoformat') else str(item['due_date'])
                    }
                    for item in installment_schedule
                ]
            }
        else:
            payment_result = {
                'status': 'error',
                'message': 'Payment method not configured'
            }
        
        # Log payment attempt
        print(f"\n[PAYMENT PROCESSING LOG]")
        print(f"User: {current_user.email}")
        print(f"Application: {application_id}")
        print(f"Amount: HK${amount:,.2f}")
        print(f"Method: {payment_method}")
        print(f"Status: {payment_result['status']}")
        print(f"Time: {datetime.utcnow().isoformat()}\n")
        
        return jsonify(payment_result)
    except Exception as e:
        print(f"Payment processing error: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Payment processing error: {str(e)}'}), 400


@app.route('/admin/applications')
@login_required
def admin_applications():
    """Admin applications management page"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Get all applications with course information
    applications = Application.query.join(Course).order_by(Application.created_at.desc()).all()
    
    return render_template('admin/applications.html', applications=applications)


@app.route('/admin/application/<int:application_id>/update', methods=['POST'])
@login_required 
def update_application_status(application_id):
    """Update application status and send notification"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    application = Application.query.get_or_404(application_id)
    new_status = request.form.get('status')
    admin_notes = request.form.get('admin_notes', '')
    
    if new_status in ['pending', 'approved', 'rejected', 'waitlist', 'interview_required']:
        old_status = application.status
        application.status = new_status
        application.reviewed_at = datetime.utcnow()
        application.reviewed_by = current_user.id
        application.admin_notes = admin_notes
        
        db.session.commit()
        
        # Send notification email
        try:
            email_service.send_application_update(
                application.applicant, application.course, application, admin_notes
            )
        except Exception as e:
            print(f"Error sending email notification: {e}")
        
        flash(f'Application status updated from {old_status} to {new_status}. Notification email sent.', 'success')
    else:
        flash('Invalid status provided.', 'error')
    
    return redirect(url_for('admin_applications'))


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Admin statistics
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_courses = Course.query.filter_by(is_active=True).count()
    pending_applications = Application.query.filter_by(status='pending').count()
    recent_applications = Application.query.order_by(Application.created_at.desc()).limit(10).all()
    new_contact_inquiries = ContactInquiry.query.filter_by(status='new').count()
    pending_consultations = Consultation.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_students=total_students,
                         total_courses=total_courses, 
                         pending_applications=pending_applications,
                         recent_applications=recent_applications,
                         new_contact_inquiries=new_contact_inquiries,
                         pending_consultations=pending_consultations)

@app.route('/admin/courses')
@login_required
def admin_courses():
    """Admin course management page"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['GET', 'POST'])
@login_required
def admin_course_add():
    """Add a new course"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    from forms import CourseForm
    form = CourseForm()
    
    if form.validate_on_submit():
        # Check if course code already exists
        existing_course = Course.query.filter_by(course_code=form.course_code.data).first()
        if existing_course:
            flash(f'Course code {form.course_code.data} already exists. Please use a unique code.', 'error')
            return render_template('admin/course_form.html', form=form, mode='add')
        
        course = Course(
            course_code=form.course_code.data,
            title=form.title.data,
            description=form.description.data,
            duration_weeks=form.duration_weeks.data,
            duration_hours=form.duration_hours.data,
            fee_hkd=form.fee_hkd.data,
            cef_eligible=form.cef_eligible.data,
            cef_fee_hkd=form.cef_fee_hkd.data if form.cef_eligible.data else None,
            max_students=form.max_students.data,
            min_students=form.min_students.data,
            language=form.language.data,
            level=form.level.data,
            category=form.category.data,
            prerequisites=form.prerequisites.data,
            learning_outcomes=form.learning_outcomes.data,
            course_content=form.course_content.data,
            assessment_method=form.assessment_method.data,
            certification=form.certification.data,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data
        )
        
        try:
            db.session.add(course)
            db.session.commit()
            flash(f'Course "{course.title}" has been created successfully!', 'success')
            return redirect(url_for('admin_courses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating course: {str(e)}', 'error')
            return render_template('admin/course_form.html', form=form, mode='add')
    
    return render_template('admin/course_form.html', form=form, mode='add')

@app.route('/admin/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_course_edit(course_id):
    """Edit an existing course"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    course = Course.query.get_or_404(course_id)
    from forms import CourseForm
    form = CourseForm(obj=course)
    
    if form.validate_on_submit():
        # Check if course code is being changed and if it conflicts
        if form.course_code.data != course.course_code:
            existing_course = Course.query.filter_by(course_code=form.course_code.data).first()
            if existing_course:
                flash(f'Course code {form.course_code.data} already exists. Please use a unique code.', 'error')
                return render_template('admin/course_form.html', form=form, course=course, mode='edit')
        
        course.course_code = form.course_code.data
        course.title = form.title.data
        course.description = form.description.data
        course.duration_weeks = form.duration_weeks.data
        course.duration_hours = form.duration_hours.data
        course.fee_hkd = form.fee_hkd.data
        course.cef_eligible = form.cef_eligible.data
        course.cef_fee_hkd = form.cef_fee_hkd.data if form.cef_eligible.data else None
        course.max_students = form.max_students.data
        course.min_students = form.min_students.data
        course.language = form.language.data
        course.level = form.level.data
        course.category = form.category.data
        course.prerequisites = form.prerequisites.data
        course.learning_outcomes = form.learning_outcomes.data
        course.course_content = form.course_content.data
        course.assessment_method = form.assessment_method.data
        course.certification = form.certification.data
        course.is_active = form.is_active.data
        course.is_featured = form.is_featured.data
        course.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Course "{course.title}" has been updated successfully!', 'success')
            return redirect(url_for('admin_courses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {str(e)}', 'error')
            return render_template('admin/course_form.html', form=form, course=course, mode='edit')
    
    return render_template('admin/course_form.html', form=form, course=course, mode='edit')

@app.route('/admin/courses/<int:course_id>/delete', methods=['POST'])
@login_required
def admin_course_delete(course_id):
    """Delete a course"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    course = Course.query.get_or_404(course_id)
    
    # Check if course has enrollments
    if course.current_enrollments > 0:
        flash(f'Cannot delete course "{course.title}" because it has active enrollments. Please deactivate it instead.', 'error')
        return redirect(url_for('admin_courses'))
    
    # Check if course has applications
    application_count = Application.query.filter_by(course_id=course_id).count()
    if application_count > 0:
        flash(f'Cannot delete course "{course.title}" because it has {application_count} applications. Please deactivate it instead.', 'error')
        return redirect(url_for('admin_courses'))
    
    try:
        course_title = course.title
        db.session.delete(course)
        db.session.commit()
        flash(f'Course "{course_title}" has been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'error')
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/users')
@login_required
def admin_users():
    """Admin user management page (admins, staff, students)"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Get all users organized by role
    admins = User.query.filter_by(role='admin').all()
    staff = User.query.filter_by(role='staff').all()
    students = User.query.filter_by(role='student').all()
    
    return render_template('admin/users.html', 
                         admins=admins, 
                         staff=staff, 
                         students=students,
                         total_admins=len(admins),
                         total_staff=len(staff),
                         total_students=len(students))

@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def admin_create_user():
    """Create new admin or staff user"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Validate input
        if not email or not first_name or not last_name or not password:
            flash('All fields are required.', 'error')
            return render_template('admin/user_form.html', mode='create')
        
        if role not in ['admin', 'staff']:
            flash('Invalid role selected.', 'error')
            return render_template('admin/user_form.html', mode='create')
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f'User with email {email} already exists.', 'error')
            return render_template('admin/user_form.html', mode='create')
        
        # Create new user
        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True,
            email_verified=True
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'{role.capitalize()} user "{new_user.full_name}" created successfully!', 'success')
            return redirect(url_for('admin_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
            return render_template('admin/user_form.html', mode='create')
    
    return render_template('admin/user_form.html', mode='create')

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    """Edit existing user"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent editing yourself or another admin
    if user.role == 'admin' and user.id != current_user.id:
        flash('Cannot edit other admin accounts.', 'error')
        return redirect(url_for('admin_users'))
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name') or user.first_name
        user.last_name = request.form.get('last_name') or user.last_name
        user.is_active = request.form.get('is_active') == 'on'
        
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
        
        try:
            db.session.commit()
            flash(f'User "{user.full_name}" updated successfully!', 'success')
            return redirect(url_for('admin_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/user_form.html', mode='edit', user=user)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """Delete user"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('Cannot delete your own account.', 'error')
        return redirect(url_for('admin_users'))
    
    # Prevent deleting other admins
    if user.role == 'admin':
        flash('Cannot delete admin accounts.', 'error')
        return redirect(url_for('admin_users'))
    
    user_name = user.full_name
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{user_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/students')
@login_required
def admin_students():
    """Admin student management page"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    students = User.query.filter_by(role='student').all()
    return render_template('admin/students.html', students=students)

@app.route('/admin/reports')
@login_required
def admin_reports():
    """Admin reports and analytics page"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Generate basic statistics for reports
    stats = {
        'total_students': User.query.filter_by(role='student').count(),
        'total_courses': Course.query.count(),
        'total_applications': Application.query.count(),
        'pending_applications': Application.query.filter_by(status='pending').count(),
        'approved_applications': Application.query.filter_by(status='approved').count(),
        'rejected_applications': Application.query.filter_by(status='rejected').count(),
    }
    
    return render_template('admin/reports.html', stats=stats)


@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    """Admin settings page using SiteSettings for admissions/banner control"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))

    from models import SiteSettings
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        settings.admissions_open = request.form.get('admissions_open') == 'on'
        settings.intake_semester = request.form.get('intake_semester') or settings.intake_semester
        settings.banner_title = request.form.get('banner_title') or settings.banner_title
        settings.banner_message = request.form.get('banner_message') or settings.banner_message
        settings.banner_enabled = request.form.get('banner_enabled') == 'on'

        deadline_str = request.form.get('application_deadline')
        if deadline_str:
            try:
                settings.application_deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            except Exception:
                flash('Invalid deadline date. Use YYYY-MM-DD.', 'error')

        settings.updated_by = current_user.id
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin_settings'))

    return render_template('admin/settings.html', settings=settings)


@app.route('/admin/backup')
@login_required
def admin_backup():
    """Admin backup and database management page"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Database statistics
    db_stats = {
        'users': User.query.count(),
        'courses': Course.query.count(),
        'enrollments': Enrollment.query.count(),
        'applications': Application.query.count(),
        'assignments': Assignment.query.count(),
        'quizzes': Quiz.query.count(),
        'messages': Message.query.count(),
        'notifications': Notification.query.count(),
        'certificates': Certificate.query.count(),
        'attendance_records': Attendance.query.count(),
    }
    
    return render_template('admin/backup.html', db_stats=db_stats)


# ============================================================================
# PHASE 2B: ADMIN CONTENT MANAGEMENT ROUTES
# ============================================================================

@app.route('/admin/courses/<int:course_id>/content')
@login_required
def admin_course_content(course_id):
    """Admin interface for managing course content (modules and lessons)"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    course = Course.query.get_or_404(course_id)
    modules = Module.query.filter_by(course_id=course_id).order_by(Module.order_index).all()
    
    return render_template('admin/course_content.html', course=course, modules=modules)


@app.route('/admin/courses/<int:course_id>/modules/add', methods=['GET', 'POST'])
@login_required
def admin_add_module(course_id):
    """Add new module to a course"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        from models import Module
        
        # Get the highest order_index for this course and add 1
        max_order = db.session.query(db.func.max(Module.order_index)).filter_by(course_id=course_id).scalar() or 0
        
        module = Module(
            course_id=course_id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            order_index=max_order + 1,
            is_published=request.form.get('is_published') == 'on',
            estimated_hours=int(request.form.get('estimated_hours', 0))
        )
        
        db.session.add(module)
        db.session.commit()
        
        flash(f'Module "{module.title}" added successfully!', 'success')
        return redirect(url_for('admin_course_content', course_id=course_id))
    
    return render_template('admin/add_module.html', course=course)


@app.route('/admin/modules/<int:module_id>/lessons/add', methods=['GET', 'POST'])
@login_required
def admin_add_lesson(module_id):
    """Add new lesson to a module"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    module = Module.query.get_or_404(module_id)
    
    if request.method == 'POST':
        from models import Lesson
        
        # Get the highest order_index for this module and add 1
        max_order = db.session.query(db.func.max(Lesson.order_index)).filter_by(module_id=module_id).scalar() or 0
        
        lesson = Lesson(
            module_id=module_id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            content_type=request.form.get('content_type'),
            order_index=max_order + 1,
            duration_minutes=int(request.form.get('duration_minutes', 0)),
            is_mandatory=request.form.get('is_mandatory') == 'on',
            is_published=request.form.get('is_published') == 'on'
        )
        
        # Handle different content types
        if lesson.content_type == 'text':
            lesson.content_text = request.form.get('content_text')
        elif lesson.content_type == 'video':
            lesson.video_url = request.form.get('video_url')
        elif lesson.content_type == 'document':
            lesson.document_path = request.form.get('document_path')
        elif lesson.content_type == 'external':
            lesson.external_url = request.form.get('external_url')
        
        db.session.add(lesson)
        db.session.commit()
        
        flash(f'Lesson "{lesson.title}" added successfully!', 'success')
        return redirect(url_for('admin_course_content', course_id=module.course_id))
    
    return render_template('admin/add_lesson.html', module=module)


@app.route('/admin/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_lesson(lesson_id):
    """Edit existing lesson"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if request.method == 'POST':
        lesson.title = request.form.get('title')
        lesson.description = request.form.get('description')
        lesson.content_type = request.form.get('content_type')
        lesson.duration_minutes = int(request.form.get('duration_minutes', 0))
        lesson.is_mandatory = request.form.get('is_mandatory') == 'on'
        lesson.is_published = request.form.get('is_published') == 'on'
        
        # Handle different content types
        if lesson.content_type == 'text':
            lesson.content_text = request.form.get('content_text')
            lesson.video_url = None
            lesson.document_path = None
            lesson.external_url = None
        elif lesson.content_type == 'video':
            lesson.video_url = request.form.get('video_url')
            lesson.content_text = None
            lesson.document_path = None
            lesson.external_url = None
        elif lesson.content_type == 'document':
            lesson.document_path = request.form.get('document_path')
            lesson.content_text = None
            lesson.video_url = None
            lesson.external_url = None
        elif lesson.content_type == 'external':
            lesson.external_url = request.form.get('external_url')
            lesson.content_text = None
            lesson.video_url = None
            lesson.document_path = None
        
        db.session.commit()
        
        flash(f'Lesson "{lesson.title}" updated successfully!', 'success')
        return redirect(url_for('admin_course_content', course_id=lesson.module.course_id))
    
    return render_template('admin/edit_lesson.html', lesson=lesson)


@app.route('/admin/modules/<int:module_id>/delete', methods=['POST'])
@login_required
def admin_delete_module(module_id):
    """Delete a module and all its lessons"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    module = Module.query.get_or_404(module_id)
    course_id = module.course_id
    module_title = module.title
    
    db.session.delete(module)
    db.session.commit()
    
    flash(f'Module "{module_title}" and all its lessons have been deleted.', 'success')
    return redirect(url_for('admin_course_content', course_id=course_id))


@app.route('/admin/lessons/<int:lesson_id>/delete', methods=['POST'])
@login_required
def admin_delete_lesson(lesson_id):
    """Delete a lesson"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    lesson = Lesson.query.get_or_404(lesson_id)
    course_id = lesson.module.course_id
    lesson_title = lesson.title
    
    db.session.delete(lesson)
    db.session.commit()
    
    flash(f'Lesson "{lesson_title}" has been deleted.', 'success')
    return redirect(url_for('admin_course_content', course_id=course_id))


# ============================================================================
# END PHASE 2B ROUTES
# ============================================================================

# ============================================================================
# PHASE 2C: STUDENT LEARNING PORTAL ROUTES
# ============================================================================

@app.route('/learn/courses/<int:course_id>')
@login_required
def student_course_portal(course_id):
    """Student learning portal for enrolled courses"""
    course = Course.query.get_or_404(course_id)
    
    # Check if student is enrolled in this course
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id, 
        course_id=course_id, 
        status='active'
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get published modules and lessons
    modules = Module.query.filter_by(
        course_id=course_id, 
        is_published=True
    ).order_by(Module.order_index).all()
    
    # Calculate progress statistics
    total_lessons = 0
    completed_lessons = 0
    
    for module in modules:
        published_lessons = [l for l in module.lessons if l.is_published]
        total_lessons += len(published_lessons)
        
        for lesson in published_lessons:
            progress = StudentProgress.query.filter_by(
                student_id=current_user.id,
                lesson_id=lesson.id,
                enrollment_id=enrollment.id
            ).first()
            if progress and progress.completed:
                completed_lessons += 1
    
    progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    # Get recent activity
    recent_progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        enrollment_id=enrollment.id
    ).order_by(StudentProgress.last_accessed.desc()).limit(5).all()
    
    return render_template('learning/course_portal.html', 
                         course=course, 
                         modules=modules,
                         enrollment=enrollment,
                         total_lessons=total_lessons,
                         completed_lessons=completed_lessons,
                         progress_percentage=progress_percentage,
                         recent_progress=recent_progress)


@app.route('/learn/lessons/<int:lesson_id>')
@login_required
def student_lesson_view(lesson_id):
    """Individual lesson viewing interface for students"""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Check if student is enrolled in the course
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course_id,
        status='active'
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if lesson is published
    if not lesson.is_published:
        flash('This lesson is not available yet.', 'warning')
        return redirect(url_for('student_course_portal', course_id=lesson.module.course_id))
    
    # Get or create progress record
    progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        lesson_id=lesson_id,
        enrollment_id=enrollment.id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=current_user.id,
            lesson_id=lesson_id,
            enrollment_id=enrollment.id
        )
        db.session.add(progress)
        db.session.commit()
    
    # Update access tracking
    progress.access_count += 1
    progress.last_accessed = datetime.utcnow()
    db.session.commit()
    
    # Get navigation context (previous/next lessons)
    module = lesson.module
    module_lessons = [l for l in module.lessons if l.is_published]
    module_lessons.sort(key=lambda x: x.order_index)
    
    current_index = next((i for i, l in enumerate(module_lessons) if l.id == lesson_id), 0)
    previous_lesson = module_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = module_lessons[current_index + 1] if current_index < len(module_lessons) - 1 else None
    
    # If no next lesson in current module, check next module
    if not next_lesson:
        next_module = Module.query.filter(
            Module.course_id == lesson.module.course_id,
            Module.is_published == True,
            Module.order_index > module.order_index
        ).order_by(Module.order_index).first()
        
        if next_module and next_module.lessons:
            first_published_lesson = next((l for l in next_module.lessons if l.is_published), None)
            if first_published_lesson:
                next_lesson = first_published_lesson
    
    return render_template('learning/lesson_view.html',
                         lesson=lesson,
                         progress=progress,
                         enrollment=enrollment,
                         previous_lesson=previous_lesson,
                         next_lesson=next_lesson,
                         module_lessons=module_lessons,
                         current_index=current_index)


@app.route('/api/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def mark_lesson_complete(lesson_id):
    """API endpoint to mark a lesson as completed"""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course_id,
        status='active'
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Not enrolled in course'}), 403
    
    # Get progress record
    progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        lesson_id=lesson_id,
        enrollment_id=enrollment.id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=current_user.id,
            lesson_id=lesson_id,
            enrollment_id=enrollment.id
        )
        db.session.add(progress)
    
    # Mark as completed
    if not progress.completed:
        progress.mark_complete()
    
    return jsonify({
        'status': 'success',
        'completed': progress.completed,
        'completion_date': progress.completion_date.isoformat() if progress.completion_date else None
    })


@app.route('/api/lesson/<int:lesson_id>/time', methods=['POST'])
@login_required
def track_lesson_time(lesson_id):
    """API endpoint to track time spent on a lesson"""
    data = request.get_json()
    minutes = data.get('minutes', 0)
    
    if minutes <= 0:
        return jsonify({'error': 'Invalid time'}), 400
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course_id,
        status='active'
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Not enrolled in course'}), 403
    
    # Get progress record
    progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        lesson_id=lesson_id,
        enrollment_id=enrollment.id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=current_user.id,
            lesson_id=lesson_id,
            enrollment_id=enrollment.id
        )
        db.session.add(progress)
    
    # Add time spent
    progress.add_time_spent(minutes)
    
    return jsonify({
        'status': 'success',
        'total_time': progress.time_spent_minutes
    })


@app.route('/api/lesson/<int:lesson_id>/bookmark', methods=['POST'])
@login_required
def toggle_lesson_bookmark(lesson_id):
    """API endpoint to bookmark/unbookmark a lesson"""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course_id,
        status='active'
    ).first()
    
    if not enrollment:
        return jsonify({'error': 'Not enrolled in course'}), 403
    
    # Get progress record
    progress = StudentProgress.query.filter_by(
        student_id=current_user.id,
        lesson_id=lesson_id,
        enrollment_id=enrollment.id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=current_user.id,
            lesson_id=lesson_id,
            enrollment_id=enrollment.id
        )
        db.session.add(progress)
        db.session.commit()
    
    # Toggle bookmark
    progress.bookmarked = not progress.bookmarked
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'bookmarked': progress.bookmarked
    })


# ============================================================================
# END PHASE 2C ROUTES
# ============================================================================

# Update login manager after routes are defined
login_manager.login_view = 'login'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    # Show only flagship programs: Pearson BTEC and Hotel Culinary Management
    courses = Course.query.filter(
        Course.is_active == True,
        (Course.title.ilike('%BTEC%') | Course.title.ilike('%Hotel Culinary Management%'))
    ).all()
    return render_template('courses.html', courses=courses)


@app.route('/admissions')
def admissions():
    return render_template('admissions.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    """Enhanced multi-step application form"""
    if request.method == 'POST':
        try:
            # Handle AJAX submission
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Extract form data
                course_id = request.form.get('course_id')
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                email = request.form.get('email')
                phone = request.form.get('phone')
                date_of_birth = request.form.get('date_of_birth')
                nationality = request.form.get('nationality')
                address = request.form.get('address')
                education_level = request.form.get('education_level')
                work_experience = request.form.get('work_experience')
                motivation = request.form.get('motivation')
                
                # Validate required fields
                if not all([course_id, first_name, last_name, email, phone, motivation]):
                    return jsonify({
                        'success': False,
                        'error': 'Please fill in all required fields.'
                    })
                
                # Validate course_id is an integer
                try:
                    course_id = int(course_id)
                except (ValueError, TypeError):
                    return jsonify({
                        'success': False,
                        'error': 'Invalid course selection.'
                    })
                
                # Get course
                course = Course.query.get(course_id)
                if not course:
                    return jsonify({
                        'success': False,
                        'error': 'Selected course not found.'
                    })
                
                # Check if user is logged in, if not create temporary record
                user = None
                if current_user and current_user.is_authenticated:
                    user = current_user
                else:
                    # Check if user with this email exists
                    user = User.query.filter_by(email=email).first()
                    if not user:
                        # Create new user account for applicant
                        user = User(
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            role='student'
                        )
                        user.set_password('temp_' + email.split('@')[0])  # Temporary password
                        db.session.add(user)
                        db.session.flush()
                
                # Create application
                application = Application(
                    user_id=user.id,
                    course_id=course_id,
                    education_level=education_level,
                    work_experience=work_experience,
                    motivation=motivation,
                    status='pending'
                )
                
                db.session.add(application)
                db.session.commit()
                
                # Create notifications for all admin users
                admin_users = User.query.filter_by(role='admin').all()
                full_name = f'{first_name} {last_name}'
                for admin in admin_users:
                    notification = Notification(
                        user_id=admin.id,
                        type='application',
                        title=f'New Application: {course.title}',
                        message=f'{full_name} ({email}) has submitted an application for {course.title}. Phone: {phone}, Education: {education_level or "Not specified"}',
                        link_url=f'/admin/applications',
                        priority='high'
                    )
                    db.session.add(notification)
                
                db.session.commit()
                
                # Send confirmation email
                try:
                    email_service.send_application_confirmation(
                        to_email=email,
                        first_name=first_name,
                        course_name=course.title,
                        application_id=application.id
                    )
                except Exception as e:
                    # Log email error but don't fail the application
                    print(f"Email sending failed: {e}")
                
                return jsonify({
                    'success': True,
                    'message': 'Application submitted successfully!',
                    'application_id': application.id
                })
                
            else:
                # Handle regular form submission (fallback)
                flash('Application submitted successfully! We will contact you soon.', 'success')
                return redirect(url_for('apply'))
                
        except Exception as e:
            print(f"Application error: {e}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'error': 'An error occurred while submitting your application. Please try again.'
                })
            else:
                flash('An error occurred. Please try again.', 'error')
                return redirect(url_for('apply'))
    
    # GET request - show application form
    # Limit to flagship programs for applications as well
    courses = Course.query.filter(
        Course.is_active == True,
        (Course.title.ilike('%BTEC%') | Course.title.ilike('%Hotel Culinary Management%'))
    ).all()
    return render_template('apply.html', courses=courses)


@app.route('/apply/<int:course_id>')
def apply_course_redirect(course_id):
    """Course-specific apply route - redirects to course application"""
    course = Course.query.get_or_404(course_id)
    if current_user.is_authenticated:
        return redirect(url_for('apply_course', course_id=course_id))
    else:
        return redirect(url_for('login', next=url_for('apply_course', course_id=course_id)))


@app.route('/student-life')
def student_life():
    return render_template('student_life.html')


# Faculty section temporarily disabled
# @app.route('/faculty')
# def faculty():
#     return render_template('faculty.html')


@app.route('/consultation', methods=['GET', 'POST'])
def consultation():
    """Consultation booking page"""
    try:
        form = ConsultationBookingForm()
        
        if form.validate_on_submit():
            # Create new consultation
            consultation = Consultation(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                consultation_type=form.consultation_type.data,
                preferred_date=form.preferred_date.data,
                preferred_time=datetime.strptime(form.preferred_time.data, '%H:%M').time(),
                meeting_type=form.meeting_type.data,
                course_id=form.course_id.data if form.course_id.data else None,
                message=form.message.data,
                special_requirements=form.special_requirements.data,
                status='pending'
            )
            
            try:
                db.session.add(consultation)
                db.session.commit()
                
                # Send confirmation email to applicant
                email_service.send_consultation_confirmation(consultation)
                
                # Send notification to admin
                email_service.send_consultation_notification(consultation)
                
                flash('Your consultation has been booked successfully! We will contact you within 24 hours to confirm the details.', 'success')
                return redirect(url_for('consultation_confirmation', consultation_id=consultation.id))
                
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while booking your consultation. Please try again.', 'error')
                print(f"Consultation booking error: {e}")
        
        return render_template('consultation.html', form=form, today=datetime.now().date().isoformat())
    
    except Exception as e:
        print(f"Consultation route error: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred loading the consultation page. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/consultation/confirmation/<int:consultation_id>')
def consultation_confirmation(consultation_id):
    """Consultation booking confirmation page"""
    consultation = Consultation.query.get_or_404(consultation_id)
    return render_template('consultation_confirmation.html', consultation=consultation)


@app.route('/admin/consultations')
@login_required
def admin_consultations():
    """Admin consultations management"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    consultations = Consultation.query.order_by(Consultation.created_at.desc()).all()
    return render_template('admin/consultations.html', consultations=consultations)


@app.route('/admin/consultation/<int:consultation_id>/update', methods=['POST'])
@login_required
def update_consultation(consultation_id):
    """Update consultation status"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    consultation = Consultation.query.get_or_404(consultation_id)
    
    status = request.form.get('status')
    meeting_link = request.form.get('meeting_link', '')
    meeting_location = request.form.get('meeting_location', '')
    notes = request.form.get('notes', '')
    
    consultation.status = status
    consultation.meeting_link = meeting_link
    consultation.meeting_location = meeting_location
    consultation.assigned_to = current_user.id
    consultation.updated_at = datetime.utcnow()
    
    if status == 'confirmed':
        consultation.confirmation_sent = datetime.utcnow()
    
    try:
        db.session.commit()
        
        # Send confirmation email if status is confirmed
        if status == 'confirmed':
            email_service.send_consultation_confirmed(consultation)
        
        flash(f'Consultation {consultation_id} updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating consultation.', 'error')
        print(f"Consultation update error: {e}")
    
    return redirect(url_for('admin_consultations'))


@app.route('/admin/contact-inquiries')
@login_required
def admin_contact_inquiries():
    """Admin contact inquiries management"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Get inquiries with filters
    status_filter = request.args.get('status', 'all')
    
    query = ContactInquiry.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    inquiries = query.order_by(ContactInquiry.created_at.desc()).all()
    
    return render_template('admin/contact_inquiries.html', inquiries=inquiries, status_filter=status_filter)


@app.route('/admin/contact-inquiry/<int:inquiry_id>/update', methods=['POST'])
@login_required
def update_contact_inquiry(inquiry_id):
    """Update contact inquiry status"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    inquiry = ContactInquiry.query.get_or_404(inquiry_id)
    
    action = request.form.get('action')
    
    if action == 'resolve':
        inquiry.status = 'resolved'
        inquiry.resolved_at = datetime.utcnow()
        inquiry.resolved_by_id = current_user.id
        inquiry.admin_notes = request.form.get('admin_notes', '')
        flash('Contact inquiry marked as resolved', 'success')
    
    elif action == 'in_progress':
        inquiry.status = 'in_progress'
        flash('Contact inquiry marked as in progress', 'success')
    
    elif action == 'reopen':
        inquiry.status = 'new'
        inquiry.resolved_at = None
        inquiry.resolved_by_id = None
        flash('Contact inquiry reopened', 'success')
    
    db.session.commit()
    return redirect(url_for('admin_contact_inquiries'))


@app.route('/facilities')
def facilities():
    return render_template('facilities.html')


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create inquiry record
        inquiry = ContactInquiry(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            program_interest=form.program_interest.data,
            message=form.message.data,
            subscribe_newsletter=form.subscribe_newsletter.data
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        # Create admin notifications
        admin_users = User.query.filter_by(role='admin').all()
        for admin in admin_users:
            notification = Notification(
                user_id=admin.id,
                type='contact',
                title=f'New Contact Inquiry: {form.subject.data}',
                message=f'{form.first_name.data} {form.last_name.data} ({form.email.data}) has sent a message via the contact form. Subject: {form.subject.data}',
                link_url='/admin/contact-inquiries',
                priority='medium'
            )
            db.session.add(notification)
        
        db.session.commit()
        
        flash('Thank you for contacting us! We will respond within 24-48 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)


def create_admin_user():
    """Create default admin user if it doesn't exist"""
    admin = User.query.filter_by(email='admin@penasia.edu.hk').first()
    if not admin:
        admin = User()
        admin.email = 'admin@penasia.edu.hk'
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.role = 'admin'
        admin.is_active = True
        admin.email_verified = True
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: admin@penasia.edu.hk / admin123")

def create_courses():
    """Create the 4 core courses from the master document"""
    # Clear existing courses first
    Course.query.delete()
    db.session.commit()
    print("Cleared existing courses")
    
    # Course 169: Hotel Culinary Management
    course169 = Course(
        course_code='PSCE-DHM-5266',
        title='Hotel Culinary Management Diploma',
        description='2-year full-time diploma program providing professional culinary training and hotel management knowledge.',
        duration_weeks=104,  # 2 years
        duration_hours=2080,  # Approximate full-time hours
        fee_hkd=125000,
        cef_eligible=False,
        max_students=30,
        language='English',
        level='QF Level 3',
        prerequisites='Form 6 completion with DSE English Level 2, or IELTS 4.5+ or pass interview',
        category='Culinary',
        is_featured=True,
        is_active=True,
        learning_outcomes='Professional culinary skills, hotel management knowledge, food safety certification',
        course_content='Food Safety & Occupational Health, Kitchen Operations, Baking & Pastry, Food Service & Operations, Communication & Report Writing, Hospitality Industry Overview, Culinary Arts',
        certification='Diploma in Hotel Culinary Management'
    )
    
    # Course 1: BTEC Business Management
    course1 = Course(
        course_code='PSCE-BTB-5001',
        title='BTEC Business Management HND',
        description='Pearson BTEC Level 5 Higher National Diploma with direct progression to UK university final year. Build essential business and management skills.',
        duration_weeks=104,  # 2 years
        duration_hours=1200,
        fee_hkd=118000,
        cef_eligible=False,
        max_students=30,
        language='English',
        level='RQF Level 5',
        prerequisites='HKDSE: 5 subjects at Level 2+ (including Chinese and English), IELTS 5.5 or equivalent, Age 18+',
        category='Business',
        is_featured=True,
        is_active=True,
        learning_outcomes='Business management skills, strategic thinking, leadership development',
        course_content='Business Environment, Marketing Essentials, HR Management, Management & Operations, Management Accounting, Business Project, Business Law, Business Strategy',
        certification='Pearson BTEC Higher National Diploma in Business'
    )
    
    # Course 171: Western Bakery & Pastry - ADMISSIONS CLOSED
    course171 = Course(
        course_code='CEF-43C130000',
        title='Western Bakery & Pastry',
        description='QF Level 2 certificate with hands-on practical training in Western baking techniques.',
        duration_weeks=11,
        duration_hours=33,
        fee_hkd=12620,
        cef_eligible=True,
        cef_fee_hkd=12620,
        max_students=20,
        language='Cantonese',
        level='QF Level 2',
        prerequisites='Form 3 completion, minimum age 18',
        category='Culinary',
        is_featured=True,
        is_active=False,  # Admissions closed
        learning_outcomes='Western baking techniques, pastry skills, professional presentation',
        course_content='Course Introduction, Western Baking History, Bread Making, Cake Making, Pastry Making, Cookie & Biscuit Making, Advanced Pastry, Final Project',
        certification='Certificate in Western Bakery and Pastry (QF Level 2)'
    )
    
    # Course 179: Western Cuisine Certificate - ADMISSIONS CLOSED
    course179 = Course(
        course_code='CEF-43C15919A',
        title='Western Cuisine Certificate',
        description='Professional culinary skills training with focus on Western cooking techniques and presentation.',
        duration_weeks=10,
        duration_hours=33,
        fee_hkd=13200,
        cef_eligible=True,
        cef_fee_hkd=13200,
        max_students=20,
        language='English supplemented with Cantonese',
        level='QF Level 2',
        prerequisites='Form 3 completion, minimum age 18',
        category='Culinary',
        is_featured=True,
        is_active=False,  # Admissions closed
        learning_outcomes='Western cuisine fundamentals, professional cooking techniques, menu planning',
        course_content='Western Cuisine Fundamentals, Kitchen Tools & Equipment, Soups and Salads, Advanced Cooking Techniques, Menu Planning, Food Cost Control',
        certification='Certificate in Western Starter and Main Course (QF Level 2)'
    )
    
    # Add all courses to database
    db.session.add_all([course169, course1, course171, course179])
    db.session.commit()
    
    # Update the IDs to match our templates
    course169.id = 169
    course1.id = 1  
    course171.id = 171
    course179.id = 179
    db.session.commit()
    
    print("Created 4 core courses: 169, 1, 171, 179")

# Admin Assignment Management Routes
@app.route('/admin/assignments')
@login_required
def admin_assignments():
    """Admin assignment management dashboard"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    assignments = Assignment.query.join(Course).all()
    return render_template('admin/assignments.html', assignments=assignments)


@app.route('/admin/assignments/create', methods=['GET', 'POST'])
@login_required
def admin_create_assignment():
    """Create new assignment"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        assignment = Assignment(
            title=request.form.get('title'),
            description=request.form.get('description'),
            instructions=request.form.get('instructions'),
            assignment_type=request.form.get('assignment_type'),
            course_id=int(request.form.get('course_id')),
            due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M') if request.form.get('due_date') else None,
            max_points=int(request.form.get('max_points', 100)),
            created_at=datetime.utcnow()
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        flash(f'Assignment "{assignment.title}" created successfully!', 'success')
        return redirect(url_for('admin_assignments'))
    
    courses = Course.query.all()
    return render_template('admin/create_assignment.html', courses=courses)


@app.route('/admin/assignments/<int:assignment_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_assignment(assignment_id):
    """Edit existing assignment"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        assignment.title = request.form.get('title')
        assignment.description = request.form.get('description')
        assignment.instructions = request.form.get('instructions')
        assignment.assignment_type = request.form.get('assignment_type')
        assignment.course_id = int(request.form.get('course_id'))
        assignment.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M') if request.form.get('due_date') else None
        assignment.max_points = int(request.form.get('max_points', 100))
        
        db.session.commit()
        
        flash(f'Assignment "{assignment.title}" updated successfully!', 'success')
        return redirect(url_for('admin_assignments'))
    
    courses = Course.query.all()
    return render_template('admin/edit_assignment.html', assignment=assignment, courses=courses)


@app.route('/admin/assignments/<int:assignment_id>/submissions')
@login_required
def admin_assignment_submissions(assignment_id):
    """View assignment submissions"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = AssignmentSubmission.query.filter_by(assignment_id=assignment_id).join(User).all()
    
    return render_template('admin/assignment_submissions.html', assignment=assignment, submissions=submissions)


@app.route('/admin/submissions/<int:submission_id>/grade', methods=['POST'])
@login_required
def admin_grade_submission(submission_id):
    """Grade assignment submission"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    submission = AssignmentSubmission.query.get_or_404(submission_id)
    
    submission.grade = float(request.form.get('grade', 0))
    submission.feedback = request.form.get('feedback', '')
    submission.status = 'graded'
    submission.graded_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'Submission graded successfully!', 'success')
    return redirect(url_for('admin_assignment_submissions', assignment_id=submission.assignment_id))


# Admin Schedule Management Routes
@app.route('/admin/schedules')
@login_required
def admin_schedules():
    """Admin class schedule management dashboard"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    schedules = ClassSchedule.query.join(Course).order_by(ClassSchedule.class_date.desc()).all()
    return render_template('admin/schedules.html', schedules=schedules)


@app.route('/admin/schedules/create', methods=['GET', 'POST'])
@login_required
def admin_create_schedule():
    """Create new class schedule"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Parse date and time
        class_date = datetime.strptime(request.form.get('class_date'), '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
        end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
        
        # Combine date and time for class_date field
        class_datetime = datetime.combine(class_date, start_time)
        
        schedule = ClassSchedule(
            course_id=int(request.form.get('course_id')),
            topic=request.form.get('topic'),
            description=request.form.get('description'),
            class_date=class_datetime,
            start_time=start_time,
            end_time=end_time,
            location=request.form.get('location'),
            instructor=request.form.get('instructor'),
            class_type=request.form.get('class_type'),
            max_participants=int(request.form.get('max_participants', 20))
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        flash(f'Class schedule for "{schedule.topic}" created successfully!', 'success')
        return redirect(url_for('admin_schedules'))
    
    courses = Course.query.all()
    return render_template('admin/create_schedule.html', courses=courses)


@app.route('/admin/schedules/<int:schedule_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_schedule(schedule_id):
    """Edit existing class schedule"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    schedule = ClassSchedule.query.get_or_404(schedule_id)
    
    if request.method == 'POST':
        # Parse date and time
        class_date = datetime.strptime(request.form.get('class_date'), '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
        end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
        
        # Combine date and time for class_date field
        class_datetime = datetime.combine(class_date, start_time)
        
        schedule.course_id = int(request.form.get('course_id'))
        schedule.topic = request.form.get('topic')
        schedule.description = request.form.get('description')
        schedule.class_date = class_datetime
        schedule.start_time = start_time
        schedule.end_time = end_time
        schedule.location = request.form.get('location')
        schedule.instructor = request.form.get('instructor')
        schedule.class_type = request.form.get('class_type')
        schedule.max_participants = int(request.form.get('max_participants', 20))
        
        db.session.commit()
        
        flash(f'Class schedule for "{schedule.topic}" updated successfully!', 'success')
        return redirect(url_for('admin_schedules'))
    
    courses = Course.query.all()
    return render_template('admin/edit_schedule.html', schedule=schedule, courses=courses)


@app.route('/admin/students/<int:student_id>/assignments')
@login_required
def admin_student_assignments(student_id):
    """View specific student's assignments and progress"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    student = User.query.get_or_404(student_id)
    if student.role != 'student':
        flash('User is not a student.', 'error')
        return redirect(url_for('admin_students'))
    
    # Get student's enrolled courses
    enrolled_course_ids = [e.course_id for e in student.enrollments]
    
    # Get assignments for enrolled courses
    assignments = Assignment.query.filter(Assignment.course_id.in_(enrolled_course_ids)).all()
    
    # Get submissions
    assignment_data = []
    for assignment in assignments:
        submission = AssignmentSubmission.query.filter_by(
            assignment_id=assignment.id,
            student_id=student_id
        ).first()
        assignment_data.append({
            'assignment': assignment,
            'submission': submission
        })
    
    return render_template('admin/student_assignments.html', 
                         student=student, assignment_data=assignment_data)


@app.route('/admin/students/<int:student_id>/schedules')
@login_required
def admin_student_schedules(student_id):
    """View specific student's class schedules"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    student = User.query.get_or_404(student_id)
    if student.role != 'student':
        flash('User is not a student.', 'error')
        return redirect(url_for('admin_students'))
    
    # Get student's enrolled courses
    enrolled_course_ids = [e.course_id for e in student.enrollments]
    
    # Get schedules for enrolled courses
    schedules = ClassSchedule.query.filter(
        ClassSchedule.course_id.in_(enrolled_course_ids)
    ).order_by(ClassSchedule.class_date.asc()).all()
    
    return render_template('admin/student_schedules.html', 
                         student=student, schedules=schedules)


# ============================================================================
# NOTIFICATION SYSTEM ROUTES
# ============================================================================

@app.route('/notifications')
@login_required
def notifications():
    """View all notifications for current user"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    notifications = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # Mark all as read when viewing notification page
    unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    for notif in unread:
        notif.mark_as_read()
    
    return render_template('notifications/index.html', notifications=notifications)


@app.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a single notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Verify ownership
    if notification.user_id != current_user.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('notifications'))
    
    notification.mark_as_read()
    
    if request.is_json:
        return jsonify({'success': True})
    
    return redirect(url_for('notifications'))


@app.route('/api/notifications/unread-count')
@login_required
def unread_notification_count():
    """Get count of unread notifications"""
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})


def create_notification(user_id, type, title, message, link_url=None, priority='normal'):
    """Helper function to create a notification"""
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        link_url=link_url,
        priority=priority
    )
    db.session.add(notification)
    db.session.commit()
    return notification


# ============================================================================
# MESSAGING SYSTEM ROUTES
# ============================================================================

@app.route('/messages')
@login_required
def messages_inbox():
    """View inbox messages"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    messages = Message.query.filter_by(recipient_id=current_user.id, is_deleted_by_recipient=False)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    unread_count = Message.query.filter_by(recipient_id=current_user.id, is_read=False, is_deleted_by_recipient=False).count()
    
    return render_template('messages/inbox.html', messages=messages, unread_count=unread_count)


@app.route('/messages/sent')
@login_required
def messages_sent():
    """View sent messages"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    messages = Message.query.filter_by(sender_id=current_user.id, is_deleted_by_sender=False)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('messages/sent.html', messages=messages)


@app.route('/messages/compose', methods=['GET', 'POST'])
@login_required
def messages_compose():
    """Compose and send a new message"""
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        body = request.form.get('body')
        priority = request.form.get('priority', 'normal')
        
        # Validate
        if not all([recipient_id, subject, body]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('messages_compose'))
        
        # Create message
        message = Message(
            sender_id=current_user.id,
            recipient_id=int(recipient_id),
            subject=subject,
            body=body,
            priority=priority
        )
        db.session.add(message)
        db.session.commit()
        
        # Create notification for recipient
        create_notification(
            user_id=int(recipient_id),
            type='message',
            title='New Message',
            message=f'{current_user.full_name} sent you a message: {subject}',
            link_url=url_for('messages_view', message_id=message.id),
            priority=priority
        )
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages_sent'))
    
    # Get potential recipients (admins, instructors)
    recipients = User.query.filter(User.role.in_(['admin', 'instructor'])).all()
    
    return render_template('messages/compose.html', recipients=recipients)


@app.route('/messages/<int:message_id>')
@login_required
def messages_view(message_id):
    """View a specific message"""
    message = Message.query.get_or_404(message_id)
    
    # Verify user has access
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('messages_inbox'))
    
    # Mark as read if recipient is viewing
    if message.recipient_id == current_user.id:
        message.mark_as_read()
    
    # Get thread (all replies)
    if message.parent_message_id:
        # This is a reply, get the original message
        thread_messages = Message.query.filter(
            (Message.id == message.parent_message_id) | 
            (Message.parent_message_id == message.parent_message_id)
        ).order_by(Message.created_at.asc()).all()
    else:
        # This is the original, get all replies
        thread_messages = [message] + list(message.replies)
    
    return render_template('messages/view.html', message=message, thread_messages=thread_messages)


@app.route('/messages/<int:message_id>/reply', methods=['POST'])
@login_required
def messages_reply(message_id):
    """Reply to a message"""
    original_message = Message.query.get_or_404(message_id)
    
    # Verify user has access
    if original_message.sender_id != current_user.id and original_message.recipient_id != current_user.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('messages_inbox'))
    
    body = request.form.get('body')
    
    if not body:
        flash('Reply cannot be empty.', 'error')
        return redirect(url_for('messages_view', message_id=message_id))
    
    # Determine recipient (send to the other person in the conversation)
    recipient_id = original_message.sender_id if original_message.recipient_id == current_user.id else original_message.recipient_id
    
    # Create reply
    reply = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        subject=f"Re: {original_message.subject}",
        body=body,
        parent_message_id=original_message.parent_message_id or original_message.id,
        priority=original_message.priority
    )
    db.session.add(reply)
    db.session.commit()
    
    # Create notification
    create_notification(
        user_id=recipient_id,
        type='message',
        title='New Reply',
        message=f'{current_user.full_name} replied to: {original_message.subject}',
        link_url=url_for('messages_view', message_id=reply.id)
    )
    
    flash('Reply sent successfully!', 'success')
    return redirect(url_for('messages_view', message_id=message_id))


@app.route('/api/messages/unread-count')
@login_required
def unread_message_count():
    """Get count of unread messages"""
    count = Message.query.filter_by(recipient_id=current_user.id, is_read=False, is_deleted_by_recipient=False).count()
    return jsonify({'count': count})


# ============================================================================
# ATTENDANCE TRACKING ROUTES
# ============================================================================

@app.route('/admin/attendance')
@login_required
def admin_attendance():
    """View attendance overview"""
    if current_user.role not in ['admin', 'instructor']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get upcoming classes
    upcoming_classes = ClassSchedule.query.filter(
        ClassSchedule.class_date >= datetime.utcnow()
    ).order_by(ClassSchedule.class_date.asc()).limit(10).all()
    
    return render_template('admin/attendance.html', upcoming_classes=upcoming_classes)


@app.route('/admin/attendance/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def mark_attendance(schedule_id):
    """Mark attendance for a specific class"""
    if current_user.role not in ['admin', 'instructor']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    schedule = ClassSchedule.query.get_or_404(schedule_id)
    
    # Get enrolled students for this course
    enrollments = Enrollment.query.filter_by(course_id=schedule.course_id, status='active').all()
    
    if request.method == 'POST':
        # Process attendance marking
        for enrollment in enrollments:
            student_id = enrollment.student_id
            status = request.form.get(f'attendance_{student_id}')
            notes = request.form.get(f'notes_{student_id}', '')
            
            if status:
                # Check if attendance already exists
                existing = Attendance.query.filter_by(
                    student_id=student_id,
                    class_schedule_id=schedule_id
                ).first()
                
                if existing:
                    existing.status = status
                    existing.notes = notes
                    existing.marked_by = current_user.id
                else:
                    attendance = Attendance(
                        student_id=student_id,
                        class_schedule_id=schedule_id,
                        course_id=schedule.course_id,
                        date=schedule.class_date.date(),
                        status=status,
                        notes=notes,
                        marked_by=current_user.id,
                        check_in_time=datetime.utcnow() if status == 'present' else None
                    )
                    db.session.add(attendance)
        
        db.session.commit()
        flash('Attendance marked successfully!', 'success')
        return redirect(url_for('admin_attendance'))
    
    # Get existing attendance records
    attendance_records = {a.student_id: a for a in Attendance.query.filter_by(class_schedule_id=schedule_id).all()}
    
    return render_template('admin/mark_attendance.html', 
                         schedule=schedule, 
                         enrollments=enrollments,
                         attendance_records=attendance_records)


@app.route('/attendance/student/<int:student_id>')
@login_required
def student_attendance_report(student_id):
    """View attendance report for a student"""
    # Allow admins, instructors, or the student themselves
    if current_user.role not in ['admin', 'instructor'] and current_user.id != student_id:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    student = User.query.get_or_404(student_id)
    
    # Get attendance records grouped by course
    attendance_by_course = {}
    for enrollment in student.enrollments:
        course = enrollment.course
        records = Attendance.query.filter_by(
            student_id=student_id,
            course_id=course.id
        ).all()
        
        if records:
            total = len(records)
            present = sum(1 for r in records if r.status in ['present', 'late'])
            percentage = (present / total * 100) if total > 0 else 0
            
            attendance_by_course[course.id] = {
                'course': course,
                'records': records,
                'total_classes': total,
                'present_count': present,
                'percentage': round(percentage, 1)
            }
    
    return render_template('attendance/student_report.html', 
                         student=student,
                         attendance_by_course=attendance_by_course)


@app.route('/my-attendance')
@login_required
def my_attendance():
    """View current user's attendance"""
    return redirect(url_for('student_attendance_report', student_id=current_user.id))


# ============================================================================
# CERTIFICATE GENERATION ROUTES
# ============================================================================

@app.route('/certificates')
@login_required
def my_certificates():
    """View user's certificates"""
    certificates = Certificate.query.filter_by(user_id=current_user.id).order_by(Certificate.issue_date.desc()).all()
    return render_template('certificates/index.html', certificates=certificates)


@app.route('/admin/certificates/generate/<int:enrollment_id>', methods=['POST'])
@login_required
def generate_certificate(enrollment_id):
    """Generate certificate for completed enrollment"""
    if current_user.role != 'admin':
        flash('Only admins can generate certificates.', 'error')
        return redirect(url_for('dashboard'))
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    # Verify enrollment is completed
    if enrollment.status != 'completed':
        flash('Can only generate certificates for completed enrollments.', 'error')
        return redirect(url_for('admin_students'))
    
    # Check if certificate already exists
    existing = Certificate.query.filter_by(enrollment_id=enrollment_id).first()
    if existing:
        flash('Certificate already exists for this enrollment.', 'error')
        return redirect(url_for('admin_students'))
    
    # Calculate attendance percentage
    attendance_records = Attendance.query.filter_by(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    ).all()
    
    if attendance_records:
        total = len(attendance_records)
        present = sum(1 for r in attendance_records if r.status in ['present', 'late'])
        attendance_percentage = (present / total * 100) if total > 0 else 0
    else:
        attendance_percentage = 100  # Default if no attendance tracked
    
    # Create certificate
    certificate = Certificate(
        user_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrollment_id=enrollment_id,
        completion_date=enrollment.completion_date or datetime.utcnow().date(),
        final_grade=enrollment.final_grade,
        issued_by=current_user.id,
        attendance_percentage=attendance_percentage
    )
    
    # Generate unique identifiers
    certificate.certificate_number = certificate.generate_certificate_number()
    certificate.verification_code = certificate.generate_verification_code()
    
    # Determine grade letter
    if certificate.final_grade:
        if certificate.final_grade >= 90:
            certificate.grade_letter = 'A'
            certificate.honors = 'Distinction'
        elif certificate.final_grade >= 80:
            certificate.grade_letter = 'B'
            certificate.honors = 'Merit'
        elif certificate.final_grade >= 70:
            certificate.grade_letter = 'C'
            certificate.honors = 'Pass'
        else:
            certificate.grade_letter = 'D'
            certificate.honors = 'Pass'
    
    db.session.add(certificate)
    db.session.commit()
    
    # Create notification for student
    create_notification(
        user_id=enrollment.student_id,
        type='certificate',
        title='Certificate Available',
        message=f'Your certificate for {enrollment.course.title} is now available for download!',
        link_url=url_for('my_certificates'),
        priority='high'
    )
    
    flash(f'Certificate generated successfully! Number: {certificate.certificate_number}', 'success')
    return redirect(url_for('admin_students'))


@app.route('/certificates/<int:certificate_id>/download')
@login_required
def download_certificate(certificate_id):
    """Download certificate PDF"""
    certificate = Certificate.query.get_or_404(certificate_id)
    
    # Verify access
    if certificate.user_id != current_user.id and not current_user.is_admin():
        flash('Unauthorized access.', 'error')
        return redirect(url_for('my_certificates'))
    
    try:
        user = certificate.user
        course = certificate.course
        
        # Generate PDF
        pdf_buffer = certificate_generator.generate_certificate_pdf(certificate, user, course)
        
        # Return PDF file
        filename = f"Certificate_{certificate.certificate_number}.pdf"
        
        if isinstance(pdf_buffer, str):
            # HTML fallback
            return render_template('certificates/view.html', 
                                 certificate=certificate,
                                 html_content=pdf_buffer)
        else:
            # PDF file
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
    except Exception as e:
        print(f"Certificate generation error: {str(e)}")
        flash(f'Error generating certificate: {str(e)}', 'error')
        return redirect(url_for('my_certificates'))


@app.route('/verify-certificate/<code>')
def verify_certificate(code):
    """Public certificate verification"""
    certificate = Certificate.query.filter_by(verification_code=code).first()
    
    if not certificate:
        return render_template('certificates/verify.html', 
                             certificate=None, 
                             message='Certificate not found')
    
    if not certificate.is_valid:
        return render_template('certificates/verify.html', 
                             certificate=certificate, 
                             message='Certificate has been revoked')
    
    return render_template('certificates/verify.html', 
                         certificate=certificate, 
                         message='Certificate is valid')


# ============================================================================
# ANNOUNCEMENT SYSTEM ROUTES  
# ============================================================================

@app.route('/announcements')
@login_required
def announcements():
    """View all announcements"""
    # Get institution-wide announcements
    institution_announcements = Announcement.query.filter_by(course_id=None, is_published=True)\
        .filter(Announcement.is_draft == False)\
        .order_by(Announcement.is_pinned.desc(), Announcement.published_at.desc())\
        .all()
    
    # Get course-specific announcements for user's courses
    course_announcements = []
    if current_user.role == 'student':
        enrolled_course_ids = [e.course_id for e in current_user.enrollments if e.status == 'active']
        if enrolled_course_ids:
            course_announcements = Announcement.query.filter(
                Announcement.course_id.in_(enrolled_course_ids),
                Announcement.is_published == True,
                Announcement.is_draft == False
            ).order_by(Announcement.published_at.desc()).all()
    
    return render_template('announcements/index.html', 
                         institution_announcements=institution_announcements,
                         course_announcements=course_announcements)


@app.route('/admin/announcements/create', methods=['GET', 'POST'])
@login_required
def create_announcement():
    """Create new announcement"""
    if current_user.role not in ['admin', 'instructor']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        course_id = request.form.get('course_id')
        priority = request.form.get('priority', 'normal')
        is_pinned = request.form.get('is_pinned') == 'on'
        
        announcement = Announcement(
            title=title,
            content=content,
            author_id=current_user.id,
            course_id=int(course_id) if course_id else None,
            priority=priority,
            is_pinned=is_pinned
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('announcements'))
    
    courses = Course.query.filter_by(is_active=True).all()
    return render_template('announcements/create.html', courses=courses)


# Additional routes
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html', now=datetime.utcnow()), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    return render_template('errors/403.html'), 403

@app.errorhandler(400)
def bad_request_error(error):
    """Handle 400 errors"""
    flash('Bad request. Please check your input.', 'error')
    return redirect(url_for('index')), 400

# Global exception handler
@app.before_request
def before_request():
    """Log all requests"""
    if request.method != 'GET':
        print(f"[REQUEST] {request.method} {request.path}")

@app.after_request
def after_request(response):
    """Log all responses"""
    if response.status_code >= 400:
        print(f"[RESPONSE] {response.status_code} {request.path}")
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_courses()
    app.run(debug=True, host='0.0.0.0', port=5000)
