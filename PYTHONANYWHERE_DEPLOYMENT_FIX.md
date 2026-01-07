# PythonAnywhere Deployment Fix - January 7, 2026

## Issues Identified

Based on live site analysis at https://www.penasia.edu.hk/courses:

### ❌ Problems:
1. **Prices not updating** - Database hasn't been synced with latest pricing
2. **Images showing incorrectly** - All courses showing same kitchen/chef image instead of specific course images
3. **Template not deployed** - Latest courses.html with proper image mapping not on server

### ✅ Expected Behavior:
1. **Prices**: HK$125,000, HK$118,000, HK$12,620, HK$13,200
2. **Images**: Each course should have its specific image from "four courses images" folder

---

## Step-by-Step Fix for PythonAnywhere

### Step 1: Pull Latest Code from Git

```bash
cd ~/penasia-education-platform
git pull origin main
```

**Expected output:** Should show files updated including:
- `templates/courses.html`
- `update_courses.py`
- `app.py`

### Step 2: Verify Image Files Exist

```bash
ls -la static/images/four\ courses\ images/
```

**Expected files:**
- `Btec.jpg`
- `hotel_culinary.jpg`
- `western-bakery.png`
- `wester_cuisine.png`

If these files are missing, you need to upload them manually via PythonAnywhere Files tab.

### Step 3: Update Database with Correct Pricing

```bash
cd ~/penasia-education-platform
python3 update_courses.py
```

**Expected output:**
```
Updating courses in database...
Updated: Hotel Culinary Management Diploma - Fee: HK$125000
Updated: BTEC Business Management HND - Fee: HK$118000
Updated: Western Bakery & Pastry - Active: True
Updated: Western Cuisine Certificate - Active: True

✅ All courses updated successfully!

📋 Current Course Status:
--------------------------------------------------------------------------------
169 | PSCE-DHM-5266   | Hotel Culinary Management Diploma        | HK$125,000 | ✓ Active
  1 | PSCE-BTB-5001   | BTEC Business Management HND             | HK$118,000 | ✓ Active
171 | CEF-43C130000   | Western Bakery & Pastry                  | HK$ 12,620 | ✓ Active
179 | CEF-43C15919A   | Western Cuisine Certificate              | HK$ 13,200 | ✓ Active
--------------------------------------------------------------------------------
```

### Step 4: Verify Template Changes

Check that the courses.html template has the correct image mappings:

```bash
grep -A 15 "for course in courses" ~/penasia-education-platform/templates/courses.html | head -20
```

**Should show:**
```html
{% for course in courses %}
<div class="col-lg-6 mb-4">
    <div class="card course-card-premium h-100">
        {% if course.id == 169 %}
        <img src="{{ url_for('static', filename='images/four courses images/hotel_culinary.jpg') }}" ...
        {% elif course.id == 1 %}
        <img src="{{ url_for('static', filename='images/four courses images/Btec.jpg') }}" ...
        {% elif course.id == 171 %}
        <img src="{{ url_for('static', filename='images/four courses images/western-bakery.png') }}" ...
        {% elif course.id == 179 %}
        <img src="{{ url_for('static', filename='images/four courses images/wester_cuisine.png') }}" ...
```

### Step 5: Reload Web App

1. Go to PythonAnywhere **Web** tab
2. Find your web app: `imjdpk.pythonanywhere.com` (or your domain)
3. Click the green **"Reload"** button
4. Wait for confirmation message

### Step 6: Clear Browser Cache & Test

**Hard refresh the page:**
- **Windows/Linux**: Ctrl + Shift + R or Ctrl + F5
- **Mac**: Cmd + Shift + R

**Visit:** https://www.penasia.edu.hk/courses

### Step 7: Verify All Issues Fixed

#### ✅ Pricing Checklist:
- [ ] Course 169 (Hotel Culinary) shows: **HK$125,000**
- [ ] Course 1 (BTEC Business) shows: **HK$118,000**
- [ ] Course 171 (Western Bakery) shows: **HK$12,620**
- [ ] Course 179 (Western Cuisine) shows: **HK$13,200**

#### ✅ Image Checklist:
- [ ] Course 169: Shows **classroom/hotel culinary** image
- [ ] Course 1: Shows **classroom/business** image (Btec.jpg)
- [ ] Course 171: Shows **bakery/pastry** image (western-bakery.png)
- [ ] Course 179: Shows **cooking/kitchen** image (wester_cuisine.png)

---

## Alternative: Manual Database Update (If update_courses.py Fails)

If the Python script doesn't work, use direct MySQL commands:

```bash
mysql -u your_username -p your_database_name
```

Then run:

```sql
-- Update pricing
UPDATE course SET fee_hkd = 125000, duration_weeks = 104, is_active = 1 
WHERE course_code = 'PSCE-DHM-5266';

UPDATE course SET fee_hkd = 118000, duration_weeks = 104, is_active = 1 
WHERE course_code = 'PSCE-BTB-5001';

UPDATE course SET fee_hkd = 12620, is_active = 1 
WHERE course_code = 'CEF-43C130000';

UPDATE course SET fee_hkd = 13200, is_active = 1 
WHERE course_code = 'CEF-43C15919A';

-- Verify changes
SELECT id, course_code, title, fee_hkd, is_active FROM course;
```

Exit MySQL:
```sql
exit;
```

---

## Troubleshooting

### Problem: Images Still Not Showing
**Solution 1:** Check file paths match exactly (case-sensitive)
```bash
cd ~/penasia-education-platform/static/images
find . -name "*ourses*" -o -name "*tec*" -o -name "*western*" -o -name "*hotel*"
```

**Solution 2:** Verify static files are being served
- Check `app.py` has: `app.static_folder = 'static'`
- Ensure folder name is exactly: `four courses images` (with space)

**Solution 3:** CDN/Cache issue
- Add version query to URLs: `hotel_culinary.jpg?v=2`
- Or rename folder temporarily to force cache invalidation

### Problem: Prices Still Wrong
**Cause:** Database not updated or wrong database being used

**Solution:** Verify you're updating the correct database
```bash
python3 -c "from app import app, db, Course; app.app_context().push(); courses = Course.query.all(); [print(f'{c.id}: {c.title} - HK\${c.fee_hkd}') for c in courses]"
```

### Problem: Template Changes Not Showing
**Cause:** Template caching or old wsgi file

**Solution 1:** Force reload
```bash
touch ~/penasia-education-platform/app.py
```

**Solution 2:** Restart web app from PythonAnywhere Web tab

---

## Quick Verification Commands

Run these on PythonAnywhere to verify everything:

```bash
# Check database has correct prices
python3 -c "from app import app, db, Course; app.app_context().push(); c = Course.query.get(169); print(f'Hotel Culinary: HK\${c.fee_hkd}')"

# Check image files exist
ls -1 static/images/four\ courses\ images/

# Check template has correct mapping
grep "course.id == 169" templates/courses.html

# Check app is using latest code
grep "fee_hkd=125000" app.py
```

---

## Expected Final Result

### On https://www.penasia.edu.hk/courses:

**Course Display:**
```
┌─────────────────────────────────────────────┐
│ [Hotel Culinary Image - classroom/kitchen]  │
│                                             │
│ Hotel Culinary Management Diploma           │
│ Course Code: PSCE-DHM-5266                 │
│ Duration: 104 weeks (2080 hours)           │
│ Fee: HK$125,000                            │ ✅
│ Language: English                           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ [BTEC Business Image - classroom]           │
│                                             │
│ BTEC Business Management HND                │
│ Course Code: PSCE-BTB-5001                 │
│ Duration: 104 weeks (1200 hours)           │
│ Fee: HK$118,000                            │ ✅
│ Language: English                           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ [Western Bakery Image - bakery/pastry]      │
│                                             │
│ Western Bakery & Pastry                     │
│ Course Code: CEF-43C130000                 │
│ Duration: 11 weeks (33 hours)              │
│ Fee: HK$12,620                             │ ✅
│ Language: Cantonese                         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ [Western Cuisine Image - kitchen/cooking]   │
│                                             │
│ Western Cuisine Certificate                 │
│ Course Code: CEF-43C15919A                 │
│ Duration: 10 weeks (33 hours)              │
│ Fee: HK$13,200                             │ ✅
│ Language: English supplemented Cantonese    │
└─────────────────────────────────────────────┘
```

---

## Files Modified (Already in Git)

- ✅ `templates/courses.html` - Updated image paths for all 4 courses
- ✅ `app.py` - Course initialization with correct fees
- ✅ `update_courses.py` - Database update script
- ✅ `static/images/four courses images/` - All 4 course-specific images

---

## Post-Deployment Checklist

After completing all steps:

- [ ] Git pull completed successfully
- [ ] Images exist in correct folder
- [ ] Database updated (verified with select query)
- [ ] Web app reloaded
- [ ] Browser cache cleared
- [ ] All 4 courses show correct prices
- [ ] All 4 courses show specific images (not all the same)
- [ ] Course comparison table shows correct prices
- [ ] Homepage pricing matches courses page

---

## Contact & Support

If issues persist after following this guide:

1. Check PythonAnywhere error logs:
   - Web tab → Log files → Error log
2. Verify MySQL database connection
3. Ensure all file permissions are correct
4. Check that domain DNS is pointing to correct app

**Last Updated:** January 7, 2026  
**Deployment Target:** www.penasia.edu.hk  
**Git Repository:** Main branch
