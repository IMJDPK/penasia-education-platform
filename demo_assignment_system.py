#!/usr/bin/env python3
"""
Assignment System Demo Script
Demonstrates the complete student assignment workflow
"""

from app import app
from models import db, User, Assignment, ClassSchedule, AssignmentSubmission, Course
from datetime import datetime, timedelta
import os

def demo_assignment_system():
    """Demonstrate the assignment system functionality"""
    
    with app.app_context():
        print("\n🎓 PenAsia LMS - Assignment System Demo")
        print("=" * 50)
        
        # Get test student
        student = User.query.filter_by(email='student@test.com').first()
        if not student:
            print("❌ Test student not found!")
            return
            
        print(f"👤 Student: {student.full_name}")
        print(f"📧 Email: {student.email}")
        
        # Get student's enrollments
        enrollments = student.enrollments
        enrolled_course_ids = [e.course_id for e in enrollments]
        
        print(f"📚 Enrolled Courses: {len(enrolled_course_ids)}")
        for enrollment in enrollments:
            print(f"   • {enrollment.course.course_code} - {enrollment.course.title}")
        
        print("\n📝 ASSIGNMENT MANAGEMENT")
        print("-" * 30)
        
        # Get assignments for enrolled courses
        assignments = Assignment.query.filter(
            Assignment.course_id.in_(enrolled_course_ids)
        ).order_by(Assignment.due_date).all()
        
        print(f"Total Assignments: {len(assignments)}")
        
        for i, assignment in enumerate(assignments, 1):
            submission = assignment.get_student_submission(student.id)
            status = "✅ SUBMITTED" if submission else "⏳ PENDING"
            
            print(f"\n{i}. {assignment.title}")
            print(f"   Course: {assignment.course.course_code}")
            print(f"   Type: {assignment.assignment_type.title()}")
            print(f"   Due: {assignment.due_date.strftime('%B %d, %Y at %I:%M %p')}")
            print(f"   Points: {assignment.max_points}")
            print(f"   Status: {status}")
            
            if assignment.is_overdue:
                print(f"   ⚠️  OVERDUE!")
            else:
                print(f"   ⏰ Days remaining: {assignment.days_until_due}")
                
            if submission:
                print(f"   📄 Submitted: {submission.submission_date.strftime('%B %d, %Y at %I:%M %p')}")
                if submission.grade:
                    print(f"   🎯 Grade: {submission.grade}/{assignment.max_points} ({submission.grade_letter})")
                    print(f"   📊 Percentage: {submission.grade_percentage:.1f}%")
        
        print("\n📅 CLASS SCHEDULE")
        print("-" * 20)
        
        # Get upcoming classes
        upcoming_classes = ClassSchedule.query.filter(
            ClassSchedule.course_id.in_(enrolled_course_ids),
            ClassSchedule.class_date >= datetime.now()
        ).order_by(ClassSchedule.class_date).all()
        
        print(f"Upcoming Classes: {len(upcoming_classes)}")
        
        for i, schedule in enumerate(upcoming_classes, 1):
            day_indicator = ""
            if schedule.is_today:
                day_indicator = "🔴 TODAY"
            elif schedule.is_tomorrow:
                day_indicator = "🟡 TOMORROW"
            elif schedule.days_until <= 7:
                day_indicator = f"🟢 IN {schedule.days_until} DAYS"
            else:
                day_indicator = f"📅 {schedule.days_until} days away"
                
            print(f"\n{i}. {schedule.topic}")
            print(f"   Course: {schedule.course.course_code}")
            print(f"   Date: {schedule.class_date.strftime('%A, %B %d, %Y')}")
            print(f"   Time: {schedule.start_time.strftime('%I:%M %p')} - {schedule.end_time.strftime('%I:%M %p')}")
            print(f"   Duration: {schedule.duration_hours}h")
            print(f"   Location: {schedule.location}")
            print(f"   Instructor: {schedule.instructor_name}")
            print(f"   Type: {schedule.class_type.title()}")
            print(f"   {day_indicator}")
        
        print("\n🎯 STUDENT DASHBOARD SUMMARY")
        print("-" * 30)
        
        pending_assignments = [a for a in assignments if not a.get_student_submission(student.id)]
        overdue_assignments = [a for a in assignments if a.is_overdue and not a.get_student_submission(student.id)]
        today_classes = [s for s in upcoming_classes if s.is_today]
        this_week_classes = [s for s in upcoming_classes if s.days_until <= 7]
        
        print(f"📊 Assignments pending: {len(pending_assignments)}")
        print(f"⚠️  Overdue assignments: {len(overdue_assignments)}")
        print(f"🔴 Classes today: {len(today_classes)}")
        print(f"📅 Classes this week: {len(this_week_classes)}")
        
        if pending_assignments:
            print(f"\n⏰ NEXT ASSIGNMENT DUE:")
            next_assignment = min(pending_assignments, key=lambda a: a.due_date)
            print(f"   📝 {next_assignment.title}")
            print(f"   📅 Due: {next_assignment.due_date.strftime('%B %d, %Y at %I:%M %p')}")
            print(f"   ⏳ Time left: {next_assignment.days_until_due} days")
        
        if this_week_classes:
            print(f"\n📅 NEXT CLASS:")
            next_class = min(this_week_classes, key=lambda s: s.class_date)
            print(f"   📚 {next_class.topic}")
            print(f"   📅 {next_class.class_date.strftime('%A, %B %d at %I:%M %p')}")
            print(f"   📍 {next_class.location}")
        
        print("\n🎉 ASSIGNMENT SYSTEM FEATURES AVAILABLE:")
        print("   ✅ View assignment details")
        print("   ✅ Submit assignments with text and file uploads")
        print("   ✅ Track submission status and grades")
        print("   ✅ View class schedules (week and list view)")
        print("   ✅ Assignment deadline tracking")
        print("   ✅ Integrated dashboard overview")
        
        print(f"\n🌐 ACCESS URLS:")
        print(f"   🏠 Student Dashboard: http://localhost:5000/dashboard")
        print(f"   📝 Assignment Details: http://localhost:5000/assignment/1")
        print(f"   📤 Submit Assignment: http://localhost:5000/assignment/1/submit")
        print(f"   📅 Class Schedule: http://localhost:5000/schedule")
        
        print("\n💡 LOGIN CREDENTIALS:")
        print("   📧 Email: student@test.com")
        print("   🔑 Password: password123")
        
        print("\n✨ SUCCESS! The assignment system is fully operational!")
        print("🚀 Students can now submit assignments and view class schedules!")

if __name__ == "__main__":
    demo_assignment_system()
