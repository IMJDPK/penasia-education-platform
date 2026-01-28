#!/usr/bin/env python3
"""
Clean up duplicate courses from database
Removes old course entries that have been replaced with updated versions
"""

from app import app, db, Course

def cleanup_duplicate_courses():
    """Remove duplicate/old course entries"""
    with app.app_context():
        print("🧹 Cleaning up duplicate courses from database...")
        print("="*60)
        
        # Keep only the three courses shown on homepage: 169, 171, 179
        # Delete all others
        courses_to_delete = [1, 180, 181, 182, 183]
        
        for course_id in courses_to_delete:
            course = Course.query.filter_by(id=course_id).first()
            if course:
                print(f"\n🗑️  Deleting Course {course_id}: {course.title}")
                db.session.delete(course)
            else:
                print(f"   ⚠️  Course {course_id} not found (already deleted)")
        
        # Commit changes
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("✅ Cleanup completed successfully!")
            print("="*60)
            
            # Display remaining courses
            print("\n📚 Remaining courses in database:")
            all_courses = Course.query.order_by(Course.id).all()
            for course in all_courses:
                print(f"\n   ID: {course.id}")
                print(f"   Title: {course.title}")
                print(f"   Fee: HK${course.fee_hkd}")
                print(f"   Duration: {course.duration_weeks} weeks")
            
            print(f"\n📊 Total courses: {len(all_courses)}")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during cleanup: {e}")
            return False
        
        return True

if __name__ == "__main__":
    print("\n🚀 Starting database cleanup...\n")
    success = cleanup_duplicate_courses()
    if success:
        print("\n✅ Cleanup completed! Old duplicate courses have been removed.")
        print("💡 Remember to reload your webapp on PythonAnywhere to see the changes.")
    else:
        print("\n❌ Cleanup failed. Please check the error messages above.")
