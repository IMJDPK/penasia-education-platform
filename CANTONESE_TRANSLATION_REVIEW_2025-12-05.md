# Cantonese Translation Review & Correction Required
**Date:** December 5, 2025  
**Status:** Pending Expert Review & Correction

---

## SUMMARY
This document lists ALL Cantonese text currently used in the PenAsia Education Platform website and application. The user has indicated that translations are **NOT CORRECT** and need to be reviewed and corrected by a professional Cantonese speaker/translator.

---

## LOCATIONS & CANTONESE TEXT TO REVIEW

### 1. **Organization Name**

#### Current Usage (INCORRECT)
- **盈亞持續教育中心** - "PenAsia Continuing Education Centre"
- **盈亞大學** - "University of PenAsia"

#### Files Using These:
- `/templates/base.html` - Line 23
- `/templates/index.html` - Line 118
- `/templates/about.html` - Line 71
- `/templates/terms.html` - Line 30
- `app.py` - Multiple locations
- `PenAsia_Master_Development_Document.md` - Line 19
- `WEBSITE_CHANGES_2025-12-04.md` - Lines 31, 210, 242, 844

#### What Needs Review:
- [ ] Which translation is correct for the organization?
- [ ] Should it be one consistent name across all materials?
- [ ] What's the official Hong Kong company registration name?

---

### 2. **Course 169 - Hotel Culinary Management Diploma**

#### Current Cantonese Text (INCORRECT)

**Title:**
```
酒店廚務管理文憑 (Diploma in Hotel Culinary Management)
```

**Description:**
```
2年全日制酒店廚務管理文憑課程，提供專業廚藝訓練和酒店管理知識
(2-year full-time diploma program providing professional culinary training and hotel management knowledge)
```

**Course Modules/Content:**
```
食物及職業安全與健康 (Food and Occupational Safety & Health)
廚務營運 (Kitchen Operations)
焗焙及甜品 (Baking and Desserts)
飲食服務與營運 (Food & Beverage Service and Operations)
溝通及報告寫作技巧 (Communication and Report Writing Skills)
款待業概論 (Introduction to Hospitality Industry)
美食 (Cuisine)
```

#### Files Using These:
- `app.py` - Lines 1509-1523
- `templates/course_detail.html` - Lines 27, 70, 74, 78, 82, 86, 90

#### What Needs Review:
- [ ] Accurate translation of diploma title
- [ ] Correct terminology for each module name
- [ ] Proper Cantonese phrasing for technical terms
- [ ] Consistency with actual course curriculum documentation

---

### 3. **Course 1 - Pearson BTEC Level 5 Business Management**

#### Current Cantonese Text (INCORRECT)

**Title:**
```
Pearson BTEC Level 5 高級國家文憑商業管理 (Higher National Diploma in Business)
```

**Description:**
```
24個月商業管理高級國家文憑，提供升讀英國學士學位課程機會
(24-month Higher National Diploma in Business with progression to UK degree programs)
```

#### Files Using These:
- `app.py` - Lines 1530-1531
- `PenAsia_Master_Development_Document.md` - Line 67

#### What Needs Review:
- [ ] Verify "高級國家文憑" is correct for BTEC HND
- [ ] Check "升讀英國學士學位課程" phrasing
- [ ] Ensure consistency with Hong Kong education terminology

---

### 4. **Course 171 - Western Bakery & Pastry**

#### Current Cantonese Text (INCORRECT)

**Title:**
```
西式烘焙及糕餅製作證書 (Certificate in Western Bakery and Pastry)
```

**Description:**
```
11週西式烘焙及糕餅製作證書課程，提供實用烘焙技能訓練
(11-week certificate program providing practical Western baking and pastry skills training)
```

#### Files Using These:
- `app.py` - Lines 1550-1551
- `PenAsia_Master_Development_Document.md` - Line 97

#### What Needs Review:
- [ ] Verify terminology for "Western Bakery and Pastry"
- [ ] Check if "糕餅製作" is the correct term
- [ ] Confirm CEF-approved translation

---

### 5. **Course 179 - Western Starter & Main Course**

#### Current Cantonese Text (INCORRECT)

**Title:**
```
西式頭盤及主菜製作證書 (Certificate in Western Starter and Main Course)
```

**Description:**
```
11週西式頭盤及主菜製作證書課程，掌握專業西式烹飪技巧
(11-week certificate program focusing on Western cuisine fundamentals and professional cooking techniques)
```

#### Files Using These:
- `app.py` - Lines 1571-1572
- `PenAsia_Master_Development_Document.md` - Line 127

#### What Needs Review:
- [ ] Verify "頭盤" is correct for "Starter"
- [ ] Check "主菜" terminology
- [ ] Ensure professional culinary Cantonese terminology

---

### 6. **Base Template - Top Strip**

#### Current Cantonese Text (INCORRECT)
**File:** `templates/base.html` - Line 23

```html
<span class="top-strip-text">University of PenAsia - 盈亞大學</span>
```

#### What Needs Review:
- [ ] Should this use organization name or university name?
- [ ] What's the correct Cantonese branding?

---

## CRITICAL QUESTIONS FOR TRANSLATOR

1. **Organization Name:**
   - What is the official Cantonese name registered with the Hong Kong government?
   - Should it be "盈亞大學" (University of PenAsia) or "盈亞持續教育中心" (PenAsia Continuing Education Centre)?
   - Are there other official names in Cantonese?

2. **Course Terminology:**
   - What are the OFFICIAL Cantonese course titles as they appear in:
     - Hong Kong Qualifications Framework (HQF) documents?
     - CEF (Continuing Education Fund) registration?
     - Pearson BTEC documentation?
   - Are there standard Hong Kong education terminology that must be used?

3. **Technical Terms:**
   - What are the correct Cantonese terms for:
     - "Diploma" (文憑? 證書?)
     - "Higher National Diploma" (高級國家文憑? Other?)
     - "Certificate" (證書? 認證?)
     - "Culinary" (廚務? 烹飪? 烹飪藝術?)

4. **Module Names:**
   - For Course 169, are these module names officially recognized in Hong Kong?
   - Should they match any specific curriculum framework?

5. **Consistency:**
   - Should ALL course titles follow the same format?
   - Should English translations always accompany Cantonese?
   - Any preferred order (Cantonese first or English first)?

---

## FILES REQUIRING UPDATES

When corrections are made, the following files need to be updated:

### Python Files:
1. `/app.py` 
   - Lines 1509-1523 (Course 169)
   - Lines 1530-1531 (Course 1)
   - Lines 1550-1551 (Course 171)
   - Lines 1571-1572 (Course 179)

### Template Files:
1. `/templates/base.html`
   - Line 23 (Organization name)

2. `/templates/index.html`
   - Line 118 (Organization name)

3. `/templates/about.html`
   - Line 71 (Organization name)

4. `/templates/terms.html`
   - Line 30 (Organization name)

5. `/templates/course_detail.html`
   - Line 27 (Course 169 title)
   - Lines 70, 74, 78, 82, 86, 90 (Module names)

### Documentation Files:
1. `/PenAsia_Master_Development_Document.md`
   - Lines 19, 39-58, 67, 97, 127

2. `/WEBSITE_CHANGES_2025-12-04.md`
   - Lines 31, 210, 242, 844

3. `/COMPLETE_SYSTEM_AUDIT_2025-12-05.md`
   - May need updates for course descriptions

---

## IMPLEMENTATION STEPS

Once translations are corrected:

1. **Create a translation mapping document** showing:
   - Current (incorrect) text
   - Corrected text
   - Files affected
   - Line numbers

2. **Perform find/replace** across all affected files with verified translations

3. **QA Check:**
   - Display all pages in browser
   - Verify Cantonese renders correctly (UTF-8 encoding)
   - Test on mobile devices
   - Check in both desktop and mobile views

4. **Update documentation** with correct translations

5. **Create Cantonese translation style guide** for future updates

---

## NOTES

- **Character Encoding:** Ensure all files are saved as UTF-8 to properly display Traditional Chinese characters
- **Font Support:** Verify browser fonts support Traditional Chinese characters
- **Terminology Sources:** Official corrections should come from:
  - Hong Kong Education Bureau
  - CEF (Continuing Education Fund) approved course descriptions
  - Pearson BTEC official Hong Kong materials
  - Professional Cantonese translator specializing in education

---

**Status:** AWAITING EXPERT CANTONESE REVIEW  
**Action Required:** Engage professional translator to review and correct all translations  
**Priority:** HIGH - Before public website launch or marketing materials

---

*This document serves as a checklist for translation corrections. Do not proceed with deployment until all Cantonese text has been reviewed and approved by a professional Cantonese speaker with expertise in Hong Kong education terminology.*
