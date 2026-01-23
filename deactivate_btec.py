#!/usr/bin/env python3
"""
Script to deactivate the BTEC course in the database.
"""

from app import app, db
from models import Course

def deactivate_btec_course():
    with app.app_context():
        # Find the BTEC course by course_code
        btec_course = Course.query.filter_by(course_code='BTEC001').first()

        if btec_course:
            btec_course.is_active = False
            db.session.commit()
            print(f"Deactivated BTEC course: {btec_course.title}")
        else:
            print("BTEC001 course not found in database")

        # Also check for any other BTEC courses and deactivate them
        btec_courses = Course.query.filter(Course.course_code.like('%BTEC%')).all()
        for course in btec_courses:
            if course.is_active:
                course.is_active = False
                print(f"Deactivated BTEC course: {course.title}")

        db.session.commit()
        print("All BTEC courses have been deactivated")

if __name__ == "__main__":
    deactivate_btec_course()