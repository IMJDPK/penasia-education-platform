# Website Rebranding & Changes Document
**Date:** December 4, 2025  
**Project:** University of PenAsia Website Transformation  
**Status:** Pending Implementation

---

## 📋 Executive Summary

Complete rebranding of PenAsia Continuing Education Centre to **University of PenAsia** with strategic business-focused positioning and streamlined course offerings.

### Key Changes:
1. **Branding:** "PenAsia Continuing Education Centre" → "University of PenAsia"
2. **Course Focus:** Limit to 2 courses (Pearson BTEC & Hotel Culinary Management)
3. **Positioning:** Business education with culinary experience
4. **New Features:** Admin-controlled Admissions Open/Closed banner
5. **Homepage Restructure:** Convert success stories to faculty section
6. **Visual Assets:** Replace all logos and update facility images

---

## 🎯 SECTION 1: BRANDING CHANGES

### 1.1 Name Changes (Complete Site-Wide Replacement)

#### Current References to Update:
| Location | Current Text | New Text |
|----------|-------------|----------|
| All Templates | "PenAsia Continuing Education Centre" | "University of PenAsia" |
| All Templates | "PenAsia School of Continuing Education" | "University of PenAsia" |
| All Templates | "盈亞持續教育中心" | "盈亞大學 (University of PenAsia)" |
| Meta Tags | "PenAsia Continuing Education Centre" | "University of PenAsia" |
| Footer | "PenAsia Continuing Education Centre" | "University of PenAsia" |
| Copyright | "© 2025 PenAsia Continuing Education Centre" | "© 2025 University of PenAsia" |

#### Files Requiring Updates:
- `templates/base.html` (Navigation, footer, meta tags - 8+ instances)
- `templates/index.html` (Hero, about, testimonials - 15+ instances)
- `templates/about.html` (Header, content - 5+ instances)
- `templates/courses.html` (Headers - 2+ instances)
- `templates/admissions.html` (Content - 3+ instances)
- `templates/faculty.html` (Content - 4+ instances)
- `templates/facilities.html` (Content - 2+ instances)
- `templates/student_life.html` (Content - 2+ instances)
- `templates/contact.html` (Content - 3+ instances)
- `templates/auth/` files (All login/register pages)
- `templates/admin/` files (Admin panel headers)
- `templates/dashboard/` files (Student dashboard)
- Email templates (if any)

**Total Estimated Changes:** 50+ instances across 20+ files

---

### 1.2 Logo Replacement

#### Current Logo Files (TO BE REMOVED):
```
static/images/penasia_logo.png
static/images/logos/penasia-logo-header.png
static/images/logos/penasia-logo-mobile.png
static/images/logos/penasia-logo-footer.png
static/images/logos/favicon-16x16.png
static/images/logos/favicon-32x32.png
```

#### New Logo Files (FROM ASSETS FOLDER):
**Action Required:** User to provide exact file names from assets folder

**Expected Files:**
- `university-of-penasia-logo-main.png` (Main header logo)
- `university-of-penasia-logo-mobile.png` (Mobile responsive)
- `university-of-penasia-favicon.png` (Browser icon)

#### Logo Update Locations:
1. **base.html** - Line 31: Main navbar logo
2. **index.html** - Hero section (if used)
3. **Footer** - Footer logo
4. **Email templates** - Email header logos
5. **Admin panel** - Admin dashboard logo
6. **Favicon links** - `<link>` tags in `<head>`

**Total Files:** 6+ template files

---

## 🎓 SECTION 2: COURSE RESTRUCTURING

### 2.1 Active Courses (Keep Only 2)

#### **COURSE 1: Pearson BTEC Higher National Diploma in Business**

**Course Details:**
- **Title:** Pearson BTEC Higher National Diploma in Business
- **Course Code:** BTEC-HND-BUS-2025
- **Duration:** 2 Years (4 Semesters)
- **Total Modules:** 16 (4 modules per semester)
- **Language:** English
- **Level:** Higher National Diploma
- **Accreditation:** Pearson BTEC (UK)

**16 BTEC Modules (From Attached Image):**

**Semester 1 (4 Modules):**
1. The Contemporary Business Environment
2. Marketing Processes and Planning
3. Management of Human Resources
4. Leadership and Management

**Semester 2 (4 Modules):**
5. Accounting Principles
6. Managing a Successful Business Project
7. Work Experience
8. Managing and Running a Small Business

**Semester 3 (4 Modules):**
9. Research Project
10. Organisational Behaviour Management
11. Statistics for Management
12. Human Resources – Value and Contribution to Organisational Success

**Semester 4 (4 Modules):**
13. Sales Management
14. International Marketing
15. Product Service and Development
16. (Module 16 - To be confirmed with client)

**Course Description (Business-Focused):**
"Our flagship business diploma program combines rigorous academic study with practical business skills. Accredited by Pearson UK, this internationally recognized qualification prepares students for global business careers with a unique foundation in hospitality management and culinary business operations."

**Key Features:**
- ✅ UK Pearson Accredited
- ✅ International Recognition
- ✅ Pathway to UK University Top-Up (Year 3)
- ✅ Business Management Core + Culinary Business Specialization
- ✅ Work Experience Component
- ✅ Research Project Portfolio

---

#### **COURSE 2: Hotel Culinary Management Diploma**

**Course Details:**
- **Title:** Hotel Culinary Management Diploma
- **Course Code:** HCMD-2025
- **Duration:** 18-24 months
- **Language:** English/Cantonese
- **Level:** Professional Diploma
- **Focus:** Business management for culinary professionals

**Course Description (Business-Focused):**
"A comprehensive business and culinary management program designed for aspiring hospitality entrepreneurs and hotel management professionals. This diploma combines culinary arts training with essential business skills including cost control, staff management, marketing, and operations - preparing graduates to manage high-end restaurants, hotels, and food service businesses."

**Key Business Modules:**
- Restaurant Business Management
- Cost Control & Financial Management
- Menu Engineering & Pricing Strategy
- Staff Management & Leadership
- Marketing & Customer Service
- Food Safety & Quality Management
- Supply Chain & Procurement
- Entrepreneurship in Hospitality

**Culinary Modules:**
- Professional Cooking Techniques
- International Cuisine
- Pastry & Baking Foundations
- Kitchen Operations & Safety
- Food Presentation & Plating

**Key Features:**
- ✅ Business-First Approach to Culinary Education
- ✅ Industry Placement in 5-Star Hotels
- ✅ Entrepreneurship Training
- ✅ CEF Reimbursable (Hong Kong)
- ✅ Professional Kitchen Training

---

### 2.2 Courses to Deactivate/Remove

**Action:** Set `is_active = False` or delete from database

**Courses to Remove:**
- Western Bakery Certificate
- Western Cuisine Certificate
- All other non-core programs
- Short courses/certificates not aligned with university positioning

**Database Action Required:**
```sql
UPDATE courses 
SET is_active = FALSE 
WHERE id NOT IN (
    SELECT id FROM courses 
    WHERE title LIKE '%BTEC%' 
    OR title LIKE '%Hotel Culinary Management%'
);
```

---

## 💼 SECTION 3: CONTENT STRATEGY - BUSINESS FOCUS

### 3.1 Vision Statement (NEW)

**Location:** Homepage - About Section

**Current Text:**
"盈亞持續教育中心 (PenAsia Continuing Education Centre) is a licensed educational institution committed to providing quality continuing education programs in Hong Kong."

**New Vision Statement:**
"University of PenAsia is the only institution in Hong Kong providing comprehensive business education with integrated culinary management experience. We prepare future business leaders and hospitality entrepreneurs through internationally recognized qualifications and real-world industry partnerships."

**Key Messaging Points:**
- ✅ Business education PRIMARY, culinary SECONDARY
- ✅ Entrepreneurship & leadership focus
- ✅ International recognition (Pearson BTEC)
- ✅ Industry connections & career outcomes
- ✅ Unique positioning: "Business + Culinary"

---

### 3.2 Homepage Content Rewrites

#### **Hero Section Title:**
**Current:** "Shaping tomorrow's global leaders"  
**Updated:** "Where Business Excellence Meets Culinary Innovation"

**Current Subtitle:** "A premier university in the heart of Asia, offering fast-track degrees in business, hospitality, and culinary arts."  
**Updated:** "Hong Kong's premier business university with specialized culinary management programs. Internationally accredited qualifications with 98% employment success."

---

#### **About Section (Line 130-136):**
**Current:** Focus on continuing education  
**New Focus:** Business university positioning

**Updated Content:**
```
<h2>About University of PenAsia</h2>
<p class="lead">盈亞大學 (University of PenAsia) is Hong Kong's pioneering business education institution offering the unique combination of rigorous business management training with specialized culinary and hospitality expertise.</p>

<p>As the only Hong Kong institution delivering Pearson BTEC Higher National Diplomas with integrated culinary management, we prepare graduates for leadership roles in global hospitality businesses, restaurant entrepreneurship, and hotel management.</p>

<div class="key-differentiators">
    <div class="differentiator">
        <i class="fas fa-trophy"></i>
        <h4>Unique Positioning</h4>
        <p>Business education enhanced with culinary management - a combination found nowhere else in Hong Kong</p>
    </div>
    <div class="differentiator">
        <i class="fas fa-globe-asia"></i>
        <h4>International Recognition</h4>
        <p>Pearson UK accredited qualifications accepted worldwide, with direct pathways to UK university degrees</p>
    </div>
    <div class="differentiator">
        <i class="fas fa-briefcase"></i>
        <h4>Career Success</h4>
        <p>98% employment rate with graduates in management roles at Peninsula, Shangri-La, and leading hospitality groups</p>
    </div>
</div>
```

---

#### **"Why Choose" Section (Line 294-351):**

**Current Title:** "Why Choose PenAsia?"  
**New Title:** "Why University of PenAsia?"

**Updated Content - Business Focus:**

**Point 1: Business Foundation**
- Icon: 💼 Briefcase
- Title: "Comprehensive Business Education"
- Content: "Our Pearson BTEC curriculum covers all core business disciplines - from financial management and marketing to operations and strategic leadership - with specialized modules in hospitality business and food service management."

**Point 2: Unique Culinary Integration**
- Icon: 🍳 + 💼
- Title: "Business Meets Culinary Excellence"
- Content: "The only program in Hong Kong combining rigorous business training with professional culinary skills. Perfect for future restaurant owners, hotel managers, and hospitality entrepreneurs."

**Point 3: International Pathways**
- Icon: 🌍 Globe
- Title: "Global Career Opportunities"
- Content: "BTEC qualifications are recognized worldwide. Graduates can pursue careers internationally or continue to UK universities for bachelor's degree completion (Year 3 entry)."

**Point 4: Industry Employment**
- Icon: 🏨 Building
- Title: "Premium Industry Partnerships"
- Content: "Direct connections to Hong Kong's top hotels and restaurants. Our graduates secure management positions at Peninsula, Shangri-La, Mandarin Oriental, and leading F&B establishments."

---

### 3.3 Course Page Content Updates

**File:** `templates/courses.html`

**Page Title:**  
**Current:** "Our Courses"  
**Updated:** "Our Business Programs"

**Subtitle:**  
**Current:** "Discover our comprehensive range of professional development programs"  
**Updated:** "Two flagship programs combining business excellence with hospitality expertise"

**Program Cards - Rewrite Descriptions:**

**BTEC Card Description:**
"The gold standard in business education. This 2-year Higher National Diploma covers 16 comprehensive business modules from accounting to international marketing, with unique specialization in hospitality and culinary business management. Recognized pathway to UK bachelor's degrees."

**Hotel Culinary Card Description:**
"Business management training for culinary professionals. Master the financial, operational, and leadership skills needed to run successful restaurants, hotels, and food service businesses. Combines hands-on culinary training with MBA-level business education."

---

## 🏠 SECTION 4: HOMEPAGE RESTRUCTURE

### 4.1 Student Success Stories → Faculty Section

**Current Section (Lines 393-438):**
- Title: "Student Success Stories"
- 3 testimonial cards
- Located after "Why Choose" section

**Action:** CONVERT to Faculty Showcase

**New Section Title:** "Learn from Industry Leaders"

**New Content Structure:**
```html
<section class="section-premium faculty-showcase">
    <div class="container-premium">
        <div class="text-center mb-5">
            <h2 class="section-title">World-Class Faculty</h2>
            <p class="section-subtitle">Our instructors bring decades of real-world business and culinary expertise from Hong Kong's most prestigious establishments</p>
        </div>
        
        <div class="grid-premium grid-3">
            <!-- Faculty Member 1 - Business -->
            <div class="faculty-card">
                <div class="faculty-image">
                    <img src="{{ url_for('static', filename='images/faculty/faculty_05.jpg') }}" alt="Dr. Sarah Lam">
                </div>
                <div class="faculty-info">
                    <h4>Dr. Sarah Lam, MBA, PhD</h4>
                    <p class="faculty-title">Program Director - Business Management</p>
                    <p class="faculty-credentials">
                        • 15 years in hotel management<br>
                        • Former Operations Manager, Shangri-La Hotels<br>
                        • PhD Business Administration, HKUST<br>
                        • Specialization: Strategic Management, Operations
                    </p>
                </div>
            </div>
            
            <!-- Faculty Member 2 - Culinary Business -->
            <div class="faculty-card">
                <div class="faculty-image">
                    <img src="{{ url_for('static', filename='images/faculty/faculty_02.jpg') }}" alt="Chef Alan Thompson">
                </div>
                <div class="faculty-info">
                    <h4>Chef Alan Thompson, CEC</h4>
                    <p class="faculty-title">Head Instructor - Culinary Management</p>
                    <p class="faculty-credentials">
                        • 20+ years executive chef experience<br>
                        • Former Executive Chef, The Peninsula Hong Kong<br>
                        • Certified Executive Chef (CEC)<br>
                        • Specialization: Fine Dining, Kitchen Operations
                    </p>
                </div>
            </div>
            
            <!-- Faculty Member 3 - Hospitality Business -->
            <div class="faculty-card">
                <div class="faculty-image">
                    <img src="{{ url_for('static', filename='images/faculty/faculty_06.jpg') }}" alt="Mr. James Wong">
                </div>
                <div class="faculty-info">
                    <h4>Mr. James Wong, MBA, CHE</h4>
                    <p class="faculty-title">Senior Lecturer - Hospitality Management</p>
                    <p class="faculty-credentials">
                        • 18 years hospitality management<br>
                        • Former F&B Director, Mandarin Oriental<br>
                        • MBA, Chinese University of Hong Kong<br>
                        • Specialization: Revenue Management, Marketing
                    </p>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-5">
            <a href="{{ url_for('faculty') }}" class="btn-primary-premium">Meet All Our Faculty</a>
        </div>
    </div>
</section>
```

**Visual Design:**
- Professional headshot photos
- Clean, corporate card design
- Emphasize credentials and industry experience
- Link to full faculty page

---

### 4.2 Hong Kong Success Stories Section

**Current Section (Lines 440-620):**
- Title: "Hong Kong Success Stories"
- 3 detailed success story cards
- Success stats grid
- Industry partner logos

**Action:** DELETE THIS ENTIRE SECTION

**Reason:** Redundant with first testimonial section. Faculty section takes priority for business positioning.

**Lines to Remove:** 440-620 (approximately 180 lines)

**Keep:** "Our Graduates Work At" partner logos section (Lines 596-615)

---

### 4.3 "Our Graduates Work At" Section

**Current Section (Lines 596-615):**
- Industry partner logos
- Text: "Our Graduates Work At:"

**Action:** KEEP & ENHANCE

**Updated Content:**
```html
<div class="industry-partners">
    <div class="container-premium">
        <h3 class="text-center mb-4">Our Graduates Hold Management Positions At:</h3>
        <p class="text-center text-muted mb-5">University of PenAsia alumni work as managers, executives, and business owners in Hong Kong's top hospitality companies</p>
        <div class="partner-logos">
            <div class="partner-logo">
                <div class="logo-placeholder">The Peninsula Hong Kong</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">Shangri-La Hotels</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">Mandarin Oriental</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">Four Seasons</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">Conrad Hong Kong</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">The Ritz-Carlton</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">Hyatt Hotels</div>
            </div>
            <div class="partner-logo">
                <div class="logo-placeholder">Rosewood Hong Kong</div>
            </div>
        </div>
    </div>
</div>
```

---

## ⚙️ SECTION 5: NEW FUNCTIONALITY - ADMISSIONS BANNER

### 5.1 Feature Requirements

**Feature:** Admin-controlled "Admissions Open" banner

**Functionality:**
- Display dynamic banner on homepage when admissions are open
- Admin can toggle ON/OFF from admin panel
- Banner shows above hero section
- Auto-hide when admissions closed

**Banner Design:**
```html
<!-- Admissions Open Banner (Conditional) -->
{% if site_settings.admissions_open %}
<div class="admissions-banner">
    <div class="container-premium">
        <div class="banner-content">
            <div class="banner-icon">
                <i class="fas fa-graduation-cap"></i>
            </div>
            <div class="banner-text">
                <h3>🎓 Admissions Now Open for {{ site_settings.intake_semester }}</h3>
                <p>Apply now for our BTEC Business and Hotel Culinary Management programs. Limited seats available.</p>
            </div>
            <div class="banner-cta">
                <a href="{{ url_for('apply') }}" class="btn-banner-primary">Apply Now</a>
                <a href="{{ url_for('admissions') }}" class="btn-banner-secondary">Learn More</a>
            </div>
        </div>
    </div>
</div>
{% endif %}
```

**CSS Styling:**
```css
.admissions-banner {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 20px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    animation: slideDown 0.5s ease-out;
}

.banner-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}

.banner-icon i {
    font-size: 3rem;
    color: #ffd700;
}

.banner-text h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
}

.banner-text p {
    margin: 5px 0 0 0;
    opacity: 0.9;
}

.btn-banner-primary {
    background: #ffd700;
    color: #1e3c72;
    padding: 12px 30px;
    border-radius: 5px;
    font-weight: bold;
    text-decoration: none;
    transition: all 0.3s;
}

.btn-banner-primary:hover {
    background: #ffed4e;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
    .banner-content {
        flex-direction: column;
        text-align: center;
    }
}
```

---

### 5.2 Database Changes

**New Model:** `SiteSettings`

**File:** `models.py`

```python
class SiteSettings(db.Model):
    """Global site settings controlled by admin"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Admissions Control
    admissions_open = db.Column(db.Boolean, default=False, nullable=False)
    intake_semester = db.Column(db.String(50), default="Fall 2025")  # e.g., "Fall 2025", "Spring 2026"
    application_deadline = db.Column(db.Date)
    
    # Banner Customization
    banner_title = db.Column(db.String(200))
    banner_message = db.Column(db.Text)
    banner_enabled = db.Column(db.Boolean, default=True)
    
    # Metadata
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<SiteSettings admissions_open={self.admissions_open}>'
```

**Migration Required:**
```bash
flask db migrate -m "Add SiteSettings model for admissions control"
flask db upgrade
```

---

### 5.3 Admin Panel Integration

**New Admin Route:** `/admin/settings`

**File:** `app.py`

```python
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    """Admin panel for site settings"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Get or create settings
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        # Update admissions status
        settings.admissions_open = request.form.get('admissions_open') == 'on'
        settings.intake_semester = request.form.get('intake_semester', 'Fall 2025')
        settings.banner_title = request.form.get('banner_title')
        settings.banner_message = request.form.get('banner_message')
        settings.banner_enabled = request.form.get('banner_enabled') == 'on'
        
        # Handle deadline
        deadline_str = request.form.get('application_deadline')
        if deadline_str:
            settings.application_deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        
        settings.updated_by = current_user.id
        
        db.session.commit()
        
        flash('Site settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', settings=settings)
```

**Template:** `templates/admin/settings.html`

```html
{% extends "admin/base.html" %}

{% block title %}Site Settings - Admin Panel{% endblock %}

{% block admin_content %}
<div class="card">
    <div class="card-header">
        <h3><i class="fas fa-cog"></i> Site Settings</h3>
    </div>
    <div class="card-body">
        <form method="POST">
            <div class="admissions-control-section mb-5">
                <h4>Admissions Control</h4>
                
                <div class="form-check form-switch mb-3">
                    <input class="form-check-input" type="checkbox" id="admissionsOpen" 
                           name="admissions_open" {% if settings.admissions_open %}checked{% endif %}>
                    <label class="form-check-label" for="admissionsOpen">
                        <strong>Admissions Open</strong>
                        <p class="text-muted small">Toggle to show/hide admissions banner on homepage</p>
                    </label>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="intakeSemester" class="form-label">Intake Semester</label>
                        <input type="text" class="form-control" id="intakeSemester" 
                               name="intake_semester" value="{{ settings.intake_semester }}" 
                               placeholder="e.g., Fall 2025, Spring 2026">
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="applicationDeadline" class="form-label">Application Deadline</label>
                        <input type="date" class="form-control" id="applicationDeadline" 
                               name="application_deadline" 
                               value="{{ settings.application_deadline.strftime('%Y-%m-%d') if settings.application_deadline else '' }}">
                    </div>
                </div>
            </div>
            
            <div class="banner-customization-section mb-5">
                <h4>Banner Customization</h4>
                
                <div class="form-check form-switch mb-3">
                    <input class="form-check-input" type="checkbox" id="bannerEnabled" 
                           name="banner_enabled" {% if settings.banner_enabled %}checked{% endif %}>
                    <label class="form-check-label" for="bannerEnabled">
                        <strong>Enable Custom Banner</strong>
                    </label>
                </div>
                
                <div class="mb-3">
                    <label for="bannerTitle" class="form-label">Banner Title (Optional)</label>
                    <input type="text" class="form-control" id="bannerTitle" 
                           name="banner_title" value="{{ settings.banner_title or '' }}" 
                           placeholder="Custom banner headline">
                </div>
                
                <div class="mb-3">
                    <label for="bannerMessage" class="form-label">Banner Message (Optional)</label>
                    <textarea class="form-control" id="bannerMessage" name="banner_message" 
                              rows="3" placeholder="Custom banner message">{{ settings.banner_message or '' }}</textarea>
                </div>
            </div>
            
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg">
                    <i class="fas fa-save"></i> Save Settings
                </button>
            </div>
        </form>
        
        <!-- Preview Section -->
        <div class="preview-section mt-5">
            <h4>Banner Preview</h4>
            <div class="alert alert-info">
                <strong>Current Status:</strong> 
                {% if settings.admissions_open %}
                    <span class="badge bg-success">Admissions OPEN</span> - Banner is visible on homepage
                {% else %}
                    <span class="badge bg-secondary">Admissions CLOSED</span> - Banner is hidden
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

### 5.4 Context Processor

**Add to `app.py`:**

```python
@app.context_processor
def inject_site_settings():
    """Inject site settings into all templates"""
    settings = SiteSettings.query.first()
    if not settings:
        # Create default settings
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    return dict(site_settings=settings)
```

---

## 🖼️ SECTION 6: FACILITY IMAGES UPDATE

### 6.1 Current Images (TO BE REPLACED)

**Current Facility Images:**
```
static/images/facilities/facilities_01.jpg
static/images/facilities/facilities_02.jpg
static/images/facilities/facilities_03.jpg
static/images/facilities/facilities_04.jpg
```

**Status:** Placeholder or stock images

---

### 6.2 New Original Images (FROM ASSETS FOLDER)

**Action Required:** User to provide image file names from assets folder

**Expected New Images:**
- Professional kitchen photos
- Classroom facilities
- Campus exterior
- Student common areas
- Computer/tech labs
- Training facilities

**Naming Convention (Recommended):**
```
uop-facility-kitchen-01.jpg
uop-facility-kitchen-02.jpg
uop-facility-classroom-01.jpg
uop-facility-classroom-02.jpg
uop-facility-campus-exterior.jpg
uop-facility-common-area.jpg
uop-facility-computer-lab.jpg
```

---

### 6.3 Images to Update Across Site

**Homepage Uses:**
- Hero background (consider new facility photo)
- About section images
- Facility showcase

**Facilities Page Uses:**
- All facility cards
- Gallery sections

**Course Pages Uses:**
- Course detail background images
- Training facility showcases

**Total Image Replacements:** 15-20 instances across 5-6 pages

---

## 📧 SECTION 7: EMAIL & COMMUNICATIONS

### 7.1 Email Template Updates

**Files to Update:**
- All email templates mentioning "PenAsia Continuing Education Centre"
- Email signatures
- Automated notifications
- Application confirmations

**Key Email Types:**
1. Application confirmation emails
2. Acceptance letters
3. Course enrollment confirmations
4. Password reset emails
5. Newsletter templates
6. Admin notifications

**Email Signature Template:**
```
---
University of PenAsia
盈亞大學

Education License: #593958
1/F, Block C, Cho Yiu Centre
Kwai Chung, Hong Kong

T: (852) 2529 6138
E: info@penasia.edu.hk
W: www.penasia.edu.hk
---
```

---

## 🎨 SECTION 8: VISUAL DESIGN UPDATES

### 8.1 Color Scheme (Consider Update)

**Current Colors:**
```css
--primary-color: #0066cc;
--secondary-color: #f8f9fa;
--accent-color: #ff6b35;
```

**Recommendation for University Positioning:**
```css
--primary-color: #1e3c72;  /* Professional Navy Blue */
--secondary-color: #2a5298; /* Corporate Blue */
--accent-color: #ffd700;   /* Gold/Academic Excellence */
--text-dark: #333333;
--text-light: #6c757d;
```

**Files to Update:**
- `static/css/style.css`
- `static/css/premium-styles.css`

---

### 8.2 Typography Updates

**Consider:** More corporate, academic typography

**Recommended Fonts:**
- **Headings:** Playfair Display, Merriweather, or Lora (serif - academic)
- **Body:** Roboto, Open Sans, or Inter (sans-serif - modern)

**Implementation:**
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
}

body, p, a, span {
    font-family: 'Inter', sans-serif;
}
```

---

## 📱 SECTION 9: MOBILE RESPONSIVENESS

### 9.1 Admissions Banner Mobile View

**Ensure:**
- Banner stacks vertically on mobile
- CTA buttons full-width on small screens
- Text remains readable
- No horizontal scroll

**Test on:**
- iPhone (375px)
- Android (360px)
- Tablet (768px)

---

## 🗄️ SECTION 10: DATABASE MODIFICATIONS

### 10.1 Required Migrations

**1. SiteSettings Table**
```sql
CREATE TABLE site_settings (
    id INTEGER PRIMARY KEY,
    admissions_open BOOLEAN DEFAULT 0,
    intake_semester VARCHAR(50) DEFAULT 'Fall 2025',
    application_deadline DATE,
    banner_title VARCHAR(200),
    banner_message TEXT,
    banner_enabled BOOLEAN DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER REFERENCES user(id)
);
```

**2. Course Table Updates**
```sql
-- Add semester structure for BTEC
ALTER TABLE courses ADD COLUMN semester_1_modules TEXT;
ALTER TABLE courses ADD COLUMN semester_2_modules TEXT;
ALTER TABLE courses ADD COLUMN semester_3_modules TEXT;
ALTER TABLE courses ADD COLUMN semester_4_modules TEXT;
ALTER TABLE courses ADD COLUMN total_modules INTEGER;
ALTER TABLE courses ADD COLUMN accreditation_body VARCHAR(100);
ALTER TABLE courses ADD COLUMN international_recognition BOOLEAN DEFAULT 0;
```

**3. Deactivate Non-Core Courses**
```sql
UPDATE courses 
SET is_active = 0, 
    deactivated_at = CURRENT_TIMESTAMP
WHERE title NOT LIKE '%BTEC%' 
AND title NOT LIKE '%Hotel Culinary Management%';
```

---

## 🔧 SECTION 11: IMPLEMENTATION CHECKLIST

### Phase 1: Critical (Week 1)
- [ ] Replace all "PenAsia Continuing Education Centre" with "University of PenAsia"
- [ ] Update logo in all templates (base.html, index.html, footer)
- [ ] Update meta tags and page titles
- [ ] Deactivate non-core courses
- [ ] Update course descriptions (business-focused)
- [ ] Create SiteSettings model
- [ ] Implement admissions banner

### Phase 2: Content (Week 1-2)
- [ ] Rewrite vision statement
- [ ] Update homepage hero section
- [ ] Convert success stories to faculty section
- [ ] Delete redundant Hong Kong stories section
- [ ] Enhance "Our graduates work at" section
- [ ] Update all course page content
- [ ] Add 16 BTEC modules to course detail

### Phase 3: Visual Assets (Week 2)
- [ ] Replace all logos with new University of PenAsia logo
- [ ] Update facility images with original photos
- [ ] Update favicon
- [ ] Test responsive design on all devices
- [ ] Verify image optimization

### Phase 4: Admin Features (Week 2-3)
- [ ] Create admin settings page
- [ ] Add admissions toggle functionality
- [ ] Create context processor for site settings
- [ ] Test banner show/hide functionality
- [ ] Add admin navigation link

### Phase 5: Testing & QA (Week 3)
- [ ] Test all pages for branding consistency
- [ ] Verify course filtering (only 2 courses shown)
- [ ] Test admissions banner on/off
- [ ] Mobile responsiveness testing
- [ ] Cross-browser testing
- [ ] SEO audit (meta tags, descriptions)
- [ ] Accessibility audit

### Phase 6: Deployment (Week 3-4)
- [ ] Backup current database
- [ ] Run database migrations on production
- [ ] Deploy code to PythonAnywhere
- [ ] Update environment variables
- [ ] Verify all changes on live site
- [ ] Monitor for errors

---

## 📊 SECTION 12: FILE CHANGES SUMMARY

### Templates to Modify (22 Files)

**Core Templates:**
1. `templates/base.html` - Logo, navigation, footer (Critical)
2. `templates/index.html` - Hero, about, faculty section (Critical)
3. `templates/courses.html` - Course listings (Critical)
4. `templates/about.html` - About content (High Priority)
5. `templates/admissions.html` - Admissions info (High Priority)
6. `templates/contact.html` - Contact info (Medium)
7. `templates/faculty.html` - Faculty content (Medium)
8. `templates/facilities.html` - Facility images (Medium)
9. `templates/student_life.html` - Content updates (Low)

**Course Templates:**
10. `templates/course_detail.html` - BTEC modules (Critical)
11. `templates/course_detail_premium.html` - Module listing (Critical)

**Auth Templates:**
12. `templates/auth/login.html` - Branding
13. `templates/auth/register.html` - Branding

**Admin Templates:**
14. `templates/admin/dashboard.html` - Branding
15. `templates/admin/settings.html` - NEW FILE (Critical)
16. `templates/admin/base.html` - Logo update

**Dashboard Templates:**
17. `templates/dashboard/student_dashboard.html` - Branding
18. `templates/dashboard/instructor_dashboard.html` - Branding

**Other:**
19. `templates/privacy.html` - Footer branding
20. `templates/terms.html` - Footer branding
21. `templates/consultation.html` - Branding
22. `templates/apply.html` - Course filtering

---

### Python Files to Modify (3 Files)

1. **`app.py`** (Critical)
   - Add SiteSettings routes
   - Add context processor
   - Update course filtering logic
   - Add admin settings route

2. **`models.py`** (Critical)
   - Add SiteSettings model
   - Update Course model (modules fields)

3. **`forms.py`** (Medium)
   - Add SiteSettings form (if needed)

---

### CSS Files to Modify (2 Files)

1. **`static/css/style.css`**
   - Add admissions banner styles
   - Update color scheme (optional)
   - Add faculty showcase styles

2. **`static/css/premium-styles.css`**
   - Update university positioning styles
   - Add banner animations

---

### Image Files to Replace (25+ Files)

**Logos:**
- Replace 6 logo files

**Facilities:**
- Replace 4-8 facility images

**Other:**
- Update favicon
- Update hero images (optional)

---

## 🚀 SECTION 13: DEPLOYMENT STEPS

### 13.1 Local Development

```bash
# 1. Create database migration
flask db migrate -m "Add SiteSettings and update Course model"
flask db upgrade

# 2. Create default site settings
python -c "
from app import app, db
from models import SiteSettings
with app.app_context():
    settings = SiteSettings(
        admissions_open=True,
        intake_semester='Fall 2025',
        banner_enabled=True
    )
    db.session.add(settings)
    db.session.commit()
    print('Default settings created')
"

# 3. Deactivate non-core courses
python -c "
from app import app, db
from models import Course
with app.app_context():
    Course.query.filter(
        ~Course.title.like('%BTEC%'),
        ~Course.title.like('%Hotel Culinary%')
    ).update({'is_active': False})
    db.session.commit()
    print('Non-core courses deactivated')
"

# 4. Test locally
flask run
```

---

### 13.2 PythonAnywhere Deployment

```bash
# SSH into PythonAnywhere console

# 1. Navigate to project
cd ~/penasia-education-platform

# 2. Pull latest changes
git pull origin main

# 3. Activate virtual environment
source flask_env/bin/activate

# 4. Install any new dependencies
pip install -r requirements.txt

# 5. Run migrations
flask db upgrade

# 6. Create default settings (if not exists)
python -c "from app import app, db; from models import SiteSettings; \
with app.app_context(): \
    if not SiteSettings.query.first(): \
        db.session.add(SiteSettings(admissions_open=True)); \
        db.session.commit()"

# 7. Reload web app
# Go to PythonAnywhere Web tab and click "Reload"
```

**PythonAnywhere API Alternative:**
```python
import requests

username = 'imjdpk'
token = '77050fab193b4b5672ea7bd549988bb104e42ae0'

# Reload web app via API
response = requests.post(
    f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/imjdpk.pythonanywhere.com/reload/',
    headers={'Authorization': f'Token {token}'}
)

if response.status_code == 200:
    print('Web app reloaded successfully')
else:
    print(f'Error: {response.status_code} - {response.content}')
```

---

## 📝 SECTION 14: CONTENT WRITING GUIDELINES

### 14.1 Tone & Voice

**University of PenAsia Brand Voice:**
- **Professional:** Academic excellence, credible, established
- **Aspirational:** Career success, international opportunities
- **Business-Focused:** ROI, career outcomes, industry connections
- **Supportive:** Student success, mentorship, guidance

**Avoid:**
- Overly casual language
- Educational jargon without explanation
- Focus on "cooking" over "business management"
- Generic continuing education messaging

---

### 14.2 Key Messaging Framework

**Every page should reinforce:**

1. **Unique Value Proposition:**
   "The only institution in Hong Kong combining business education with culinary management"

2. **International Recognition:**
   "Pearson BTEC UK accredited qualifications accepted worldwide"

3. **Career Outcomes:**
   "98% employment rate in management roles at top hospitality brands"

4. **Business First:**
   "Business management education enhanced with culinary expertise"

---

### 14.3 SEO Keywords (Business Focus)

**Primary Keywords:**
- Business education Hong Kong
- BTEC Hong Kong
- Hospitality management degree Hong Kong
- Culinary business management
- Hotel management diploma
- Business university Hong Kong

**Secondary Keywords:**
- Pearson BTEC Hong Kong
- Culinary management certificate
- Restaurant business management
- UK university pathway Hong Kong
- Hospitality degree Hong Kong

---

## 🎯 SECTION 15: SUCCESS METRICS

### 15.1 Post-Launch KPIs

**Track:**
- Application submissions (target: +30% after rebranding)
- Bounce rate (target: <40%)
- Time on site (target: >3 minutes)
- Course inquiry form submissions
- "Apply Now" button clicks
- Admissions banner click-through rate

**Analytics Events to Set Up:**
- Banner interaction tracking
- Course page views (BTEC vs Hotel Culinary)
- Apply button clicks
- Faculty section engagement

---

## ✅ SECTION 16: FINAL DELIVERABLES

### 16.1 Documentation

- [x] This comprehensive changes document
- [ ] Updated README.md
- [ ] Admin user guide for admissions banner
- [ ] Content style guide
- [ ] Image asset catalog

### 16.2 Code Deliverables

- [ ] All template updates
- [ ] New SiteSettings model
- [ ] Admin settings page
- [ ] Database migrations
- [ ] Updated CSS/styling
- [ ] New logo files
- [ ] New facility images

### 16.3 Testing Deliverables

- [ ] Cross-browser test report
- [ ] Mobile responsiveness test
- [ ] Accessibility audit
- [ ] SEO audit report
- [ ] Performance metrics (PageSpeed)

---

## 🔄 SECTION 17: ROLLBACK PLAN

### 17.1 Backup Strategy

**Before Deployment:**
```bash
# Backup database
cp penasia.db penasia_backup_pre_rebrand_2025-12-04.db

# Backup static files
tar -czf static_backup_2025-12-04.tar.gz static/

# Git commit before changes
git add .
git commit -m "Pre-rebranding backup - 2025-12-04"
git tag "v1.0-pre-rebrand"
```

**Rollback Commands:**
```bash
# Revert code
git reset --hard v1.0-pre-rebrand

# Restore database
cp penasia_backup_pre_rebrand_2025-12-04.db penasia.db

# Restore static files
tar -xzf static_backup_2025-12-04.tar.gz
```

---

## 📞 SECTION 18: STAKEHOLDER SIGN-OFF

### 18.1 Required Approvals

**Before Implementation:**
- [ ] Branding approved (University of PenAsia name, logo)
- [ ] Vision statement approved
- [ ] Course descriptions approved
- [ ] Faculty section content approved
- [ ] Homepage layout approved
- [ ] New facility images reviewed

**Before Deployment:**
- [ ] Full site review completed
- [ ] Mobile view approved
- [ ] Admin panel tested
- [ ] Client final sign-off

---

## 📅 SECTION 19: TIMELINE

### Week 1 (Dec 4-10, 2025)
- Days 1-2: Branding updates (name, logo)
- Days 3-4: Course restructuring
- Days 5-7: Homepage content rewrites

### Week 2 (Dec 11-17, 2025)
- Days 1-3: Visual asset replacement
- Days 4-5: Admin features implementation
- Days 6-7: Initial testing

### Week 3 (Dec 18-24, 2025)
- Days 1-3: QA testing
- Days 4-5: Bug fixes
- Days 6-7: Final approval & deployment prep

### Week 4 (Dec 25-31, 2025)
- Day 1: Production deployment
- Days 2-7: Monitoring & optimization

---

## 🎓 CONCLUSION

This document provides a complete roadmap for transforming PenAsia Continuing Education Centre into University of PenAsia with strategic business positioning.

**Total Scope:**
- 50+ text replacements
- 22 template files
- 3 Python files
- 2 CSS files
- 25+ image replacements
- 1 new database model
- 1 new admin feature
- Complete content strategy

**Estimated Effort:** 80-100 development hours over 3-4 weeks

**Next Steps:**
1. Review and approve this document
2. Provide new logo files from assets folder
3. Provide new facility images from assets folder
4. Confirm final vision statement wording
5. Begin Phase 1 implementation

---

## 🔗 Site Credit

- Added footer credit: "Site developed by IMJD — YOUR DIGITAL MEDIA PARTNER" with link to https://imjd.asia in `templates/base.html`.


---

**Document Prepared By:** Development Team  
**Date:** December 4, 2025  
**Version:** 1.0  
**Status:** Pending Client Approval

---

**END OF DOCUMENT**
