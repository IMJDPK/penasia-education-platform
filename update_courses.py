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
        
        # Update Hotel Culinary Management
        hotel = Course.query.filter_by(course_code='HCM001').first()
        if hotel:
            hotel.fee_hkd = 141000
            hotel.duration_weeks = 104  # 2 years
            hotel.is_active = True
            print(f"Updated: {hotel.title} - Fee: HK${hotel.fee_hkd}")
        else:
            print("Hotel Culinary (HCM001) not found - needs to be created")
        
        # Update BTEC Business Management
        btec = Course.query.filter_by(course_code='BTEC001').first()
        if btec:
            btec.fee_hkd = 118000
            btec.duration_weeks = 104  # 2 years
            btec.is_active = False
            btec.is_featured = False  # Ensure it's not featured on home page
            print(f"Updated: {btec.title} - Fee: HK${btec.fee_hkd}")
        else:
            print("BTEC Business (BTEC001) not found - needs to be created")
        
        # Update Western Bakery & Pastry - Make it active
        bakery = Course.query.filter_by(course_code='WBP171').first()
        if bakery:
            bakery.is_active = True
            bakery.fee_hkd = 12620
            print(f"Updated: {bakery.title} - Fee: HK${bakery.fee_hkd}")
        else:
            print("Western Bakery (WBP171) not found - needs to be created")
        
        # Update Western Cuisine - Make it active
        cuisine = Course.query.filter_by(course_code='WC179').first()
        if cuisine:
            cuisine.is_active = True
            cuisine.fee_hkd = 13200
            print(f"Updated: {cuisine.title} - Fee: HK${cuisine.fee_hkd}")
        else:
            print("Western Cuisine (WC179) not found - needs to be created")
        
        # Hide legacy duplicate courses
        print("\nHiding legacy duplicate courses...")
        
        # Hide legacy BTEC Business Management HND
        legacy_btec = Course.query.filter_by(course_code='PSCE-BTB-5001').first()
        if legacy_btec:
            legacy_btec.is_active = False
            legacy_btec.is_featured = False  # Ensure it's not featured on home page
            print(f"Hidden: {legacy_btec.title} (legacy duplicate)")
        
        # Hide legacy Hotel Culinary Management Diploma
        legacy_hotel = Course.query.filter_by(course_code='PSCE-DHM-5266').first()
        if legacy_hotel:
            legacy_hotel.is_active = False
            print(f"Hidden: {legacy_hotel.title} (legacy duplicate)")
        
        # Hide legacy Western Bakery & Pastry
        legacy_bakery = Course.query.filter_by(course_code='CEF-43C130000').first()
        if legacy_bakery:
            legacy_bakery.is_active = False
            print(f"Hidden: {legacy_bakery.title} (legacy duplicate)")
        
        # Hide legacy Western Cuisine Certificate
        legacy_cuisine = Course.query.filter_by(course_code='CEF-43C15919A').first()
        if legacy_cuisine:
            legacy_cuisine.is_active = False
            print(f"Hidden: {legacy_cuisine.title} (legacy duplicate)")
        
        # Commit changes
        db.session.commit()
        print("\n✅ All courses updated and duplicates hidden successfully!")
        
        # Display current courses
        print("\n📋 Current Course Status:")
        print("-" * 80)
        courses = Course.query.all()
        for course in courses:
            status = "✓ Active" if course.is_active else "✗ Inactive"
            print(f"{course.id:3d} | {course.course_code:15s} | {course.title:40s} | HK${float(course.fee_hkd):>10,.0f} | {status}")
        print("-" * 80)
        
        # Verify correct pricing by course code
        print("\n🔍 Verifying Pricing by Course Code:")
        errors = []
        
        hotel = Course.query.filter_by(course_code='HCM001').first()
        if hotel and float(hotel.fee_hkd) != 141000:
            errors.append(f"Hotel Culinary (code {hotel.course_code}) fee is {hotel.fee_hkd}, should be 141000")
        
        btec = Course.query.filter_by(course_code='BTEC001').first()
        if btec and float(btec.fee_hkd) != 118000:
            errors.append(f"BTEC Business (code {btec.course_code}) fee is {btec.fee_hkd}, should be 118000")
        
        bakery = Course.query.filter_by(course_code='WBP171').first()
        if bakery and float(bakery.fee_hkd) != 12620:
            errors.append(f"Western Bakery (code {bakery.course_code}) fee is {bakery.fee_hkd}, should be 12620")
        
        cuisine = Course.query.filter_by(course_code='WC179').first()
        if cuisine and float(cuisine.fee_hkd) != 13200:
            errors.append(f"Western Cuisine (code {cuisine.course_code}) fee is {cuisine.fee_hkd}, should be 13200")
        
        if errors:
            print("❌ PRICE ERRORS DETECTED:")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✅ All prices are CORRECT!")

if __name__ == '__main__':
    update_courses()
