#!/usr/bin/env python3
"""
Sample data creation script for PenAsia Phase 2
This script populates the database with sample courses, students, and applications
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Course, CourseSchedule, Application, Enrollment
from datetime import datetime, date, time
import random

def create_sample_data():
    """Create sample data for demonstration"""
    with app.app_context():
        print("Creating sample data...")
        
        # Create sample courses
        courses_data = [
            {
                'course_code': 'HCM001',
                'title': 'Hotel Culinary Management (Level 4)',
                'description': 'Comprehensive program covering culinary arts, hotel management, and food service operations.',
                'duration_weeks': 52,
                'duration_hours': 1040,
                'fee_hkd': 88000.00,
                'cef_eligible': True,
                'cef_fee_hkd': 66000.00,
                'max_students': 20,
                'min_students': 8,
                'category': 'culinary',
                'level': 'intermediate',
                'is_featured': True
            },
            {
                'course_code': 'BTEC001',
                'title': 'BTEC Business Management (Level 5)',
                'description': 'International business qualification covering management principles and practices.',
                'duration_weeks': 78,
                'duration_hours': 1560,
                'fee_hkd': 96000.00,
                'cef_eligible': True,
                'cef_fee_hkd': 72000.00,
                'max_students': 25,
                'min_students': 10,
                'category': 'business',
                'level': 'advanced',
                'is_featured': True
            },
            {
                'course_code': 'WBP171',
                'title': 'Western Bakery & Pastry Skills',
                'description': 'Professional baking and pastry techniques for commercial kitchens.',
                'duration_weeks': 12,
                'duration_hours': 240,
                'fee_hkd': 18000.00,
                'cef_eligible': False,
                'max_students': 16,
                'min_students': 6,
                'category': 'culinary',
                'level': 'beginner',
                'is_featured': True
            },
            {
                'course_code': 'WC179',
                'title': 'Western Cuisine Fundamentals',
                'description': 'Essential Western cooking techniques and menu development.',
                'duration_weeks': 12,
                'duration_hours': 240,
                'fee_hkd': 16000.00,
                'cef_eligible': False,
                'max_students': 18,
                'min_students': 6,
                'category': 'culinary',
                'level': 'beginner'
            }
        ]
        
        # Create courses
        for course_data in courses_data:
            existing_course = Course.query.filter_by(course_code=course_data['course_code']).first()
            if not existing_course:
                course = Course(**course_data)
                db.session.add(course)
        
        db.session.commit()
        print("Created sample courses")
        
        # Create sample students
        students_data = [
            {'first_name': 'Emily', 'last_name': 'Chan', 'email': 'emily.chan@email.com'},
            {'first_name': 'Michael', 'last_name': 'Wong', 'email': 'michael.wong@email.com'},
            {'first_name': 'Sarah', 'last_name': 'Li', 'email': 'sarah.li@email.com'},
            {'first_name': 'David', 'last_name': 'Leung', 'email': 'david.leung@email.com'},
            {'first_name': 'Jessica', 'last_name': 'Tam', 'email': 'jessica.tam@email.com'},
        ]
        
        for student_data in students_data:
            existing_student = User.query.filter_by(email=student_data['email']).first()
            if not existing_student:
                student = User(
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name'],
                    email=student_data['email'],
                    role='student',
                    is_active=True,
                    email_verified=True,
                    phone=f"+852 9{random.randint(100,999)} {random.randint(1000,9999)}"
                )
                student.set_password('student123')
                db.session.add(student)
        
        db.session.commit()
        print("Created sample students")
        
        # Create course schedules
        courses = Course.query.all()
        for course in courses[:2]:  # Create schedules for first 2 courses
            schedule = CourseSchedule(
                course_id=course.id,
                start_date=date(2025, 9, 8),
                end_date=date(2025, 12, 1),
                day_of_week='monday',
                start_time=time(9, 0),
                end_time=time(17, 0),
                location='Main Campus',
                instructor='Prof. Johnson',
                registration_start=date(2025, 7, 1),
                registration_end=date(2025, 8, 31),
                is_active=True,
                status='upcoming'
            )
            db.session.add(schedule)
        
        db.session.commit()
        print("Created course schedules")
        
        # Create sample applications
        students = User.query.filter_by(role='student').all()
        courses = Course.query.all()
        
        for i, student in enumerate(students[:3]):
            application = Application(
                user_id=student.id,
                course_id=courses[i % len(courses)].id,
                education_level='secondary',
                motivation=f"I am very interested in {courses[i % len(courses)].title} because it aligns with my career goals.",
                how_did_you_hear='website',
                status=random.choice(['pending', 'approved', 'pending']),
                cef_application=random.choice([True, False])
            )
            if application.cef_application:
                application.hkid_number = f"A{random.randint(100000, 999999)}(0)"
            
            db.session.add(application)
        
        db.session.commit()
        print("Created sample applications")
        
        # Create sample enrollments for approved applications
        approved_apps = Application.query.filter_by(status='approved').all()
        # Use a different variable name to avoid shadowing the imported Flask `app`
        for approved_app in approved_apps:
            enrollment = Enrollment(
                user_id=approved_app.user_id,
                course_id=approved_app.course_id,
                application_id=approved_app.id,
                status='active',
                start_date=date(2025, 9, 8),
                expected_completion=date(2026, 6, 30),
                attendance_percentage=random.uniform(75, 95)
            )
            db.session.add(enrollment)
        
        db.session.commit()
        print("Created sample enrollments")
        
        print("✅ Sample data creation completed!")
        print("\nSample accounts created:")
        print("- Admin: admin@penasia.edu.hk / admin123")
        for student in students_data:
            print(f"- Student: {student['email']} / student123")

if __name__ == "__main__":
    create_sample_data()
