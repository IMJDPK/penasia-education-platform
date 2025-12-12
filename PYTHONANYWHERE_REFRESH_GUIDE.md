# 🚀 PythonAnywhere Deployment Refresh Guide
**For:** imjdpk.pythonanywhere.com  
**Date:** December 11, 2025  
**Purpose:** Step-by-step guide to update the live website with latest changes

---

## Quick Overview

You have two options:
1. **Full Refresh (Recommended)** - Pull latest from GitHub + reload
2. **Quick Reload** - Just reload the app (if already synced)

**Time Required:** 
- Full Refresh: 5-10 minutes
- Quick Reload: 1-2 minutes

---

## Option 1: Full Refresh (Recommended)

### Step 1: Access PythonAnywhere Console

1. Go to **https://www.pythonanywhere.com**
2. Log in with your account (IMJDPK)
3. Click **Consoles** in the top menu
4. Click **Bash** (if available) or **Start a new console**

### Step 2: Navigate to Your Project

```bash
cd /home/imjdpk/mysite
```

**Note:** Replace `mysite` with your actual directory name. If unsure, use:
```bash
ls ~
```

### Step 3: Pull Latest Code from GitHub

```bash
git pull origin main
```

**Expected Output:**
```
Updating 8075f73..8754316
Fast-forward
 FINAL_AUDIT_REPORT_2025-12-11.md | 1059 +++++++++++++++++++++
 1 file changed, 1059 insertions(+)
 create mode 100644 FINAL_AUDIT_REPORT_2025-12-11.md
```

### Step 4: Install/Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

**Expected Output:**
```
Successfully installed Flask==2.3.3
...
```

### Step 5: Run Database Migrations (if needed)

```bash
flask db upgrade
```

Or if using the app directly:
```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Step 6: Reload Web App

1. Go to **Web** menu in PythonAnywhere
2. Find your web app in the list (e.g., `imjdpk.pythonanywhere.com`)
3. Click the green **Reload** button at the top

**⏳ Wait 5-10 seconds for reload to complete**

### Step 7: Verify Deployment

1. Visit **https://imjdpk.pythonanywhere.com**
2. Check that:
   - Homepage loads correctly
   - Navigation works
   - Login page is accessible
   - Courses display properly

✅ **Deployment Complete!**

---

## Option 2: Quick Reload (If Code Already Synced)

If you've already pushed code and it's synced, just reload:

### Via Web Console:
1. Go to **https://www.pythonanywhere.com**
2. Click **Web** menu
3. Find your app (`imjdpk.pythonanywhere.com`)
4. Click green **Reload** button
5. Wait 5-10 seconds

### Via Bash Console:
```bash
touch /home/imjdpk/mysite/flask_app.wsgi
```

This touches the WSGI file to trigger a reload.

---

## Troubleshooting

### Issue 1: "Git command not found"

**Solution:** Use the file editor instead
1. Go to **Files** in PythonAnywhere
2. Navigate to your project directory
3. Manually update changed files
4. Then reload the web app

### Issue 2: "Permission denied" when pulling

**Solution:** Check repository access
```bash
# Check if SSH key is set up
cat ~/.ssh/id_rsa.pub

# Or use HTTPS instead
git remote set-url origin https://github.com/IMJDPK/penasia-education-platform.git
git pull origin main
```

### Issue 3: Database errors after update

**Solution:** Reset database
```bash
# Remove old database
rm instance/penasia.db

# Recreate
python3 << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
print("Database recreated!")
EOF
```

### Issue 4: Static files not updating

**Solution:** Clear static files cache
1. Go to **Web** menu
2. Scroll to **Static files**
3. Click the red **X** to clear cache
4. Click green **Reload** button

### Issue 5: Changes not visible after reload

**Solution:** Hard refresh browser
- **Windows/Linux:** `Ctrl + Shift + R`
- **Mac:** `Cmd + Shift + R`
- Or clear browser cache manually

---

## Full Step-by-Step Workflow

### Complete Refresh Checklist

```
☐ 1. Log into PythonAnywhere
☐ 2. Open Bash console
☐ 3. Navigate to project: cd /home/imjdpk/mysite
☐ 4. Pull latest code: git pull origin main
☐ 5. Update dependencies: pip install -r requirements.txt --upgrade
☐ 6. Run migrations: flask db upgrade
☐ 7. Go to Web menu
☐ 8. Click Reload button
☐ 9. Wait 5-10 seconds
☐ 10. Visit https://imjdpk.pythonanywhere.com
☐ 11. Hard refresh browser (Ctrl+Shift+R)
☐ 12. Test all features:
      ☐ Homepage loads
      ☐ Login works
      ☐ Courses display
      ☐ Admin panel accessible
```

---

## Common Commands Reference

### Check Current Branch
```bash
git status
```

### View Recent Commits
```bash
git log --oneline -5
```

### Check Python Version
```bash
python3 --version
```

### Check Installed Packages
```bash
pip list
```

### View Error Logs
```bash
# PythonAnywhere stores logs here
cat /var/log/imjdpk.pythonanywhere.com.error.log

# Or check recent errors
tail -50 /var/log/imjdpk.pythonanywhere.com.error.log
```

### Restart Python Anywhere App
```bash
# In PythonAnywhere Web menu, click Reload
# Or touch WSGI file to force reload
touch /home/imjdpk/mysite/flask_app.wsgi
```

---

## After Each Update: Testing Checklist

### Critical Features to Test

**Authentication:**
- [ ] Login page loads
- [ ] Can log in with credentials
- [ ] Can register new account
- [ ] Can log out

**Courses:**
- [ ] Course listing page loads
- [ ] Course details page works
- [ ] Can apply for course
- [ ] Application form validates

**Admin:**
- [ ] Admin login works
- [ ] Dashboard loads
- [ ] Can view users
- [ ] Can view applications
- [ ] Can approve/reject applications

**Payments:**
- [ ] Payment form displays
- [ ] Payment validation works
- [ ] Payment status shows correctly

**LMS Features:**
- [ ] Can access learning modules
- [ ] Can submit assignments
- [ ] Can take quizzes
- [ ] Progress tracking works

---

## Scheduled Updates

### Daily/Weekly Checks
- Review error logs
- Monitor uptime
- Check user feedback

### Monthly Maintenance
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Review and optimize database
- Backup database regularly

### Quarterly Reviews
- Security audit
- Performance optimization
- Feature enhancement

---

## Important Notes

### Before Pushing to Production

1. **Test Locally First**
   ```bash
   cd "/home/imjd/Hong Kong University/Flask Website"
   source flask_env/bin/activate
   python app.py
   # Test at http://localhost:5000
   ```

2. **Test on Staging (if available)**
   - Deploy to staging first
   - Verify all features
   - Then deploy to production

3. **Always Commit Before Pushing**
   ```bash
   git add .
   git commit -m "Descriptive message of changes"
   git push origin main
   ```

### Backup Strategy

**Weekly Backups:**
```bash
# Backup database
cp /home/imjdpk/mysite/instance/penasia.db \
   /home/imjdpk/mysite/backups/penasia_$(date +%Y%m%d).db

# Backup entire project
tar -czf /home/imjdpk/mysite_$(date +%Y%m%d).tar.gz /home/imjdpk/mysite/
```

---

## Environment Variables on PythonAnywhere

### Setting Environment Variables

1. Go to **Web** menu
2. Scroll to **Web app sections**
3. Click your app name
4. Scroll to **Environment variables**
5. Add variables like:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

6. Click **Reload** button

### Verify Variables Are Set
```bash
python3 << 'EOF'
import os
print("FLASK_ENV:", os.getenv('FLASK_ENV'))
print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("SMTP_SERVER:", os.getenv('SMTP_SERVER'))
EOF
```

---

## Quick Reference: Reload Methods

### Method 1: Web Console (Easiest)
1. PythonAnywhere Dashboard
2. Click "Web"
3. Click green "Reload" button
4. Wait 5 seconds

### Method 2: Bash Console
```bash
cd /home/imjdpk/mysite
touch flask_app.wsgi
```

### Method 3: API (if configured)
```bash
curl -X POST https://www.pythonanywhere.com/api/v0/user/imjdpk/webapps/imjdpk.pythonanywhere.com/reload/
```

---

## Support Resources

### PythonAnywhere Help
- **Help Page:** https://www.pythonanywhere.com/help/
- **Blog:** https://www.pythonanywhere.com/blog/
- **Forums:** https://www.pythonanywhere.com/forums/

### Git Help
- **Clone Repository:** `git clone https://github.com/IMJDPK/penasia-education-platform.git`
- **View Changes:** `git diff`
- **View Log:** `git log --oneline`

### Flask Help
- **Official Docs:** https://flask.palletsprojects.com/
- **Database Migrations:** `flask db --help`

---

## Contact & Support

**Project Repository:** https://github.com/IMJDPK/penasia-education-platform  
**PythonAnywhere Account:** imjdpk.pythonanywhere.com  
**Current Status:** Production Ready ✅

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-11 | 1.0 | Initial guide created |

---

## ✅ You're Ready!

With this guide, you can confidently update your PythonAnywhere deployment anytime you push changes to GitHub. The process is simple and safe!

**Happy deploying! 🚀**
