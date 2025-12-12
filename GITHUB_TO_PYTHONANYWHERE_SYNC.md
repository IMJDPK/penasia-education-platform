# 🔄 Syncing GitHub Updates to PythonAnywhere - Complete Guide
**Date:** December 11, 2025  
**Problem:** Updates pushed to GitHub aren't showing on PythonAnywhere  
**Solution:** Step-by-step instructions to properly sync and deploy

---

## ⚡ Quick Fix (If Updates Aren't Showing)

If you've already pulled code but changes still aren't visible, follow these steps in order:

### Step 1: Clear Python Cache (IMPORTANT!)

```bash
cd /home/imjdpk/mysite
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
```

### Step 2: Force Reload the Web App

**Method A: Via Web Dashboard (Easiest)**
1. Log into https://www.pythonanywhere.com
2. Click **Web** menu
3. Find your app: `imjdpk.pythonanywhere.com`
4. Scroll to top
5. Click the **green RELOAD** button
6. **Wait 10-15 seconds for reload to complete**

**Method B: Via Bash Console**
```bash
touch /home/imjdpk/mysite/flask_app.wsgi
```

### Step 3: Hard Refresh Browser

Clear your browser cache to see new content:
- **Windows/Linux:** `Ctrl + Shift + R`
- **Mac:** `Cmd + Shift + R`
- Or manually clear browser cache

### Step 4: Verify Changes

Visit https://imjdpk.pythonanywhere.com and check if updates appear

---

## 🔧 Complete Sync Process (Step-by-Step)

If the quick fix didn't work, follow this complete workflow:

### Step 1: Verify Changes Exist on GitHub

**On your local machine:**
```bash
cd "/home/imjd/Hong Kong University/Flask Website"
git status
```

**Should show:**
```
On branch main
Your branch is ahead of 'origin/main' by X commits.
nothing to commit, working tree clean
```

**If you have uncommitted changes:**
```bash
git add .
git commit -m "Your changes description"
git push origin main
```

**Verify push succeeded:**
```bash
git log --oneline -3
```

### Step 2: SSH into PythonAnywhere

```bash
ssh imjdpk@ssh.pythonanywhere.com
```

**Or use Bash Console in PythonAnywhere:**
1. Go to https://www.pythonanywhere.com
2. Click **Consoles**
3. Click **Bash**

### Step 3: Navigate to Project

```bash
cd /home/imjdpk/mysite
```

**Verify you're in correct directory:**
```bash
pwd
# Should output: /home/imjdpk/mysite

ls -la
# Should show: app.py, models.py, requirements.txt, etc.
```

### Step 4: Check Current Git Status

```bash
git status
```

**Should show:**
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

**If not up to date, show what's different:**
```bash
git diff origin/main
git log --oneline origin/main -5
```

### Step 5: Pull Latest Code from GitHub

```bash
git pull origin main
```

**Expected output (if updates exist):**
```
Updating abc1234..def5678
Fast-forward
 FINAL_AUDIT_REPORT_2025-12-11.md | 1059 ++++++++++++
 PYTHONANYWHERE_COMPLETE_GUIDE.md  | 500 ++++++
 2 files changed, 1559 insertions(+)
```

**If no updates:**
```
Already up to date.
```

### Step 6: Activate Virtual Environment

```bash
source venv/bin/activate
```

**Verify activation (prompt changes):**
```
(venv) imjdpk@...mysite$
```

### Step 7: Install/Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

**This ensures all required packages are installed**

### Step 8: Clear Python Cache

```bash
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
```

### Step 9: Check for Database Migrations

```bash
python << 'EOF'
from app import app, db
with app.app_context():
    print("✅ Database connection successful")
EOF
```

**If there are new migrations:**
```bash
flask db upgrade
```

### Step 10: Reload the Web App

**Important: Do this AFTER pulling code**

**Method A: Touch WSGI file (Fastest)**
```bash
touch flask_app.wsgi
```

**Method B: Via Web Dashboard**
1. Go to https://www.pythonanywhere.com
2. **Web** menu
3. Click **Reload** button
4. Wait 10-15 seconds

### Step 11: Verify Changes

```bash
# Check git is up to date
git log --oneline -3

# Check app imports correctly
python << 'EOF'
from app import app
print("✅ App imports successfully")
EOF
```

### Step 12: Test Website

1. Visit https://imjdpk.pythonanywhere.com
2. **Hard refresh:** `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
3. Check that changes are visible

---

## 🚨 Why Updates Aren't Showing? (Troubleshooting)

### Reason 1: Code Not Reloaded

**Symptoms:** You pulled the code but changes don't appear

**Solution:**
```bash
cd /home/imjdpk/mysite

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reload app
touch flask_app.wsgi

# Wait 10-15 seconds and refresh browser (Ctrl+Shift+R)
```

### Reason 2: Browser Cache

**Symptoms:** Old version of site keeps showing

**Solution:**
- **Windows/Linux:** `Ctrl + Shift + R`
- **Mac:** `Cmd + Shift + R`
- Or clear entire browser cache manually
- Or use incognito/private window

### Reason 3: Code Not Pushed to GitHub

**Symptoms:** You made changes locally but forgot to push

**Solution (on your local machine):**
```bash
cd "/home/imjd/Hong Kong University/Flask Website"

# Check if changes exist
git status

# If yes, add and commit
git add .
git commit -m "Your changes"

# Push to GitHub
git push origin main

# Then sync on PythonAnywhere (follow steps above)
```

### Reason 4: Pull Failed on PythonAnywhere

**Symptoms:** `git pull` shows error

**Solution:**
```bash
# Check git status
git status

# Show what's different
git diff

# If changes conflict, force reset to GitHub version
git fetch origin
git reset --hard origin/main
```

### Reason 5: Virtual Environment Not Activated

**Symptoms:** Errors about missing packages after pulling

**Solution:**
```bash
cd /home/imjdpk/mysite
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Check packages
pip list | grep Flask
```

### Reason 6: Database Issues

**Symptoms:** 500 errors or database connection errors after update

**Solution:**
```bash
cd /home/imjdpk/mysite
source venv/bin/activate

# Check database
python << 'EOF'
from app import app, db
with app.app_context():
    try:
        result = db.session.execute("SELECT 1")
        print("✅ Database is healthy")
    except Exception as e:
        print(f"❌ Database error: {e}")
EOF

# Run migrations if needed
flask db upgrade
```

### Reason 7: Static Files Not Updated

**Symptoms:** CSS, JavaScript, or images aren't updating

**Solution:**
```bash
# Copy static files
cp -r /home/imjdpk/mysite/static/* /home/imjdpk/mysite/static/

# Clear static cache in PythonAnywhere
# 1. Go to Web menu
# 2. Scroll to Static files
# 3. Click red X to clear cache

# Hard refresh browser: Ctrl+Shift+R
```

---

## 📋 Complete Sync Checklist

Use this checklist every time you want to sync updates:

```
☐ Step 1: Push changes on local machine
   ├─ git add .
   ├─ git commit -m "message"
   └─ git push origin main

☐ Step 2: SSH into PythonAnywhere
   └─ ssh imjdpk@ssh.pythonanywhere.com

☐ Step 3: Navigate to project
   └─ cd /home/imjdpk/mysite

☐ Step 4: Pull latest code
   └─ git pull origin main

☐ Step 5: Activate venv
   └─ source venv/bin/activate

☐ Step 6: Update dependencies
   └─ pip install -r requirements.txt --upgrade

☐ Step 7: Clear cache
   └─ find . -type d -name __pycache__ -exec rm -rf {} +

☐ Step 8: Database migrations (if needed)
   └─ flask db upgrade

☐ Step 9: Reload web app
   ├─ Option A: touch flask_app.wsgi
   └─ Option B: Via Web dashboard reload button

☐ Step 10: Wait 10-15 seconds for reload

☐ Step 11: Hard refresh browser
   └─ Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

☐ Step 12: Verify changes are visible
   └─ Visit https://imjdpk.pythonanywhere.com
```

---

## 🔗 One-Liner Commands

### Fast Sync (Copy-Paste Friendly)

**Run this ONE command in PythonAnywhere Bash:**

```bash
cd /home/imjdpk/mysite && source venv/bin/activate && git pull origin main && pip install -r requirements.txt --upgrade && find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && touch flask_app.wsgi && echo "✅ Sync complete! Wait 10-15 seconds and refresh browser."
```

**What it does:**
1. Navigate to project
2. Activate virtual environment
3. Pull latest code from GitHub
4. Update dependencies
5. Clear Python cache
6. Reload web app
7. Show completion message

### Then Reload Web App

**Via Web Dashboard (Recommended):**
1. Go to https://www.pythonanywhere.com
2. Click **Web** menu
3. Click green **RELOAD** button
4. Wait 10-15 seconds
5. Hard refresh browser: `Ctrl+Shift+R`

---

## 🎯 If Updates STILL Aren't Showing

### Nuclear Option (Full Reset)

**⚠️ WARNING: This removes any local uncommitted changes!**

```bash
cd /home/imjdpk/mysite
source venv/bin/activate

# 1. Force reset to GitHub version
git fetch origin
git reset --hard origin/main

# 2. Clean everything
git clean -fd

# 3. Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# 4. Reinstall dependencies
pip install -r requirements.txt --upgrade

# 5. Reload
touch flask_app.wsgi

# 6. Verify
python << 'EOF'
from app import app
print("✅ App imported successfully")
EOF

echo "✅ Full reset complete! Reload web app in dashboard now."
```

### Then Reload Via Web Dashboard:
1. https://www.pythonanywhere.com → **Web** menu
2. Click **RELOAD** button
3. Wait 10-15 seconds
4. Hard refresh: `Ctrl+Shift+R`

---

## 📊 Verification Commands

### Check Git Status

```bash
cd /home/imjdpk/mysite
git status
git log --oneline -5
```

### Check if App Imports

```bash
python << 'EOF'
from app import app, db
print("✅ App imports successfully")
print("✅ Database initialized")
EOF
```

### Check Database

```bash
python << 'EOF'
from app import app, db, User
with app.app_context():
    users = User.query.all()
    print(f"✅ Total users: {len(users)}")
EOF
```

### Check Packages Installed

```bash
pip list | grep Flask
pip list | grep SQLAlchemy
```

### View Error Log

```bash
tail -50 /var/log/imjdpk.pythonanywhere.com.error.log
```

---

## 🎓 Best Practices for Future Updates

### Before Pushing to GitHub

1. **Test locally first:**
   ```bash
   cd "/home/imjd/Hong Kong University/Flask Website"
   source flask_env/bin/activate
   python app.py
   # Test at http://localhost:5000
   ```

2. **Commit with meaningful message:**
   ```bash
   git add .
   git commit -m "Fixed: login form validation" # Clear description
   ```

3. **Push to GitHub:**
   ```bash
   git push origin main
   ```

### After Pushing to GitHub

1. **Let PythonAnywhere know to reload:**
   - Pull code: `git pull origin main`
   - Reload app: `touch flask_app.wsgi` or Web dashboard
   - Hard refresh browser: `Ctrl+Shift+R`

### For Large Changes

```bash
# Create a backup first
cd /home/imjdpk
tar -czf backups/backup_before_sync_$(date +%Y%m%d_%H%M%S).tar.gz mysite/

# Then proceed with sync
cd mysite
git pull origin main
# ... rest of sync steps
```

---

## 🆘 Still Not Working?

### Get Help Debugging

1. **Check error log:**
   ```bash
   tail -100 /var/log/imjdpk.pythonanywhere.com.error.log
   ```

2. **Test app directly:**
   ```bash
   cd /home/imjdpk/mysite
   source venv/bin/activate
   python -c "from app import app; print('App works!')"
   ```

3. **Check what changed:**
   ```bash
   git show HEAD
   git diff origin/main
   ```

4. **View web app logs in dashboard:**
   - Go to https://www.pythonanywhere.com
   - **Web** menu
   - Click **Error log** or **Access log**

---

## 📝 Quick Reference: Common Scenarios

### Scenario 1: Updated HTML Template Not Showing

```bash
cd /home/imjdpk/mysite
git pull origin main              # Pull changes
touch flask_app.wsgi              # Reload app
# Hard refresh: Ctrl+Shift+R
```

### Scenario 2: Python Code Changes Not Working

```bash
cd /home/imjdpk/mysite
source venv/bin/activate
git pull origin main              # Pull changes
pip install -r requirements.txt   # Update deps
find . -type d -name __pycache__ -exec rm -rf {} +  # Clear cache
touch flask_app.wsgi              # Reload app
```

### Scenario 3: Database Changes

```bash
cd /home/imjdpk/mysite
source venv/bin/activate
git pull origin main              # Pull changes
flask db upgrade                  # Run migrations
touch flask_app.wsgi              # Reload app
```

### Scenario 4: CSS/JavaScript Not Updating

```bash
cd /home/imjdpk/mysite
git pull origin main
# In Web dashboard: Static files → click X to clear cache
# Hard refresh browser: Ctrl+Shift+R
```

---

## ✅ Success Indicators

After syncing, you should see:

```
☑ "Already up to date" or "Fast-forward" from git pull
☑ Successfully installed packages from pip
☑ App imports without errors
☑ Website loads at https://imjdpk.pythonanywhere.com
☑ Changes visible after hard refresh
☑ No 502 Bad Gateway errors
☑ Error log shows no new errors
```

---

## 📞 Still Need Help?

1. **Check error log:** `/var/log/imjdpk.pythonanywhere.com.error.log`
2. **View web app status:** PythonAnywhere Web menu
3. **Review this guide's Troubleshooting section**
4. **Visit:** https://help.pythonanywhere.com
5. **Check:** Project documentation in repository

---

## 🎉 You're All Set!

With these steps, you can confidently sync updates from GitHub to PythonAnywhere anytime!

**Remember:** 
- Always pull → update → clear cache → reload → hard refresh
- Check error logs if something breaks
- Test locally before pushing to GitHub

**Happy deploying! 🚀**
