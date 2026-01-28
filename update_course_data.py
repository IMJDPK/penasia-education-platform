#!/usr/bin/env python3
"""
Update Course Data in Database
Run this script to update course names, pricing, and details in the database
"""

from app import app, db, Course

def update_courses():
    """Update existing course records with new data"""
    with app.app_context():
        print("🔄 Updating course data in database...")
        print("="*60)
        
        # Update Certificate in Western Bakery & Pastry (Course ID 171)
        course_171 = Course.query.filter_by(id=171).first()
        if course_171:
            print(f"\n📝 Updating Course 171: {course_171.title}")
            course_171.title = 'Certificate in Western Bakery & Pastry'
            course_171.description = 'QF Level 2 certificate with hands-on practical training in Western baking techniques.'
            course_171.duration_weeks = 11
            course_171.duration_hours = 33
            course_171.fee_hkd = 12620
            course_171.certification = 'Certificate in Western Bakery & Pastry (QF Level 2)'
            print(f"   ✅ Updated: {course_171.title}")
            print(f"   💰 Fee: HK${course_171.fee_hkd}")
            print(f"   📅 Duration: {course_171.duration_weeks} weeks")
        else:
            print("   ⚠️  Course 171 not found in database")
        
        # Update Certificate in Starter and Main Course (Course ID 179)
        course_179 = Course.query.filter_by(id=179).first()
        if course_179:
            print(f"\n📝 Updating Course 179: {course_179.title}")
            course_179.title = 'Certificate in Starter and Main Course'
            course_179.description = 'Professional culinary skills training with focus on Western cooking techniques and presentation.'
            course_179.duration_weeks = 11
            course_179.duration_hours = 33
            course_179.fee_hkd = 12620
            course_179.certification = 'Certificate in Western Starter and Main Course (QF Level 2)'
            print(f"   ✅ Updated: {course_179.title}")
            print(f"   💰 Fee: HK${course_179.fee_hkd}")
            print(f"   📅 Duration: {course_179.duration_weeks} weeks")
        else:
            print("   ⚠️  Course 179 not found in database")
        
        # Commit changes
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("✅ Database updated successfully!")
            print("="*60)
            
            # Display all courses
            print("\n📚 All courses in database:")
            all_courses = Course.query.all()
            for course in all_courses:
                print(f"\n   ID: {course.id}")
                print(f"   Title: {course.title}")
                print(f"   Fee: HK${course.fee_hkd}")
                print(f"   Duration: {course.duration_weeks} weeks")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error updating database: {e}")
            return False
        
        return True

if __name__ == "__main__":
    print("\n🚀 Starting course data update...\n")
    success = update_courses()
    if success:
        print("\n✅ Update completed! Your courses page will now show the updated data.")
    else:
        print("\n❌ Update failed. Please check the error messages above.")
