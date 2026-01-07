# Course Image Mapping Guide
**Date:** January 7, 2026  
**Purpose:** Document which image each course should use

---

## Current Image Assignments (UPDATED - January 7, 2026)

### courses.html - Using New "Four Courses Images" Folder

| Course ID | Course Title | Image Path | Image File |
|-----------|-------------|------------|------------|
| 169 | Hotel Culinary Management Diploma | `images/four courses images/hotel_culinary.jpg` | ✅ Hotel culinary specific |
| 1 | BTEC Business Management HND | `images/four courses images/Btec.jpg` | ✅ BTEC specific |
| 171 | Western Bakery & Pastry | `images/four courses images/western-bakery.png` | ✅ Bakery specific |
| 179 | Western Cuisine Certificate | `images/four courses images/wester_cuisine.png` | ✅ Western cuisine specific |

**Note:** Each course now has a dedicated image matching its program content.

---

## Expected vs Actual (Based on Screenshot)

### What We See on Live Site:

1. **Hotel Culinary Management** (Course 169)
   - Expected: Classroom image
   - Actually showing: Classroom image ✅
   - Fee: HK$125,000 (should be 141,000)

2. **BTEC Business Management** (Course 1)
   - Expected: Classroom image (classroom-02.jpg)
   - Actually showing: Kitchen/chef image ❌
   - Fee: HK$118,000 ✅

3. **Western Bakery & Pastry** (Course 171)
   - Expected: Bakery/pastry image (courses_03.png)
   - Actually showing: Kitchen/chef image ❌
   - Fee: HK$12,620 ✅

4. **Western Cuisine Certificate** (Course 179)
   - Expected: Kitchen image (courses_01.png)
   - Actually showing: Kitchen/chef image ❌
   - Fee: HK$13,200 ✅

---

## Issue Analysis

The live site is showing kitchen/chef images for courses 1, 171, and 179 instead of the assigned images. This suggests:

1. **Code not deployed**: The updated `courses.html` with new image paths hasn't been pulled to PythonAnywhere
2. **Cache issue**: Browser or CDN is caching old template
3. **Different template**: Site might be using a different template file

---

## Recommended Image Assignments

| Course | Best Image | Reason |
|--------|-----------|--------|
| Hotel Culinary (169) | Kitchen/chef training image | Matches culinary program |
| BTEC Business (1) | `classroom-02.jpg` | Matches business classroom setting |
| Western Bakery (171) | Bakery/pastry image | Matches bakery program |
| Western Cuisine (179) | Kitchen/professional cooking | Matches cuisine program |

---

## Available Images

Based on the file structure:

### University Images
- `images/university/classroom-01.jpg`
- `images/university/classroom-02.jpg` ✅ Currently assigned to BTEC & Hotel
- `images/university/smart-class-room.png`
- `images/university/facility-01.jpg`
- `images/university/facility-02.jpg`
- `images/university/facility-03.jpg`

### Course Images
- `images/courses/courses_01.jpg`
- `images/courses/courses_01.png` ✅ Currently assigned to Western Cuisine
- `images/courses/courses_02.jpg`
- `images/courses/courses_03.jpg`
- `images/courses/courses_03.png` ✅ Currently assigned to Western Bakery
- `images/courses/western-bakery.png`
- `images/courses/western-cuisine.png`

---

## Action Required

1. **Verify PythonAnywhere has latest code**
   ```bash
   cd ~/penasia-education-platform
   git pull origin main
   grep -A 10 "course.id == 1" templates/courses.html
   ```

2. **Check which template is being rendered**
   ```bash
   ls -la templates/courses*.html
   ```

3. **Force template reload**
   ```bash
   touch /var/www/imjdpk_pythonanywhere_com_wsgi.py
   # Clear browser cache and reload
   ```

4. **If images still wrong, update to better matches**
   - Consider using `western-bakery.png` for course 171
   - Consider using `western-cuisine.png` for course 179

---

## Next Steps

- [ ] Pull latest code to PythonAnywhere
- [ ] Verify courses.html template
- [ ] Reload web app
- [ ] Clear browser cache
- [ ] Test live site
- [ ] Update MySQL database fee for course 169 to 141000
