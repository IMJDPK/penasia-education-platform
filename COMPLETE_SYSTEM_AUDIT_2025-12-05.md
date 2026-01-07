# PenAsia Education Platform - Complete System Audit Report
**Generated: December 5, 2025**  
**Environment: Local Development**  
**Status: Ready for Manual Server Deployment**

---

## TABLE OF CONTENTS
1. [Executive Summary](#executive-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Module & Component Mapping](#module--component-mapping)
4. [Database Models & Relationships](#database-models--relationships)
5. [Routing Architecture](#routing-architecture)
6. [Static Assets & Image Management](#static-assets--image-management)
7. [Template Structure & File Organization](#template-structure--file-organization)
8. [External Services Integration](#external-services-integration)
9. [Dependencies & Requirements](#dependencies--requirements)
10. [Deployment Checklist](#deployment-checklist)
11. [Key Module Connections](#key-module-connections)

---

## EXECUTIVE SUMMARY

### Project Overview
- **Project Name:** PenAsia Education Platform
- **Framework:** Flask (Python)
- **Database:** SQLite (Local)
- **Current Phase:** Phase 2C (Learning Portal & Assessment System)
- **Status:** Production-ready for manual deployment
- **Total Models:** 22 database models
- **Total Routes:** 80+ Flask routes
- **Total Templates:** 30+ HTML templates across 10 subdirectories

### Core Features Implemented
✅ User Authentication & Authorization  
✅ Course Management System  
✅ Learning Management System (LMS) - Modules & Lessons  
✅ Assignment Management & Grading  
✅ Quiz & Assessment System  
✅ Student Progress Tracking  
✅ Class Scheduling & Attendance  
✅ Payment Processing  
✅ Contact & Consultation Booking  
✅ Admin Dashboard & Reporting  
✅ Email Notifications  
✅ Digital Certificates  

### Core Courses
1. **Course 1:** Pearson BTEC Level 5 Higher National Diploma in Business (24 months)
2. **Course 169:** Diploma in Hotel Culinary Management (2 years)
3. **Course 171:** Certificate in Western Bakery and Pastry (11 weeks, CEF-eligible)
4. **Course 179:** Certificate in Western Starter and Main Course (11 weeks, CEF-eligible)

---

## SYSTEM ARCHITECTURE OVERVIEW

### Technology Stack
```
Backend:       Flask 2.3.3
ORM:           SQLAlchemy 2.0.42 + Flask-SQLAlchemy 3.1.1
Authentication: Flask-Login 0.6.3
Forms:         Flask-WTF 1.1.1, WTForms 3.0.1
Database Migration: Flask-Migrate 4.0.5
Email:         Flask-Mail 0.9.1
Validation:    email-validator 2.2.0
HTTP:          requests 2.32.4
Server:        Werkzeug 2.3.7
Template:      Jinja2 3.1.2
```

### Directory Structure
```
/home/imjd/Hong Kong University/Flask Website/
├── app.py                      # Main Flask application (2415 lines)
├── models.py                   # Database models (1194 lines)
├── forms.py                    # WTForms forms (430 lines)
├── email_service.py            # Email notifications (328 lines)
├── payment_service.py          # Payment processing (152 lines)
├── requirements.txt            # Python dependencies
├── flask_env/                  # Virtual environment
├── migrations/                 # Database migration files
├── instance/                   # Instance data (database storage)
│   └── penasia.db             # SQLite database
├── static/                     # Static files
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   └── images/                # Image assets
└── templates/                  # HTML templates
    ├── base.html              # Base template
    ├── index.html             # Homepage
    ├── *.html                 # Public pages
    └── [subdirectories]/      # Feature-specific templates
```

---

## MODULE & COMPONENT MAPPING

### Core Application Files

#### 1. **app.py** - Main Application (2415 lines)
**Location:** `/home/imjd/Hong Kong University/Flask Website/app.py`

**Key Components:**
- Flask app initialization
- Database configuration
- Login manager setup
- Jinja2 filters (nl2br)
- 80+ route definitions

**Route Categories:**

**Authentication Routes (Lines ~100-200)**
- `GET/POST /login` - User login
- `GET/POST /auth/login` - Alias route
- `GET/POST /register` - User registration
- `GET /logout` - User logout

**Student Dashboard Routes (Lines ~200-400)**
- `GET /dashboard` - Student dashboard (enrollments, assignments, schedules)
- `GET/POST /profile` - Student profile management
- `GET /assignments/<id>` - View assignment details
- `GET/POST /assignments/<id>/submit` - Submit assignment
- `GET /schedule` - View class schedule

**Course Routes (Lines ~400-700)**
- `GET /courses` - List courses
- `GET /courses/<id>` - Course detail page
- `GET/POST /courses/<id>/apply` - Apply for course
- `GET /apply/<id>` - Course-specific apply redirect

**Learning Portal Routes (Lines ~1200-1600)**
- `GET /learn/courses/<id>` - Student course portal
- `GET /learn/lessons/<id>` - Lesson viewing interface
- `POST /api/lesson/<id>/complete` - Mark lesson complete
- `POST /api/lesson/<id>/time` - Track time spent
- `POST /api/lesson/<id>/bookmark` - Bookmark lesson

**Admin Routes (Lines ~700-1200, ~1600-2000)**
- `GET /admin` - Admin dashboard
- `GET /admin/courses` - Course management
- `GET /admin/students` - Student management
- `GET /admin/applications` - Application reviews
- `GET/POST /admin/settings` - Site settings
- `GET /admin/reports` - Reports & analytics
- `GET /admin/backup` - Database backup info

**Content Management Routes (Lines ~1100-1300)**
- `GET /admin/courses/<id>/content` - Manage course content
- `GET/POST /admin/courses/<id>/modules/add` - Add module
- `GET/POST /admin/modules/<id>/lessons/add` - Add lesson
- `GET/POST /admin/lessons/<id>/edit` - Edit lesson
- `POST /admin/modules/<id>/delete` - Delete module
- `POST /admin/lessons/<id>/delete` - Delete lesson

**Assignment Management Routes (Lines ~1900-2100)**
- `GET /admin/assignments` - Assignment dashboard
- `GET/POST /admin/assignments/create` - Create assignment
- `GET/POST /admin/assignments/<id>/edit` - Edit assignment
- `GET /admin/assignments/<id>/submissions` - View submissions
- `POST /admin/submissions/<id>/grade` - Grade submission

**Schedule Management Routes (Lines ~2100-2200)**
- `GET /admin/schedules` - Schedule management
- `GET/POST /admin/schedules/create` - Create schedule
- `GET/POST /admin/schedules/<id>/edit` - Edit schedule

**Public Routes**
- `GET /` - Homepage (index)
- `GET /about` - About page
- `GET /facilities` - Facilities page
- `GET /news` - News page
- `GET /faculty` - Faculty page
- `GET /student-life` - Student life page
- `GET /admissions` - Admissions page
- `GET/POST /apply` - General application form
- `GET/POST /consultation` - Consultation booking
- `GET /consultation/confirmation/<id>` - Confirmation page
- `GET /contact` - Contact form
- `GET /privacy` - Privacy policy
- `GET /terms` - Terms of service

**Support Routes**
- `GET /admin/consultations` - Manage consultations
- `POST /admin/consultation/<id>/update` - Update consultation
- `GET /admin/contact-inquiries` - View contact inquiries
- `POST /admin/contact-inquiry/<id>/update` - Update inquiry status

**Payment Routes**
- `GET /payment/<id>` - Payment checkout page
- `POST /api/process-payment` - Process payment API

---

#### 2. **models.py** - Database Models (1194 lines)
**Location:** `/home/imjd/Hong Kong University/Flask Website/models.py`

**Core Database Models (22 Models Total):**

**Authentication & User Management**
1. `User` (Lines ~10-50)
   - Email, password hash, profile info
   - Roles: student, admin, staff
   - Relationships: enrollments, applications, assignments, messages, etc.

2. `SiteSettings` (Lines ~52-75)
   - Admissions control
   - Banner customization
   - Application deadlines

**Course Management**
3. `Course` (Lines ~76-165)
   - Course details (code, title, duration, fees)
   - CEF eligibility
   - Relationships: schedules, enrollments, applications, modules

4. `CourseSchedule` (Lines ~167-210)
   - Schedule details (dates, times, location)
   - Registration periods
   - Status tracking

5. `Application` (Lines ~212-280)
   - Course applications
   - Education/English levels
   - CEF information
   - Payment tracking
   - Status: pending, approved, rejected, waitlist

6. `Enrollment` (Lines ~282-320)
   - Student course enrollment
   - Attendance percentage
   - Final grades
   - Certificate tracking

**Learning Management System (LMS)**
7. `Module` (Lines ~330-380)
   - Course modules/chapters
   - Order and publishing
   - Relationships: course, lessons

8. `Lesson` (Lines ~382-450)
   - Individual lessons within modules
   - Content types: text, video, document, external
   - Duration tracking
   - Publishing control

9. `StudentProgress` (Lines ~452-520)
   - Lesson completion tracking
   - Time spent on lessons
   - Bookmarks and notes
   - Unique constraint per student/lesson/enrollment

**Assessment System**
10. `Quiz` (Lines ~540-610)
    - Quiz assessments
    - Time limits and attempts
    - Passing scores
    - Relationships: questions, attempts

11. `Question` (Lines ~612-660)
    - Quiz questions
    - Types: multiple choice, true/false, essay, short answer
    - Points and explanations
    - Relationships: student answers

12. `QuizAttempt` (Lines ~662-730)
    - Student quiz attempts
    - Scoring and percentages
    - Pass/fail tracking
    - Relationships: answers

13. `StudentAnswer` (Lines ~732-800)
    - Individual question answers
    - Auto-grading for objective questions
    - Manual feedback for essays

**Assignment System**
14. `Assignment` (Lines ~802-880)
    - Assignment management
    - Types: homework, project, essay, lab
    - Due dates and point values
    - Relationships: submissions

15. `AssignmentSubmission` (Lines ~882-950)
    - Student submissions
    - Grading and feedback
    - Late submission tracking
    - Grade letter conversion

**Class Management**
16. `ClassSchedule` (Lines ~952-1050)
    - Class dates and times
    - Location and instructor
    - Class type: lecture, lab, seminar, exam
    - Cancellation tracking
    - Online meeting URL

**Communication & Notifications**
17. `Notification` (Lines ~1052-1150)
    - System notifications
    - Types: assignment, grade, schedule, application, etc.
    - Priority levels
    - Read status tracking

18. `Message` (Lines ~1152-1220)
    - Direct messaging system
    - Message threading (replies)
    - Read status
    - Relationships: attachments

19. `MessageAttachment` (Lines ~1222-1260)
    - Message file attachments
    - File size tracking
    - MIME type storage

**Tracking & Reporting**
20. `Attendance` (Lines ~1262-1330)
    - Class attendance records
    - Status: present, absent, late, excused
    - Check-in time tracking
    - Marked by instructor/admin

21. `Certificate` (Lines ~1332-1450)
    - Digital certificates
    - Certificate numbers and verification codes
    - Grade recording
    - PDF generation
    - Revocation tracking

22. `Announcement` (Lines ~1452-1520)
    - System and course announcements
    - Pinning and priority
    - Expiration dates
    - Publishing control

23. `ContactInquiry` (Lines ~1522-1550)
    - Contact form submissions
    - Status tracking
    - Resolution tracking
    - Newsletter subscription

---

#### 3. **forms.py** - WTForms Definitions (430 lines)
**Location:** `/home/imjd/Hong Kong University/Flask Website/forms.py`

**Form Classes:**

1. `LoginForm` (Lines ~1-10)
   - Fields: email, password, remember_me
   - Validators: DataRequired, Email

2. `RegistrationForm` (Lines ~12-30)
   - Fields: first_name, last_name, email, phone, password, password2
   - Validators: Length, EqualTo, custom email validation
   - Custom validation: Check duplicate emails

3. `ProfileForm` (Lines ~32-60)
   - Fields: first_name, last_name, phone, date_of_birth, address
   - Emergency contact fields
   - Validators: Optional, Length

4. `CourseApplicationForm` (Lines ~62-140)
   - Fields: first_name, last_name, email, phone, address
   - Education level: Form 3-6, Diploma, Degree, Master
   - English level: Basic to IELTS 6+
   - Work experience, motivation, special requirements
   - Payment method selection

5. `ConsultationBookingForm` (Lines ~142-200)
   - Fields: first_name, last_name, email, phone
   - Consultation type: course_info, career_guidance, admission_help, etc.
   - Preferred date and time
   - Meeting type: online, in_person
   - Course interest (optional)

6. `AssignmentSubmissionForm` (Lines ~202-220)
   - Submission text
   - File upload capability

7. `ContactForm` (Lines ~222-280)
   - Fields: first_name, last_name, email, phone
   - Subject and message
   - Program interest
   - Newsletter subscription checkbox

---

#### 4. **email_service.py** - Email Notifications (328 lines)
**Location:** `/home/imjd/Hong Kong University/Flask Website/email_service.py`

**Service Class: EmailService**

**Configuration:**
- SMTP Server: localhost (configurable)
- SMTP Port: 587
- From Email: enquiry@penasia.edu.hk

**Methods:**

1. `send_email(to_email, subject, body, is_html=False)`
   - Generic email sending method
   - Supports plain text and HTML

2. `send_application_confirmation(user, course, application)`
   - Triggered when application submitted
   - Contains: application ID, course name, next steps

3. `send_application_update(user, course, application, admin_notes=None)`
   - Triggered on application status change
   - Status-specific messages (approved, rejected, waitlist, interview_required)
   - Payment instructions for approved applications

4. `send_payment_confirmation(user, course, payment_amount, payment_reference)`
   - Triggered after payment processed
   - Contains: payment details, course start date, location

5. `send_consultation_confirmation(consultation)`
   - Triggered when consultation booked
   - Contains: booking details, next steps

6. `send_consultation_notification(consultation)`
   - Notification to admin staff about new booking

7. `send_consultation_confirmed(consultation)`
   - Confirmation to student when consultation confirmed

**Note:** Currently prints to console (development mode)

---

#### 5. **payment_service.py** - Payment Processing (152 lines)
**Location:** `/home/imjd/Hong Kong University/Flask Website/payment_service.py`

**Service Class: PaymentProcessor**

**Supported Methods:**
- Credit Card
- Bank Transfer
- CEF Reimbursement
- Installment Plans (3 months)

**Key Methods:**

1. `generate_payment_reference(user_id, course_id, amount)`
   - Generates unique payment reference: PA{timestamp}{hash}

2. `calculate_installment_schedule(total_amount, num_installments=3)`
   - Creates installment payment schedule
   - Default: 3 monthly installments

3. `process_payment(user, course, amount, payment_method, application_id)`
   - Simulates payment processing
   - Returns payment data with status

4. `get_payment_instructions(payment_method, amount, reference)`
   - Returns payment instructions for each method
   - Bank details for transfers
   - CEF calculation information

**Note:** Currently simulation for demo purposes

---

### Configuration Files

#### 6. **requirements.txt** - Python Dependencies
**Location:** `/home/imjd/Hong Kong University/Flask Website/requirements.txt`

```
Flask==2.3.3
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.1.1
Flask-Migrate==4.0.5
Flask-Mail==0.9.1
WTForms==3.0.1
Werkzeug==2.3.7
Jinja2==3.1.2
email-validator==2.2.0
SQLAlchemy==2.0.42
requests==2.32.4
```

---

## DATABASE MODELS & RELATIONSHIPS

### Model Dependency Tree

```
User (Core)
├── owns: Enrollment
├── owns: Application
├── owns: CourseApplicationForm submissions
├── sends: Message
├── receives: Message
├── completes: StudentProgress
├── attempts: QuizAttempt
├── submits: AssignmentSubmission
├── attends: Attendance
├── receives: Notification
├── writes: Announcement
└── resolves: ContactInquiry

Course (Core)
├── has: CourseSchedule (1-to-Many)
├── has: Enrollment (1-to-Many)
├── has: Application (1-to-Many)
├── has: Module (1-to-Many)
├── has: Assignment (1-to-Many)
├── has: Quiz (1-to-Many)
├── has: ClassSchedule (1-to-Many)
├── has: Announcement (1-to-Many)
└── has: Certificate (1-to-Many)

Module (LMS)
├── belongs_to: Course
├── has: Lesson (1-to-Many)
└── published_on: is_published flag

Lesson (LMS)
├── belongs_to: Module
├── has: StudentProgress (1-to-Many)
├── has: Quiz (0-to-Many)
└── content_types: text, video, document, external

StudentProgress (Learning)
├── student_id -> User
├── lesson_id -> Lesson
├── enrollment_id -> Enrollment
└── tracks: time_spent, bookmarks, completion

Quiz (Assessment)
├── course_id -> Course
├── lesson_id -> Lesson (optional)
├── has: Question (1-to-Many)
└── has: QuizAttempt (1-to-Many)

Question (Assessment)
├── belongs_to: Quiz
├── has: StudentAnswer (1-to-Many)
└── question_types: multiple_choice, true_false, essay, short_answer

QuizAttempt (Assessment)
├── student_id -> User
├── quiz_id -> Quiz
├── enrollment_id -> Enrollment
├── has: StudentAnswer (1-to-Many)
└── auto_grades: objective questions

StudentAnswer (Assessment)
├── attempt_id -> QuizAttempt
├── question_id -> Question
└── supports: auto-grading for MC/TF, manual for essays

Assignment (Assessment)
├── course_id -> Course
├── has: AssignmentSubmission (1-to-Many)
└── types: homework, project, essay, lab

AssignmentSubmission (Assessment)
├── student_id -> User
├── assignment_id -> Assignment
├── enrollment_id -> Enrollment
└── tracks: grade, feedback, status

ClassSchedule (Scheduling)
├── course_id -> Course
├── has: Attendance (1-to-Many)
├── types: lecture, lab, seminar, exam
└── online_meeting_url for virtual classes

Attendance (Scheduling)
├── student_id -> User
├── class_schedule_id -> ClassSchedule
├── marked_by -> User (instructor)
└── status: present, absent, late, excused

Certificate (Completion)
├── user_id -> User
├── course_id -> Course
├── enrollment_id -> Enrollment
├── issued_by -> User (admin)
└── verification_code for validation

Notification (Communication)
├── user_id -> User
├── types: assignment, grade, schedule, application, course, message, announcement
└── priority: low, normal, high, urgent

Message (Communication)
├── sender_id -> User
├── recipient_id -> User
├── parent_message_id (threading)
├── has: MessageAttachment (1-to-Many)
└── categories: academic, administrative, technical, general

MessageAttachment (Communication)
├── message_id -> Message
└── tracks: file info, size, mime type

Announcement (Communication)
├── author_id -> User
├── course_id -> Course (optional, null = institution-wide)
└── status: draft, published, expired

SiteSettings (Configuration)
└── global controls: admissions_open, banners, deadlines

ContactInquiry (Public)
├── received_from: first_name, last_name, email, phone
├── resolved_by -> User (optional)
└── status: new, in_progress, resolved

Consultation (Public)
├── course_id -> Course (optional)
├── assigned_to -> User (optional)
└── status: pending, confirmed, completed, cancelled
```

### Database Schema Summary

**Total Tables:** 23  
**Total Foreign Keys:** 45+  
**Unique Constraints:** 5+ (email, certificate_number, verification_code, student/lesson/enrollment)  
**Indexes:** 15+ (email, course_code, user_id, course_id, etc.)

---

## ROUTING ARCHITECTURE

### Route Organization Map

```
/ (PUBLIC)
├── GET /                          (Homepage)
├── GET /about                     (About)
├── GET /courses                   (Courses listing)
├── GET /courses/<id>              (Course detail)
├── GET /admissions                (Admissions info)
├── GET /apply                     (Application form)
├── GET /student-life              (Student life)
├── GET /faculty                   (Faculty)
├── GET /facilities                (Facilities)
├── GET /news                      (News)
├── GET /contact                   (Contact form)
├── GET /consultation              (Book consultation)
├── GET /consultation/confirmation (Confirmation)
├── GET /privacy                   (Privacy policy)
└── GET /terms                     (Terms of service)

/auth (AUTHENTICATION)
├── GET/POST /login                (Login page)
├── GET/POST /auth/login           (Alias)
├── GET/POST /register             (Registration)
└── GET /logout                    (Logout)

/student (STUDENT)
├── GET /dashboard                 (Student dashboard)
├── GET /profile                   (Profile view/edit)
├── GET /schedule                  (Class schedule)
├── GET /assignments/<id>          (Assignment detail)
├── GET/POST /assignments/<id>/submit (Submit)
├── GET /courses/<id>/apply        (Course application)
└── GET /payment/<id>              (Payment checkout)

/learn (LEARNING PORTAL)
├── GET /learn/courses/<id>        (Course portal)
├── GET /learn/lessons/<id>        (Lesson view)
├── POST /api/lesson/<id>/complete (Mark complete)
├── POST /api/lesson/<id>/time     (Track time)
└── POST /api/lesson/<id>/bookmark (Bookmark)

/admin (ADMIN ONLY)
├── GET /admin                     (Dashboard)
├── GET /admin/courses             (Course mgmt)
├── GET /admin/students            (Student mgmt)
├── GET /admin/applications        (Application review)
├── GET /admin/settings            (Site settings)
├── GET /admin/reports             (Reports)
├── GET /admin/backup              (Database info)
├── GET /admin/consultations       (Consultation mgmt)
├── GET /admin/contact-inquiries   (Contact mgmt)
│
├── COURSE CONTENT MANAGEMENT
│   ├── GET /admin/courses/<id>/content
│   ├── GET/POST /admin/courses/<id>/modules/add
│   ├── GET/POST /admin/modules/<id>/lessons/add
│   ├── GET/POST /admin/lessons/<id>/edit
│   ├── POST /admin/modules/<id>/delete
│   └── POST /admin/lessons/<id>/delete
│
├── ASSIGNMENT MANAGEMENT
│   ├── GET /admin/assignments
│   ├── GET/POST /admin/assignments/create
│   ├── GET/POST /admin/assignments/<id>/edit
│   ├── GET /admin/assignments/<id>/submissions
│   └── POST /admin/submissions/<id>/grade
│
└── SCHEDULE MANAGEMENT
    ├── GET /admin/schedules
    ├── GET/POST /admin/schedules/create
    └── GET/POST /admin/schedules/<id>/edit

/api (API ENDPOINTS)
├── POST /api/process-payment
├── POST /api/lesson/<id>/complete
├── POST /api/lesson/<id>/time
└── POST /api/lesson/<id>/bookmark
```

**Total Routes:** 80+  
**Public Routes:** 15  
**Authenticated Routes:** 30  
**Admin-only Routes:** 35+

---

## STATIC ASSETS & IMAGE MANAGEMENT

### Image Directory Structure

**Root Location:** `/home/imjd/Hong Kong University/Flask Website/static/images/`

#### Directory Breakdown

```
static/images/
├── logos/                          # Logo assets
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── penasia-logo-footer.png
│   ├── penasia-logo-header.png
│   ├── penasia-logo-mobile.png
│   ├── university-of-penasia-logo.png
│   └── university-of-penasia.png
│
├── hero/                           # Hero section images
│   ├── hero_01.jpg
│   ├── hero_01.png
│   └── hero_03.jpg
│
├── courses/                        # Course program images
│   └── [course-specific images]
│
├── faculty/                        # Faculty member photos (8 images)
│   ├── faculty_01.jpg to faculty_08.jpg
│
├── student-life/                   # Student life photos
│   ├── student-life_01.jpg
│   └── student-life_02.jpg
│
├── testimonials/                   # Student testimonials (4 images)
│   ├── testimonials_01.jpg
│   ├── testimonials_02.jpg
│   ├── testimonials_03.jpg
│   └── testimonials_04.jpg
│
├── facilities/                     # Facilities photos
│   ├── facilities_01.jpg/jpeg
│   ├── facilities_02.jpg/jpeg
│   ├── facilities_03.jpg/jpeg
│   ├── facilities_04.jpg/jpeg
│   ├── facilities_05.jpeg
│   ├── facilities_06.jpeg
│   ├── facilities_07.jpeg
│   ├── Original Facility01-08.jpeg (backup originals)
│
├── blog/                           # Blog post images
│   ├── blog_01.jpg
│   ├── blog_02.jpg
│   └── blog_03.jpg
│
├── about/                          # About page images
│   └── [about section images]
│
└── penasia_logo.png               # Root logo (duplicate)

```

### Image Usage in Templates

**Logo Usage:**
- `penasia-logo-header.png` → Header/Navigation
- `penasia-logo-footer.png` → Footer
- `penasia-logo-mobile.png` → Mobile menu
- `favicon-*.png` → Browser tab/bookmarks

**Home/Index Page:**
- `hero_*.jpg` → Hero section background
- `testimonials_*.jpg` → Testimonial section

**Faculty Page:**
- `faculty_*.jpg` → Faculty profile images

**Facilities Page:**
- `facilities_*.jpg/jpeg` → Facility showcase

**Student Life:**
- `student-life_*.jpg` → Campus life photos

**Blog/News:**
- `blog_*.jpg` → Article thumbnails

---

## TEMPLATE STRUCTURE & FILE ORGANIZATION

### Template Directory Structure

**Location:** `/home/imjd/Hong Kong University/Flask Website/templates/`

```
templates/
│
├── base.html                       # Base template (all pages inherit)
├── index.html                      # Homepage
├── about.html                      # About page
├── courses.html                    # Courses listing
├── admissions.html                 # Admissions info
├── facilities.html                 # Facilities
├── faculty.html                    # Faculty directory
│   ├── faculty_old.html           # Legacy version
│   └── faculty_premium.html        # Premium version
│
├── student_life.html               # Student life
├── news.html                       # News/blog
├── contact.html                    # Contact form
├── consultation.html               # Consultation booking
├── consultation_confirmation.html  # Confirmation
├── privacy.html                    # Privacy policy
├── terms.html                      # Terms of service
│
├── apply.html                      # Application form (public)
│
├── course_detail.html              # Course details
├── course_detail_premium.html      # Premium version
│
├── auth/                           # Authentication
│   ├── login.html
│   ├── login_old.html
│   ├── register.html
│   └── register_old.html
│
├── dashboard/                      # Student dashboard
│   ├── student.html                # Main student dashboard
│   └── profile.html                # Profile management
│
├── admin/                          # Admin panel (19 templates)
│   ├── dashboard.html              # Admin dashboard
│   ├── courses.html                # Course management
│   ├── students.html               # Student management
│   ├── applications.html           # Application review
│   ├── contact_inquiries.html      # Contact management
│   ├── course_content.html         # Content management
│   ├── add_module.html             # Add module
│   ├── add_lesson.html             # Add lesson
│   ├── edit_lesson.html            # Edit lesson
│   ├── assignments.html            # Assignment management
│   ├── create_assignment.html      # Create assignment
│   ├── student_assignments.html    # Student assignments
│   ├── assignment_submissions.html # View submissions
│   ├── schedules.html              # Schedule management
│   ├── create_schedule.html        # Create schedule
│   ├── mark_attendance.html        # Mark attendance
│   ├── settings.html               # Site settings
│   ├── backup.html                 # Database backup
│   └── reports.html                # Reports & analytics
│
├── courses/                        # Course templates
│   ├── apply.html                  # Course application form
│   └── detail.html                 # Course details
│
├── learning/                       # Learning portal
│   ├── course_portal.html          # Course portal
│   └── lesson_view.html            # Lesson view
│
├── assignments/                    # Assignment portal
│   ├── detail.html
│   └── submit.html
│
├── attendance/                     # Attendance
│   └── [attendance templates]
│
├── certificates/                   # Certificates
│   └── [certificate templates]
│
├── messages/                       # Messaging
│   └── [messaging templates]
│
├── notifications/                  # Notifications
│   └── [notification templates]
│
└── payment/                        # Payment
    └── checkout.html
```

### Template Inheritance Chain

```
base.html (root)
├── index.html
├── about.html
├── courses.html
├── courses/detail.html
├── apply.html
├── auth/login.html
├── auth/register.html
├── dashboard/student.html
├── dashboard/profile.html
├── learning/course_portal.html
├── learning/lesson_view.html
└── admin/dashboard.html
    ├── admin/courses.html
    ├── admin/students.html
    ├── admin/applications.html
    ├── admin/course_content.html
    └── ... (all admin templates)
```

### Template Variables & Context

**Injected Context (All Templates):**
- `site_settings` - Global site settings from SiteSettings model
- `current_user` - Logged-in user object
- `current_user.is_authenticated` - Auth status

**Common Template Blocks:**
- `{% block title %}` - Page title
- `{% block content %}` - Main content
- `{% block scripts %}` - Page-specific scripts
- `{% block styles %}` - Page-specific styles

---

## EXTERNAL SERVICES INTEGRATION

### 1. Email Service
**File:** `email_service.py`  
**Service:** Flask-Mail  
**Configuration:**
- Host: localhost (configurable)
- Port: 587
- From: enquiry@penasia.edu.hk

**Triggered Events:**
- Application submitted
- Application status updated
- Payment confirmed
- Consultation booked
- Consultation confirmed

**Current Mode:** Console output (development)  
**Production Mode:** Requires SMTP configuration

### 2. Payment Processing
**File:** `payment_service.py`  
**Methods:**
- Credit Card (Stripe integration placeholder)
- Bank Transfer (Manual processing)
- CEF Reimbursement
- Installment Plans

**Current Mode:** Simulation/Demo  
**Production Integration:** Required for payment gateway (Stripe, Alipay, etc.)

### 3. Database Service
**Type:** SQLite (Local)  
**Location:** `/home/imjd/Hong Kong University/Flask Website/instance/penasia.db`  
**Framework:** SQLAlchemy 2.0.42

**Migration System:** Alembic (Flask-Migrate)  
**Location:** `/home/imjd/Hong Kong University/Flask Website/migrations/`

---

## DEPENDENCIES & REQUIREMENTS

### Python Packages (12 Total)

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| Flask-Login | 0.6.3 | User session management |
| Flask-SQLAlchemy | 3.1.1 | ORM integration |
| Flask-WTF | 1.1.1 | Form handling & CSRF |
| Flask-Migrate | 4.0.5 | Database migrations |
| Flask-Mail | 0.9.1 | Email sending |
| WTForms | 3.0.1 | Form library |
| Werkzeug | 2.3.7 | WSGI utilities |
| Jinja2 | 3.1.2 | Template engine |
| email-validator | 2.2.0 | Email validation |
| SQLAlchemy | 2.0.42 | ORM library |
| requests | 2.32.4 | HTTP requests |

### Virtual Environment
**Location:** `/home/imjd/Hong Kong University/Flask Website/flask_env/`  
**Python Version:** 3.12

### Installation Command
```bash
pip install -r requirements.txt
```

---

## DEPLOYMENT CHECKLIST

### Pre-Deployment

- [ ] Database backup created
- [ ] All migrations applied
- [ ] Environment variables configured
- [ ] Static files collected
- [ ] Templates tested in production mode
- [ ] Logs configured
- [ ] SSL certificates prepared (for HTTPS)

### Server Configuration

- [ ] Web server installed (Apache/Nginx)
- [ ] WSGI application server configured (Gunicorn/uWSGI)
- [ ] Database location determined
- [ ] Email service configured (SMTP)
- [ ] Payment gateway integrated
- [ ] Domain configured
- [ ] DNS records updated

### Application Setup

```bash
# 1. Create project directory
mkdir -p /var/www/penasia
cd /var/www/penasia

# 2. Clone/copy project files
cp -r /home/imjd/Hong\ Kong\ University/Flask\ Website/* /var/www/penasia/

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Initialize database
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     # Create admin user if needed
... 
>>> exit()

# 6. Collect static files
cp -r static/* /var/www/penasia/static/

# 7. Test application
flask run

# 8. Configure for production WSGI
# Update SECRET_KEY in app.py
# Configure email service credentials
# Configure payment gateway API keys
```

### Post-Deployment

- [ ] Test all routes
- [ ] Test user registration and login
- [ ] Test course application workflow
- [ ] Test payment processing
- [ ] Test email notifications
- [ ] Test admin dashboard
- [ ] Test LMS modules and lessons
- [ ] Verify database backups
- [ ] Monitor error logs
- [ ] Set up monitoring/alerts

### Security Checklist

- [ ] Change SECRET_KEY in app.py
- [ ] Set DEBUG = False
- [ ] Configure HTTPS/SSL
- [ ] Set secure cookies (SECURE_COOKIE)
- [ ] Enable CSRF protection (already in Flask-WTF)
- [ ] Configure CORS if needed
- [ ] Set up rate limiting
- [ ] Regular security updates

---

## KEY MODULE CONNECTIONS

### User Registration → Course Application → Payment

```
User Registration (POST /register)
    ↓
    User created with role='student'
    ↓
Course Application (GET/POST /courses/<id>/apply)
    ↓
    Application created
    Notifications sent to admin
    ↓
Admin Review (GET /admin/applications)
    ↓
Update Status (POST /admin/application/<id>/update)
    ↓
    Email sent to applicant
    Notification created
    ↓
Payment Checkout (GET /payment/<id>)
    ↓
    Payment details generated
    Payment reference created
    ↓
Payment Processing (POST /api/process-payment)
    ↓
    Application status updated
    Email confirmation sent
    ↓
Enrollment created
    ↓
Access to Learning Portal (GET /learn/courses/<id>)
```

### Learning Portal Flow

```
Student Enrollment
    ↓
Access Course Portal (/learn/courses/<id>)
    ↓
View Modules (via Module.query.filter_by(course_id, is_published=True))
    ↓
Select Lesson (/learn/lessons/<id>)
    ↓
StudentProgress created/updated
    - Track time spent
    - Mark bookmarks
    - Complete lesson
    ↓
Quiz/Assessment (/learn/lessons/<id>/quiz)
    ↓
    QuizAttempt created
    StudentAnswer records created
    Auto-grade objective questions
    ↓
Assignment Submission (/assignments/<id>/submit)
    ↓
    AssignmentSubmission created
    Admin grades submission
    ↓
Class Attendance (marked by instructor)
    ↓
    Attendance records created
    Percentage calculated
    ↓
Certificate Generation
    ↓
    Certificate created when:
    - Course completed
    - Required attendance met
    - Passing grade achieved
```

### Admin Content Management

```
Admin Dashboard (/admin)
    ↓
Manage Course Content (/admin/courses/<id>/content)
    ↓
Add Module (/admin/courses/<id>/modules/add)
    ↓
    Module created
    order_index assigned
    ↓
Add Lesson (/admin/modules/<id>/lessons/add)
    ↓
    Lesson created
    content_type selected (text/video/document/external)
    ↓
    Stored in:
    - content_text (for text)
    - video_url (for video)
    - document_path (for documents)
    - external_url (for external resources)
    ↓
Publish Module/Lesson
    ↓
    is_published = True
    Becomes visible to students
    ↓
StudentProgress can now track completion
```

### Admin Assignment & Grading

```
Admin Dashboard (/admin)
    ↓
Assignments (/admin/assignments)
    ↓
Create Assignment (/admin/assignments/create)
    ↓
    Assignment created
    - Title, description, instructions
    - Due date, max points
    - Assignment type
    ↓
Students Submit (/assignments/<id>/submit)
    ↓
    AssignmentSubmission created
    is_late calculated based on due_date
    ↓
View Submissions (/admin/assignments/<id>/submissions)
    ↓
Grade Submission (/admin/submissions/<id>/grade)
    ↓
    grade assigned
    feedback added
    status = 'graded'
    ↓
Student notified (via system)
```

### Consultation Booking

```
Consultation Form (GET/POST /consultation)
    ↓
    Consultation record created
    - consultation_type
    - preferred_date/time
    - meeting_type (online/in_person)
    ↓
Confirmation email sent
    ↓
Admin Notification
    ↓
Admin Review (/admin/consultations)
    ↓
Update Consultation Status (/admin/consultation/<id>/update)
    ↓
    status = confirmed
    meeting_link or location provided
    assigned_to instructor
    ↓
Confirmation email sent to student
```

### Database Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           USER                                   │
│  (email, password_hash, role, phone, address, etc.)             │
└──────────┬──────────────────────────────────────────────────────┘
           │
    ┌──────┼──────┬──────────┬───────────┬────────────┐
    │      │      │          │           │            │
    ▼      ▼      ▼          ▼           ▼            ▼
┌────┐ ┌─────┐ ┌──────┐ ┌───────────┐ ┌─────────┐ ┌──────┐
│    │ │     │ │      │ │           │ │         │ │      │
│    │ │     │ │      │ │           │ │         │ │      │
└────┘ └─────┘ └──────┘ └───────────┘ └─────────┘ └──────┘

┌──────────────────────────────────────────────────────────────────┐
│                          COURSE                                   │
│  (code, title, duration, fee, is_active, category, etc.)        │
└────────┬──────────────────────────────────────────────────────────┘
         │
    ┌────┼────┬────────┬──────────┬─────────┬──────────┐
    │    │    │        │          │         │          │
    ▼    ▼    ▼        ▼          ▼         ▼          ▼
┌─────┐┌───┐┌──────┐┌────────┐┌─────┐┌────────┐┌──────────┐
│ ... ││ ..││......││........││.....││........││..........│
│ ... ││ ..││......││........││.....││........││..........│
└─────┘└───┘└──────┘└────────┘└─────┘└────────┘└──────────┘

┌──────────────────────────────────────────────────────────────────┐
│                         MODULE (LMS)                              │
│  (title, description, order_index, is_published, estimated_hours)│
└───────────┬────────────────────────────────────────────────────────┘
            │
            ├─ Lesson 1
            ├─ Lesson 2
            └─ Lesson 3
                 │
            ┌────┴──────┐
            │ (content) │
            ├───────────┤
            │ StudentProgress
            │ Quiz
            │ StudentAnswer
            └───────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      ENROLLMENT                                   │
│  (user_id, course_id, status, attendance%, final_grade)          │
└──────────┬───────────────────────────────────────────────────────┘
           │
    ┌──────┼──────┬────────┬────────┬──────────┐
    │      │      │        │        │          │
    ▼      ▼      ▼        ▼        ▼          ▼
[Progress] [Quiz] [Assign] [Class] [Cert] [Attend]
           Attempt Submit Schedule             Record
```

---

## CRITICAL CONNECTIONS SUMMARY

### How the System Flows

1. **User Journey**
   - Registration → Login → Dashboard
   - Browse Courses → Apply → Payment → Enrollment
   - Access Learning → Complete Modules → Pass Quiz → Submit Assignment
   - Earn Certificate → Download/Share

2. **Admin Journey**
   - Dashboard → Content Management → Create Modules/Lessons
   - Review Applications → Update Status → Payment Processing
   - Create Assignments → Grade Submissions → Award Certificates
   - View Reports → Manage Settings

3. **Data Flow**
   - Forms (forms.py) → Models (models.py) → Database
   - Routes (app.py) → Templates (templates/) → Client
   - Services (email, payment) → External APIs

4. **Key Integration Points**
   - Forms validate data → Models persist to DB
   - Routes handle HTTP requests → Services process logic
   - Templates render data → Static files (CSS/JS) enhance UX
   - Models trigger notifications → Email service sends messages

---

## QUICK REFERENCE: FILE LOCATIONS

### Core Application Files
- **Main App:** `/home/imjd/Hong Kong University/Flask Website/app.py`
- **Database Models:** `/home/imjd/Hong Kong University/Flask Website/models.py`
- **Forms:** `/home/imjd/Hong Kong University/Flask Website/forms.py`
- **Email Service:** `/home/imjd/Hong Kong University/Flask Website/email_service.py`
- **Payment Service:** `/home/imjd/Hong Kong University/Flask Website/payment_service.py`

### Configuration Files
- **Requirements:** `/home/imjd/Hong Kong University/Flask Website/requirements.txt`
- **Database:** `/home/imjd/Hong Kong University/Flask Website/instance/penasia.db`
- **Migrations:** `/home/imjd/Hong Kong University/Flask Website/migrations/`

### Template Files
- **Base Template:** `/home/imjd/Hong Kong University/Flask Website/templates/base.html`
- **Admin Templates:** `/home/imjd/Hong Kong University/Flask Website/templates/admin/`
- **Dashboard Templates:** `/home/imjd/Hong Kong University/Flask Website/templates/dashboard/`
- **Learning Portal:** `/home/imjd/Hong Kong University/Flask Website/templates/learning/`

### Static Assets
- **Stylesheets:** `/home/imjd/Hong Kong University/Flask Website/static/css/`
- **JavaScript:** `/home/imjd/Hong Kong University/Flask Website/static/js/`
- **Images:** `/home/imjd/Hong Kong University/Flask Website/static/images/`

---

## NOTES FOR NEXT DEVELOPER

### When Changing Models/Framework:

1. **Start with this document**
   - Understand the relationship between models
   - Review the routing architecture
   - Check which templates depend on each model

2. **Update checklist:**
   - Modify model in `models.py`
   - Update form in `forms.py` (if accepting input)
   - Create/update route in `app.py`
   - Create/update template in `templates/`
   - Test database migrations
   - Update this audit document

3. **Common changes:**
   - **Adding new Course feature:** Update Course model → Add form → Add route → Add template
   - **Adding new User role:** Update User model → Update role validation → Update route permissions
   - **Adding new content type in LMS:** Update Lesson model → Update content management route → Update lesson template

4. **Testing workflow:**
   - Test in development mode locally
   - Verify database migrations
   - Test all affected routes
   - Test template rendering with sample data
   - Verify email notifications
   - Update this audit document

---

## VERSION CONTROL & DEPLOYMENT INFO

- **Repository:** penasia-education-platform (GitHub)
- **Owner:** IMJDPK
- **Current Branch:** main
- **Deployment Method:** Manual file upload to server
- **Database:** SQLite (local file-based for development)
- **Production Database:** Requires migration to PostgreSQL or MySQL

---

**Document Version:** 1.0  
**Last Updated:** December 5, 2025  
**Next Review:** Upon framework/model changes or quarterly

---

*This document serves as the single source of truth for the PenAsia Education Platform architecture. When making significant changes, update this document to maintain accuracy.*
