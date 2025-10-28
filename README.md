# PenAsia Website - README

## Project Structure

This is a Flask-based website for PenAsia Continuing Education Centre featuring:

- **4 Core Courses**: Hotel Culinary Management, BTEC Business Management, Western Bakery, Western Cuisine
- **Multi-language Support**: English, Traditional Chinese, Simplified Chinese
- **Responsive Design**: Mobile-optimized with Bootstrap 5
- **Application System**: Complete application form with validation

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Development Server**:
   ```bash
   python app.py
   ```

3. **Access the Website**:
   Open http://localhost:5000 in your browser

## File Structure

```
Flask Website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── course_detail.html # Course detail pages
│   └── apply.html        # Application form
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Custom styles
│   ├── js/
│   │   └── main.js      # JavaScript functionality
│   └── images/          # Website images (to be added)
└── README.md           # This file
```

## Features Implemented

### Phase 1 (Current):
- ✅ Complete Flask application structure
- ✅ Homepage with hero carousel and course overview
- ✅ Individual course detail pages for all 4 courses
- ✅ Application form with validation
- ✅ Responsive navigation and footer
- ✅ Professional CSS styling
- ✅ JavaScript functionality

### Next Steps (Phase 1 Continuation):
- 📋 Add remaining page templates (about, faculty, facilities, etc.)
- 🖼️ Add 33 Phase 1 priority images
- 🎨 Implement image placeholders
- 🔧 Set up development tasks

## Course Information

### 1. Hotel Culinary Management (Course 169)
- 2-year full-time diploma
- HK$141,100 total fee
- September 2025 start

### 2. BTEC Business Management
- 24-month program
- HK$78,000 fee
- 4 intakes yearly

### 3. Western Bakery Certificate (Course 171)
- 11-week evening program
- HK$12,620 fee
- CEF reimbursable

### 4. Western Cuisine Certificate (Course 179)
- 11-week evening program
- HK$12,620 fee
- CEF reimbursable

## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: (To be implemented)
- **Deployment**: (To be configured)

## Development Notes

- All course information matches the master document specifications
- SEO-optimized meta descriptions included
- Accessibility features implemented
- Mobile-responsive design
- Form validation and user experience optimized

## Contact Information

PenAsia Continuing Education Centre
- Address: 1/F, Block C, Cho Yiu Centre, Kwai Chung, HK
- Phone: (852) 2529 6138
- Email: enquiry@penasia.edu.hk
- License: No. 593958
