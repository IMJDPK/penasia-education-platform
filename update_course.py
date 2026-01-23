#!/usr/bin/env python3
"""
Simple script to update the Hotel Culinary Management course data
Run this on PythonAnywhere after deployment to fix the course information
"""

from app import app, db, Course

def update_course():
    with app.app_context():
        # Find the course
        course = Course.query.filter_by(course_code='HCM001').first()

        if course:
            # Update with correct Level 3 information
            course.title = 'Hotel Culinary Management Diploma'
            course.level = 'QF Level 3'
            course.duration_weeks = 104
            course.duration_hours = 2080
            course.fee_hkd = 141000.00
            course.description = 'This comprehensive diploma program equips students with the essential skills and knowledge required for a successful career in hotel culinary management. Covering advanced culinary techniques, food safety standards, menu planning, cost control, and management principles, this program prepares graduates for supervisory and management roles in the hospitality industry.'
            course.learning_outcomes = 'Upon completion, students will be able to: Demonstrate advanced culinary skills and techniques, Apply food safety and hygiene standards, Develop and manage restaurant menus, Implement cost control measures, Lead kitchen operations and staff management'
            course.course_content = 'Advanced Culinary Techniques, Food Safety & Hygiene Management, Menu Planning & Development, Cost Control & Budgeting, Kitchen Operations Management, Staff Training & Leadership, Quality Assurance, Hospitality Industry Trends'
            course.assessment_method = 'Practical assessments, written examinations, project work, and continuous assessment throughout the program'
            course.certification = 'QF Level 3 Diploma in Hotel Culinary Management'
            course.category = 'culinary'
            course.is_active = True

            db.session.commit()
            print("✅ Course HCM001 updated successfully!")
            print(f"Title: {course.title}")
            print(f"Level: {course.level}")
            print(f"Duration: {course.duration_weeks} weeks")
            print(f"Fee: HKD {course.fee_hkd}")
        else:
            print("❌ Course HCM001 not found!")

if __name__ == '__main__':
    update_course()