# 🚨 URGENT FIX SUMMARY - January 7, 2026

## Problem Overview

Your live site at **https://www.penasia.edu.hk/courses** has:
1. ❌ **Wrong images** - All courses showing same kitchen image
2. ❌ **Outdated prices** - Database not synced with latest pricing

## Root Cause

✅ **Local files are CORRECT** - The issue is on PythonAnywhere server:
- Latest `courses.html` template not deployed
- Database not updated with `update_courses.py` script
- Possible browser cache showing old version

## ✅ Solution (3 Simple Steps on PythonAnywhere)

### Step 1: Pull Latest Code
```bash
cd ~/penasia-education-platform
git pull origin main
```

### Step 2: Run Deployment Script
```bash
bash deploy_fix.sh
```
This will:
- Check image files exist
- Update database prices
- Verify everything is correct

### Step 3: Reload Web App
1. Go to PythonAnywhere → **Web** tab
2. Click green **"Reload"** button
3. Clear browser cache (Ctrl+Shift+R)
4. Visit https://www.penasia.edu.hk/courses

---

## Manual Alternative (If Script Doesn't Work)

### Option A: Manual Steps

```bash
cd ~/penasia-education-platform
git pull
python3 update_courses.py
touch /var/www/imjdpk_pythonanywhere_com_wsgi.py
```

Then reload from Web tab.

### Option B: Direct Database Update

```bash
mysql -u username -p database_name
```

```sql
UPDATE course SET fee_hkd = 125000, is_active = 1 WHERE course_code = 'PSCE-DHM-5266';
UPDATE course SET fee_hkd = 118000, is_active = 1 WHERE course_code = 'PSCE-BTB-5001';
UPDATE course SET fee_hkd = 12620, is_active = 1 WHERE course_code = 'CEF-43C130000';
UPDATE course SET fee_hkd = 13200, is_active = 1 WHERE course_code = 'CEF-43C15919A';
exit;
```

---

## ✅ Expected Final Result

After deployment, your courses page should show:

| Course | Image | Price | Status |
|--------|-------|-------|--------|
| **Hotel Culinary Management** | Hotel/classroom image | HK$125,000 | ✅ |
| **BTEC Business Management** | Business classroom image | HK$118,000 | ✅ |
| **Western Bakery & Pastry** | Bakery/pastry image | HK$12,620 | ✅ |
| **Western Cuisine Certificate** | Kitchen/cooking image | HK$13,200 | ✅ |

**All four courses should have DIFFERENT, specific images!**

---

## Files Already Prepared (In Git)

✅ All files are ready in your local repository:

1. **courses.html** - Updated with correct image paths
2. **update_courses.py** - Database update script  
3. **deploy_fix.sh** - Automated deployment script
4. **app.py** - Correct course initialization
5. **Images folder** - `static/images/four courses images/` with all 4 images

---

## Verification Checklist

After deployment, check:

- [ ] Hotel Culinary shows: **HK$125,000** (NOT 141,100)
- [ ] BTEC shows: **HK$118,000** 
- [ ] Western Bakery shows: **HK$12,620**
- [ ] Western Cuisine shows: **HK$13,200**
- [ ] Hotel Culinary has **hotel/classroom** image
- [ ] BTEC has **business classroom** image  
- [ ] Western Bakery has **bakery/pastry** image
- [ ] Western Cuisine has **kitchen/cooking** image
- [ ] All 4 images are **different** (not all the same)

---

## Quick Reference: Correct Pricing (Official)

As per **COURSE_PRICING_UPDATE_2026-01-06.md**:

```
Hotel Culinary Management: HK$125,000 (NOT 141,100)
BTEC Business Management:  HK$118,000
Western Bakery & Pastry:   HK$ 12,620
Western Cuisine:           HK$ 13,200
```

**Note:** README.md shows HK$141,100 but that's OUTDATED. The official pricing update from January 6, 2026 confirms HK$125,000.

---

## Troubleshooting

### Images Still Not Showing?

**Check 1:** Verify image folder exists on server
```bash
ls -la ~/penasia-education-platform/static/images/four\ courses\ images/
```

**Check 2:** If folder missing, upload via PythonAnywhere Files tab:
- Navigate to: `static/images/`
- Create folder: `four courses images` (with space!)
- Upload all 4 image files from local

**Check 3:** Clear CDN/browser cache
- Hard refresh: Ctrl + Shift + R (Windows/Linux)
- Or: Cmd + Shift + R (Mac)

### Prices Still Wrong?

**Check 1:** Verify database was updated
```bash
python3 -c "from app import app, Course; app.app_context().push(); c = Course.query.get(169); print(f'Price: {c.fee_hkd}')"
```

**Check 2:** Check you're in correct directory
```bash
pwd
# Should show: /home/username/penasia-education-platform
```

**Check 3:** Run update script again
```bash
python3 update_courses.py
```

---

## Support Files Created

1. **PYTHONANYWHERE_DEPLOYMENT_FIX.md** - Detailed step-by-step guide
2. **deploy_fix.sh** - Automated deployment script
3. **THIS FILE** - Quick reference summary

---

## Contact Information

**Live Site:** https://www.penasia.edu.hk/courses  
**Issue:** Pricing not updating, images showing incorrectly  
**Root Cause:** Server not synced with Git repository  
**Solution:** Pull latest code + run database update + reload app

**Last Updated:** January 7, 2026, 6:30 PM  
**Status:** Ready to deploy

---

## TL;DR (Too Long; Didn't Read)

On PythonAnywhere, run:
```bash
cd ~/penasia-education-platform
git pull
bash deploy_fix.sh
```

Then:
1. Reload web app from Web tab
2. Clear browser cache
3. Check https://www.penasia.edu.hk/courses

Done! ✅
