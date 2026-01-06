#!/usr/bin/env python3
"""
Update course pricing and status in the database
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Course

def update_courses():
    """Update course pricing and activate all courses"""
    with app.app_context():
        print("Updating courses in database...")
        
        # Update or create Course 169: Hotel Culinary Management
        course169 = Course.query.filter_by(course_code='PSCE-DHM-5266').first()
        if course169:
            course169.fee_hkd = 125000
            course169.duration_weeks = 104  # 2 years
            course169.is_active = True
            print(f"Updated: {course169.title} - Fee: HK${course169.fee_hkd}")
        else:
            print("Course 169 not found - needs to be created")
        
        # Update or create Course 1: BTEC Business Management
        course1 = Course.query.filter_by(course_code='PSCE-BTB-5001').first()
        if course1:
            course1.fee_hkd = 118000
            course1.duration_weeks = 104  # 2 years
            course1.is_active = True
            print(f"Updated: {course1.title} - Fee: HK${course1.fee_hkd}")
        else:
            print("Course 1 not found - needs to be created")
        
        # Update Course 171: Western Bakery & Pastry - Make it active
        course171 = Course.query.filter_by(course_code='CEF-43C130000').first()
        if course171:
            course171.is_active = True
            course171.fee_hkd = 12620
            print(f"Updated: {course171.title} - Active: {course171.is_active}")
        else:
            print("Course 171 not found - needs to be created")
        
        # Update Course 179: Western Cuisine - Make it active
        course179 = Course.query.filter_by(course_code='CEF-43C15919A').first()
        if course179:
            course179.is_active = True
            course179.fee_hkd = 13200
            print(f"Updated: {course179.title} - Active: {course179.is_active}")
        else:
            print("Course 179 not found - needs to be created")
        
        # Commit changes
        db.session.commit()
        print("\n✅ All courses updated successfully!")
        
        # Display current courses
        print("\n📋 Current Course Status:")
        print("-" * 80)
        courses = Course.query.all()
        for course in courses:
            status = "✓ Active" if course.is_active else "✗ Inactive"
            print(f"{course.id:3d} | {course.course_code:15s} | {course.title:40s} | HK${float(course.fee_hkd):>10,.0f} | {status}")
        print("-" * 80)

if __name__ == '__main__':
    update_courses()
