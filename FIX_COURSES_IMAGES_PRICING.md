# Fix Courses Page - Images & Pricing
**Date:** January 12, 2026  
**Issue:** All course images showing same image, prices need verification

---

## Issues Identified

### 1. Image Display Problem
**Symptom:** All courses showing the same culinary kitchen image instead of unique images per course

**Root Cause:** 
- Template uses image paths from `static/images/four courses images/` folder
- These images may not exist on PythonAnywhere server
- Browser may be caching old images

### 2. Pricing Status
**Local Database:** ✓ Updated (HK$125,000 for Hotel, HK$118,000 for BTEC)  
**Live Site:** Appears correct based on screenshot  
**PythonAnywhere Database:** Needs verification

---

## Solution - Deployment Steps

### Step 1: Verify Local Files
```bash
cd "/home/imjd/Hong Kong University/Flask Website"

# Check images exist locally
ls -la "static/images/four courses images/"

# Should show:
# - Btec.jpg (1.4MB)
# - hotel_culinary.jpg (1.4MB)
# - wester_cuisine.png (1.5MB)
# - western-bakery.png (158KB)
```

### Step 2: Commit and Push Changes
```bash
cd "/home/imjd/Hong Kong University/Flask Website"

# Add all files including images
git add .
git commit -m "Fix course images and pricing - Jan 2026"
git push origin main
```

### Step 3: Deploy to PythonAnywhere
```bash
# SSH to PythonAnywhere
ssh USERNAME@ssh.pythonanywhere.com

# Navigate to project
cd ~/penasia-education-platform

# Pull latest changes
git pull origin main

# Verify images were pulled
ls -la static/images/four\ courses\ images/

# Update database pricing
python3 update_pricing_jan2026.py

# Reload web app
touch /var/www/USERNAME_pythonanywhere_com_wsgi.py
```

### Step 4: Clear Browser Cache
After deployment:
1. Hard refresh: Ctrl+Shift+R (Linux/Windows) or Cmd+Shift+R (Mac)
2. Or clear browser cache completely
3. Open in incognito/private window to test

---

## Template Image Logic

The [courses.html](Flask%20Website/templates/courses.html) template uses course codes to map images:

```jinja2
{% if course.course_code == 'PSCE-DHM-5266' %}
    <!-- Hotel Culinary Management -->
    <img src="{{ url_for('static', filename='images/four courses images/hotel_culinary.jpg') }}">
    
{% elif course.course_code == 'PSCE-BTB-5001' %}
    <!-- BTEC Business Management -->
    <img src="{{ url_for('static', filename='images/four courses images/Btec.jpg') }}">
    
{% elif course.course_code == 'CEF-43C130000' %}
    <!-- Western Bakery -->
    <img src="{{ url_for('static', filename='images/four courses images/western-bakery.png') }}">
    
{% elif course.course_code == 'CEF-43C15919A' %}
    <!-- Western Cuisine -->
    <img src="{{ url_for('static', filename='images/four courses images/wester_cuisine.png') }}">
    
{% else %}
    <!-- Fallback image -->
    <img src="{{ url_for('static', filename='images/courses/courses_01.png') }}">
{% endif %}
```

---

## Verification Checklist

After deployment, verify:

- [ ] Hotel Culinary (PSCE-DHM-5266) shows unique culinary image
- [ ] BTEC Business (PSCE-BTB-5001) shows BTEC classroom image
- [ ] Western Bakery (CEF-43C130000) shows bakery/pastry image
- [ ] Western Cuisine (CEF-43C15919A) shows western cuisine image
- [ ] Hotel Culinary fee shows HK$125,000
- [ ] BTEC Business fee shows HK$118,000
- [ ] Western Bakery fee shows HK$12,620
- [ ] Western Cuisine fee shows HK$12,620

---

## Troubleshooting

### If Images Still Don't Show:

1. **Check image paths on server:**
   ```bash
   cd ~/penasia-education-platform
   find static/images -name "*.jpg" -o -name "*.png" | grep -i "four courses"
   ```

2. **Check file permissions:**
   ```bash
   ls -la static/images/four\ courses\ images/
   # Should be readable (644 or similar)
   ```

3. **Test image URLs directly:**
   - https://yoursite.pythonanywhere.com/static/images/four%20courses%20images/hotel_culinary.jpg
   - https://yoursite.pythonanywhere.com/static/images/four%20courses%20images/Btec.jpg
   - https://yoursite.pythonanywhere.com/static/images/four%20courses%20images/western-bakery.png
   - https://yoursite.pythonanywhere.com/static/images/four%20courses%20images/wester_cuisine.png

4. **Check browser console for 404 errors:**
   - Right-click → Inspect → Console tab
   - Look for failed image load errors

### If Pricing is Wrong:

1. **Verify database on PythonAnywhere:**
   ```bash
   cd ~/penasia-education-platform
   sqlite3 penasia.db "SELECT course_code, fee_hkd FROM course WHERE is_active = 1;"
   ```

2. **Run pricing update if needed:**
   ```bash
   python3 update_pricing_jan2026.py
   ```

---

## Current Status

**Local Environment:** ✓ Fixed  
- Database updated with correct pricing
- Images exist in `static/images/four courses images/`
- Template correctly maps course codes to images

**PythonAnywhere:** Needs deployment  
- Push code with git
- Pull on server
- Update database
- Reload app

---

## Quick Deploy Command

```bash
# Run from local machine
cd "/home/imjd/Hong Kong University/Flask Website"
git add .
git commit -m "Fix course images and pricing - Jan 2026"
git push origin main

echo "Now SSH to PythonAnywhere and run:"
echo "cd ~/penasia-education-platform && git pull && python3 update_pricing_jan2026.py"
```
