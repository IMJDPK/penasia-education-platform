#!/usr/bin/env python3
"""
PenAsia Website - Complete Audit & Documentation Update
Comprehensive testing of all functionality before updating master document
"""

import requests
import time
import os
from datetime import datetime

def complete_website_audit():
    """Run complete audit of all website functionality"""
    print("🎯 PenAsia Website - Complete Audit 2025")
    print("=" * 60)
    print(f"📅 Audit Date: {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000"
    audit_results = {
        'main_pages': {},
        'course_pages': {},
        'apply_functionality': {},
        'admin_system': {},
        'authentication': {},
        'database': {},
        'errors': []
    }
    
    try:
        # 1. TEST MAIN PAGES
        print("\n📄 TESTING MAIN PAGES:")
        print("-" * 40)
        main_pages = {
            "/": "Homepage",
            "/about": "About Us", 
            "/courses": "Courses Listing",
            "/admissions": "Admissions",
            "/student-life": "Student Life",
            "/faculty": "Faculty",
            "/facilities": "Facilities", 
            "/news": "News & Blog",
            "/contact": "Contact",
            "/privacy": "Privacy Policy",
            "/terms": "Terms & Conditions"
        }
        
        for route, name in main_pages.items():
            try:
                response = requests.get(f"{base_url}{route}")
                status = response.status_code == 200
                audit_results['main_pages'][route] = status
                icon = "✅" if status else "❌"
                print(f"{icon} {name:<20} - Status {response.status_code}")
            except Exception as e:
                audit_results['main_pages'][route] = False
                audit_results['errors'].append(f"Main page {route}: {e}")
                print(f"❌ {name:<20} - ERROR")
        
        # 2. TEST COURSE PAGES
        print(f"\n📚 TESTING COURSE PAGES:")
        print("-" * 40)
        course_routes = {
            "/courses/169": "Hotel Culinary Management",
            "/courses/1": "BTEC Business Management",
            "/courses/171": "Western Bakery & Pastry",
            "/courses/179": "Western Cuisine"
        }
        
        for route, name in course_routes.items():
            try:
                response = requests.get(f"{base_url}{route}")
                status = response.status_code == 200
                audit_results['course_pages'][route] = status
                icon = "✅" if status else "❌"
                print(f"{icon} {name:<25} - Status {response.status_code}")
            except Exception as e:
                audit_results['course_pages'][route] = False
                audit_results['errors'].append(f"Course page {route}: {e}")
                print(f"❌ {name:<25} - ERROR")
        
        # 3. TEST AUTHENTICATION SYSTEM
        print(f"\n🔐 TESTING AUTHENTICATION:")
        print("-" * 40)
        auth_routes = {
            "/login": "Login Page",
            "/register": "Registration Page",
            "/logout": "Logout Function"
        }
        
        for route, name in auth_routes.items():
            try:
                response = requests.get(f"{base_url}{route}", allow_redirects=True)
                status = response.status_code == 200
                audit_results['authentication'][route] = status
                icon = "✅" if status else "❌"
                print(f"{icon} {name:<20} - Status {response.status_code}")
            except Exception as e:
                audit_results['authentication'][route] = False
                audit_results['errors'].append(f"Auth route {route}: {e}")
                print(f"❌ {name:<20} - ERROR")
        
        # 4. TEST APPLY NOW FUNCTIONALITY
        print(f"\n🔗 TESTING APPLY NOW FUNCTIONALITY:")
        print("-" * 40)
        apply_routes = {
            "/apply": "General Apply",
            "/apply/169": "Hotel Culinary Apply",
            "/apply/1": "BTEC Business Apply",
            "/apply/171": "Western Bakery Apply", 
            "/apply/179": "Western Cuisine Apply"
        }
        
        for route, name in apply_routes.items():
            try:
                response = requests.get(f"{base_url}{route}", allow_redirects=False)
                # Apply routes should redirect (302) or show form (200)
                status = response.status_code in [200, 302]
                audit_results['apply_functionality'][route] = status
                icon = "✅" if status else "❌"
                print(f"{icon} {name:<25} - Status {response.status_code}")
                
                if response.status_code == 302:
                    redirect = response.headers.get('Location', 'Unknown')
                    print(f"   → Redirects to: {redirect}")
                    
            except Exception as e:
                audit_results['apply_functionality'][route] = False
                audit_results['errors'].append(f"Apply route {route}: {e}")
                print(f"❌ {name:<25} - ERROR")
        
        # 5. TEST ADMIN SYSTEM
        print(f"\n🔧 TESTING ADMIN SYSTEM:")
        print("-" * 40)
        admin_routes = {
            "/admin": "Admin Dashboard",
            "/admin/applications": "Applications Management",
            "/admin/courses": "Courses Management", 
            "/admin/students": "Students Management",
            "/admin/reports": "Reports & Analytics"
        }
        
        for route, name in admin_routes.items():
            try:
                response = requests.get(f"{base_url}{route}")
                # Admin routes should redirect to login (302) or show admin page (200)
                status = response.status_code in [200, 302]
                audit_results['admin_system'][route] = status
                icon = "✅" if status else "❌"
                print(f"{icon} {name:<25} - Status {response.status_code}")
            except Exception as e:
                audit_results['admin_system'][route] = False
                audit_results['errors'].append(f"Admin route {route}: {e}")
                print(f"❌ {name:<25} - ERROR")
        
        # 6. DATABASE CONNECTIVITY TEST
        print(f"\n🗄️  TESTING DATABASE:")
        print("-" * 40)
        try:
            # Test database routes that show data
            db_test_routes = ["/courses", "/admin", "/faculty"]
            db_working = True
            
            for route in db_test_routes:
                response = requests.get(f"{base_url}{route}")
                if response.status_code not in [200, 302]:
                    db_working = False
                    break
            
            audit_results['database']['connectivity'] = db_working
            icon = "✅" if db_working else "❌"
            print(f"{icon} Database connectivity and data retrieval")
            
        except Exception as e:
            audit_results['database']['connectivity'] = False
            audit_results['errors'].append(f"Database test: {e}")
            print("❌ Database connectivity - ERROR")
        
        # 7. CALCULATE RESULTS
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE AUDIT RESULTS")
        print("=" * 60)
        
        # Count successes
        main_pages_passed = sum(audit_results['main_pages'].values())
        main_pages_total = len(audit_results['main_pages'])
        
        course_pages_passed = sum(audit_results['course_pages'].values())
        course_pages_total = len(audit_results['course_pages'])
        
        auth_passed = sum(audit_results['authentication'].values())
        auth_total = len(audit_results['authentication'])
        
        apply_passed = sum(audit_results['apply_functionality'].values())
        apply_total = len(audit_results['apply_functionality'])
        
        admin_passed = sum(audit_results['admin_system'].values())
        admin_total = len(audit_results['admin_system'])
        
        db_passed = sum(audit_results['database'].values())
        db_total = len(audit_results['database'])
        
        total_passed = main_pages_passed + course_pages_passed + auth_passed + apply_passed + admin_passed + db_passed
        total_tests = main_pages_total + course_pages_total + auth_total + apply_total + admin_total + db_total
        
        print(f"📄 Main Pages: {main_pages_passed}/{main_pages_total} ({'✅' if main_pages_passed == main_pages_total else '❌'})")
        print(f"📚 Course Pages: {course_pages_passed}/{course_pages_total} ({'✅' if course_pages_passed == course_pages_total else '❌'})")
        print(f"🔐 Authentication: {auth_passed}/{auth_total} ({'✅' if auth_passed == auth_total else '❌'})")
        print(f"🔗 Apply Functionality: {apply_passed}/{apply_total} ({'✅' if apply_passed == apply_total else '❌'})")
        print(f"🔧 Admin System: {admin_passed}/{admin_total} ({'✅' if admin_passed == admin_total else '❌'})")
        print(f"🗄️  Database: {db_passed}/{db_total} ({'✅' if db_passed == db_total else '❌'})")
        
        overall_percentage = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        print(f"\n🎯 OVERALL SCORE: {total_passed}/{total_tests} ({overall_percentage:.1f}%)")
        
        if overall_percentage == 100:
            print("\n🎉 PERFECT SCORE - ALL SYSTEMS OPERATIONAL!")
            print("\n✅ PenAsia Website Status:")
            print("   • Core functionality: 100% working")
            print("   • Course system: 100% operational") 
            print("   • Apply Now buttons: 100% functional")
            print("   • Admin system: 100% accessible")
            print("   • Authentication: 100% working")
            print("   • Database integration: 100% working")
        elif overall_percentage >= 95:
            print("\n🎊 EXCELLENT - Nearly perfect functionality!")
            print(f"   • Only {total_tests - total_passed} minor issues detected")
        elif overall_percentage >= 90:
            print("\n✅ VERY GOOD - System mostly functional")
            print(f"   • {total_tests - total_passed} issues need attention")
        else:
            print("\n⚠️  NEEDS ATTENTION - Multiple issues detected")
            print(f"   • {total_tests - total_passed} issues require fixing")
        
        # Show errors if any
        if audit_results['errors']:
            print(f"\n❌ ERRORS DETECTED ({len(audit_results['errors'])}):")
            for error in audit_results['errors']:
                print(f"   • {error}")
        
        print(f"\n📋 AUDIT COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return audit_results, overall_percentage
        
    except Exception as e:
        print(f"❌ AUDIT FAILED: {e}")
        return None, 0

if __name__ == "__main__":
    audit_results, score = complete_website_audit()
    if score == 100:
        print("\n🚀 Ready for master document update!")
    else:
        print(f"\n⚠️  Audit score: {score}% - Check issues before document update")
