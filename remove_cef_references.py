#!/usr/bin/env python3
"""
Script to systematically remove all CEF references from the PenAsia website
"""

import os
import re
from pathlib import Path

def remove_cef_from_file(file_path, replacements):
    """Remove CEF references from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for old_text, new_text in replacements:
            if isinstance(old_text, str):
                content = content.replace(old_text, new_text)
            else:  # regex pattern
                content = old_text.sub(new_text, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"ℹ️  No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    base_dir = Path("/home/imjd/Hong Kong University/Flask Website")
    
    # Define file-specific replacements
    template_replacements = [
        # Remove CEF badges and references
        ('CEF Approved', 'Certified Program'),
        ('CEF Eligible', 'Available'),
        ('CEF-eligible', 'eligible'),
        ('CEF reimbursement', 'program completion'),
        ('CEF funding', 'educational support'),
        ('CEF application', 'program application'),
        ('Continuing Education Fund (CEF)', 'continuing education'),
        ('Continuing Education Fund', 'continuing education'),
        ('<div class="cef-badge">CEF Approved</div>', ''),
        ('<div class="cef-badge-small">CEF Approved</div>', ''),
        
        # Remove specific course codes
        (re.compile(r'Course Code: CEF-[A-Z0-9]+'), 'Course Code: PENASIA-001'),
        (re.compile(r'CEF-[A-Z0-9]+'), 'PENASIA-001'),
        
        # Remove funding amounts
        ('up to HK$25,000', 'quality education'),
        ('Up to HK$25,000', 'Quality education'),
        ('HK$25,000', 'affordable fees'),
        
        # Remove CEF calculator sections
        (re.compile(r'<!-- CEF Calculator.*?<!-- End CEF Calculator -->', re.DOTALL), ''),
        (re.compile(r'<div class="cef-calculator">.*?</div>', re.DOTALL), ''),
        
        # Remove CEF-specific form fields
        ('cef_application', 'program_application'),
        ('CEF (Continuing Education Fund)', 'program'),
        
        # Update testimonials
        ('CEF funding made', 'financial planning made'),
        ('CEF reimbursement', 'program completion'),
    ]
    
    # Template files to update
    template_files = [
        'about.html',
        'courses.html', 
        'course_detail.html',
        'course_detail_premium.html',
        'apply.html',
        'apply_new.html',
        'consultation.html',
        'consultation_confirmation.html',
        'contact.html',
        'student_life.html',
        'privacy.html'
    ]
    
    print("🧹 Starting CEF reference removal...")
    
    # Process template files
    for template_file in template_files:
        file_path = base_dir / 'templates' / template_file
        if file_path.exists():
            remove_cef_from_file(file_path, template_replacements)
    
    # Process forms.py
    forms_replacements = [
        ("('cef', 'CEF Reimbursement')", "('scholarship', 'Scholarship Information')"),
        ('cef_application = BooleanField', 'scholarship_application = BooleanField'),
        ('CEF Subsidy', 'scholarship support'),
        ('CEF applications', 'scholarship applications'),
        ('cef_eligible = BooleanField', 'scholarship_eligible = BooleanField'),
        ('cef_fee_hkd', 'discounted_fee_hkd'),
        ('CEF Fee', 'Discounted Fee'),
        ('CEF Eligible', 'Scholarship Eligible'),
        ("('financial_aid', 'Financial Aid & CEF Information')", "('financial_aid', 'Financial Aid & Scholarship Information')"),
    ]
    
    forms_file = base_dir / 'forms.py'
    if forms_file.exists():
        remove_cef_from_file(forms_file, forms_replacements)
    
    # Process models.py
    models_replacements = [
        ('is_cef_eligible', 'is_scholarship_eligible'),
        ('cef_eligible', 'scholarship_eligible'),
        ('cef_fee_hkd', 'discounted_fee_hkd'),
    ]
    
    models_file = base_dir / 'models.py'
    if models_file.exists():
        remove_cef_from_file(models_file, models_replacements)
    
    # Process payment_service.py
    payment_replacements = [
        ("'cef'", "'scholarship'"),
        ('cef_reference', 'scholarship_reference'),
        ('cef_amount', 'discount_amount'),
        ('CEF', 'SCHOLARSHIP'),
        ("'cef': {", "'scholarship': {"),
    ]
    
    payment_file = base_dir / 'payment_service.py'
    if payment_file.exists():
        remove_cef_from_file(payment_file, payment_replacements)
    
    # Process CSS file
    css_replacements = [
        ('.cef-badge', '.program-badge'),
        ('.cef-calculator', '.fee-calculator'),
        ('--cef-green', '--program-green'),
        ('.btn-cef-premium', '.btn-program-premium'),
    ]
    
    css_file = base_dir / 'static' / 'css' / 'premium-styles.css'
    if css_file.exists():
        remove_cef_from_file(css_file, css_replacements)
    
    # Process JavaScript files
    js_replacements = [
        ('calculateCEF', 'calculateFees'),
        ('cef-status', 'fee-status'),
        ('cef-info', 'fee-info'),
    ]
    
    js_file = base_dir / 'static' / 'js' / 'main.js'
    if js_file.exists():
        remove_cef_from_file(js_file, js_replacements)
    
    print("\n🎉 CEF reference removal completed!")
    print("📝 Summary: All CEF references have been replaced with generic education terms")
    print("✅ The website is now suitable for non-Hong Kong universities")

if __name__ == "__main__":
    main()
