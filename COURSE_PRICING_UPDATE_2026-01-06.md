# Course Pricing & Status Update - January 6, 2026

## Summary of Changes

Updated course pricing to correct values and enabled admissions for all four courses.

## Pricing Updates

### Correct Pricing (Now Applied)
- **Hotel Culinary Management Diploma**: HK$125,000 (2 years / 104 weeks)
- **BTEC Business Management HND**: HK$118,000 (2 years / 104 weeks)
- **Western Bakery & Pastry**: HK$12,620 (11 weeks)
- **Western Cuisine Certificate**: HK$13,200 (10 weeks)

## Files Modified

### 1. Backend (Database Initialization)
**File**: `Flask Website/app.py`
- Updated `course171` (Western Bakery & Pastry): `is_active=True` (was False)
- Updated `course179` (Western Cuisine Certificate): `is_active=True` (was False)
- Comments changed from "ADMISSIONS CLOSED" to "Admissions open"

### 2. Frontend Templates

#### `Flask Website/templates/index.html`
- Removed "Admissions Closed" badge from Western Bakery card
- Removed "Admissions Closed" badge from Western Cuisine card
- Removed opacity styling (was 0.8) to make cards fully visible
- Removed `.program-overlay` divs containing the closed badges

#### `Flask Website/templates/apply.html`
- Removed `disabled` class from Western Bakery program option
- Removed `disabled` class from Western Cuisine program option
- Removed `data-active="false"` attributes
- Removed "Admissions Closed" badge elements

#### Note: `Flask Website/templates/apply_new.html` removed
All application form changes are consolidated in `Flask Website/templates/apply.html`.

### 3. Database Update Script
**File**: `Flask Website/update_courses.py` (NEW)
- Created script to update existing database records
- Updates pricing for all courses
- Activates courses 171 and 179
- Displays current course status for verification

## Next Steps - Database Sync

To sync the database on PythonAnywhere:

### Option 1: Run the update script (Recommended)
```bash
cd ~/penasia-education-platform
python3 update_courses.py
```

### Option 2: Reinitialize sample data
```bash
cd ~/penasia-education-platform
python3 -c "from app import app, db, init_sample_data; app.app_context().push(); init_sample_data()"
```

### Option 3: Manual SQL Update
```sql
-- Activate Western Bakery & Pastry
UPDATE course SET is_active = 1 WHERE course_code = 'CEF-43C130000';

-- Activate Western Cuisine
UPDATE course SET is_active = 1 WHERE course_code = 'CEF-43C15919A';

-- Update pricing (if needed)
UPDATE course SET fee_hkd = 125000, duration_weeks = 104 WHERE course_code = 'PSCE-DHM-5266';
UPDATE course SET fee_hkd = 118000, duration_weeks = 104 WHERE course_code = 'PSCE-BTB-5001';
```

## Verification Checklist

After deploying to PythonAnywhere:

- [ ] Home page shows all 4 courses without "Admissions Closed" badges
- [ ] Courses page displays correct pricing from database
- [ ] Apply form shows all 4 courses as selectable (no disabled state)
- [ ] Course 169 shows HK$125,000
- [ ] Course 1 shows HK$118,000
- [ ] Course 171 shows HK$12,620 and is selectable
- [ ] Course 179 shows HK$13,200 and is selectable

## Deployment to PythonAnywhere

1. **Push changes to Git**:
```bash
cd "/home/imjd/Hong Kong University/Flask Website"
git add .
git commit -m "Update course pricing and enable all admissions"
git push origin main
```

2. **On PythonAnywhere**:
```bash
cd ~/penasia-education-platform
git pull
python3 update_courses.py
```

3. **Reload the web app** in PythonAnywhere Web tab

## Notes

- Home page pricing was already correct (HK$125,000 and HK$118,000)
- Courses page pulls pricing from database, so it will auto-update after running the update script
- The courses.html template uses `{{ "{:,.0f}".format(course.fee_hkd) }}` to display fees from the database
- All changes maintain consistency between frontend and backend
