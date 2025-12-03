# PythonAnywhere Deployment - Step by Step Guide

## 🚀 Quick Auto-Deploy (Recommended)

After pushing to GitHub, simply run:
```bash
./deploy_to_pythonanywhere.sh
```

**First time?** Edit the script with your credentials:
```bash
PYTHONANYWHERE_USERNAME="your_username"
PYTHONANYWHERE_DOMAIN="your_username.pythonanywhere.com"
PYTHONANYWHERE_API_TOKEN="get_from_pythonanywhere.com/account"
```

## 🎯 What You're Doing
Deploying your PenAsia LMS to PythonAnywhere free hosting

## ✅ Pre-Flight Checklist

Before starting, make sure:
- [ ] Flask server is running locally (test at http://127.0.0.1:5000)
- [ ] All features tested and working
- [ ] You have a GitHub account (recommended) or files ready to upload
- [ ] You know your admin credentials: admin@penasia.edu.hk / admin123

---

## 📝 Step-by-Step Instructions

### Step 1: Create PythonAnywhere Account (5 minutes)

1. Go to: https://www.pythonanywhere.com/
2. Click **"Pricing & signup"**
3. Select **"Create a Beginner account"** (FREE)
4. Fill in:
   - Username: (choose yours, e.g., penasia)
   - Email: your email
   - Password: create strong password
5. Click **"Register"**
6. Check your email and confirm

✅ **Done!** You now have a free account

---

### Step 2: Upload Your Project Files

**Option A: Using Git (Recommended - Faster)**

1. Click **"Consoles"** tab → **"Bash"**
2. In the console, run:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

**Option B: Manual Upload (If no GitHub)**

1. Click **"Files"** tab
2. Navigate to: `/home/yourusername/`
3. Click **"New directory"** → Name it: `penasia_lms`
4. Upload files one by one (or zip file)
   - Upload all files from your local `Flask Website` folder
   - Include: app.py, models.py, forms.py, requirements.txt, templates/, static/

✅ **Done!** Your files are uploaded

---

### Step 3: Set Up Virtual Environment (5 minutes)

1. Go to **"Consoles"** tab → Click **"Bash"**
2. Run these commands:

```bash
# Navigate to your project
cd penasia_lms

# Create virtual environment
python3.10 -m venv flask_env

# Activate it
source flask_env/bin/activate

# Install dependencies (this takes 2-3 minutes)
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.3 Flask-SQLAlchemy-3.0.5 ...
```

✅ **Done!** Dependencies installed

---

### Step 4: Initialize Database (2 minutes)

Still in the Bash console:

```bash
# Make sure you're in the right folder
cd ~/penasia_lms

# Activate virtual environment if not active
source flask_env/bin/activate

# Create instance directory
mkdir -p instance

# Initialize database
python3 << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")
EOF
```

**Expected output:**
```
✅ Database created successfully!
```

✅ **Done!** Database is ready

---

### Step 5: Create Web App (5 minutes)

1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Click **"Next"** (for the domain name)
4. Select **"Manual configuration"**
5. Select **"Python 3.10"**
6. Click **"Next"**

✅ **Done!** Web app created

---

### Step 6: Configure WSGI File (3 minutes)

1. Still on **"Web"** tab
2. Scroll down to **"Code"** section
3. Click on the WSGI configuration file link (blue text like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
4. **DELETE EVERYTHING** in the file
5. **PASTE THIS** (replace `yourusername` with YOUR actual username):

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/penasia_lms'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Flask to production mode
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application

# Optional: Set a better secret key
application.config['SECRET_KEY'] = 'change-this-to-a-random-long-string-in-production'
```

6. Click **"Save"** button (top right)

✅ **Done!** WSGI configured

---

### Step 7: Configure Virtual Environment Path (1 minute)

1. Still on **"Web"** tab
2. Scroll down to **"Virtualenv"** section
3. Click **"Enter path to a virtualenv, if desired"**
4. Enter: `/home/yourusername/penasia_lms/flask_env`
   (Replace `yourusername` with your actual username)
5. Press Enter or click the checkmark

✅ **Done!** Virtual environment linked

---

### Step 8: Configure Static Files (2 minutes)

1. Still on **"Web"** tab
2. Scroll down to **"Static files"** section
3. Click **"Enter URL"** and enter: `/static/`
4. Click **"Enter path"** and enter: `/home/yourusername/penasia_lms/static`
   (Replace `yourusername` with your actual username)
5. Click the checkmark ✓

✅ **Done!** Static files configured

---

### Step 9: Reload and Test (1 minute)

1. Scroll to the top of the **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait for "reload complete" message (appears near button)
4. Click on your domain link (near top): `https://yourusername.pythonanywhere.com`

**🎉 Your site should now be live!**

✅ **Done!** Site is deployed

---

## 🧪 Testing Your Deployed Site

Visit your site and test:

1. **Home Page**
   - [ ] Page loads correctly
   - [ ] Images load
   - [ ] Navigation works

2. **Login**
   - [ ] Go to: `https://yourusername.pythonanywhere.com/login`
   - [ ] Login with: admin@penasia.edu.hk / admin123
   - [ ] Should redirect to admin dashboard

3. **Admin Dashboard**
   - [ ] Stats cards display correctly
   - [ ] Help button works
   - [ ] Navigation links work

4. **Contact Form**
   - [ ] Go to: `https://yourusername.pythonanywhere.com/contact`
   - [ ] Fill and submit form
   - [ ] Should see success message

5. **Application Form**
   - [ ] Go to: `https://yourusername.pythonanywhere.com/apply`
   - [ ] Test form submission

---

## 🔧 Troubleshooting

### Problem: "Something went wrong" error page

**Solution:**
1. Go to **"Web"** tab
2. Scroll to **"Log files"** section
3. Click on **"Error log"**
4. Look for the error message (usually at the bottom)
5. Common fixes:
   - Check WSGI file has correct username
   - Check virtual environment path is correct
   - Make sure all dependencies installed

### Problem: Static files (CSS/images) not loading

**Solution:**
1. Go to **"Web"** tab
2. Check **"Static files"** section
3. Verify URL is: `/static/`
4. Verify path is: `/home/yourusername/penasia_lms/static`
5. Click **"Reload"** button

### Problem: Database errors

**Solution:**
1. Go to **"Consoles"** → **"Bash"**
2. Run:
```bash
cd ~/penasia_lms
source flask_env/bin/activate
python3 << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("Database recreated!")
EOF
```
3. Reload web app

### Problem: Import errors (module not found)

**Solution:**
1. Go to **"Consoles"** → **"Bash"**
2. Run:
```bash
cd ~/penasia_lms
source flask_env/bin/activate
pip install -r requirements.txt
```
3. Reload web app

---

## 🔄 How to Update Your Site Later

When you make changes locally:

**If using Git:**
```bash
# On PythonAnywhere Bash console
cd ~/penasia_lms
git pull origin main
source flask_env/bin/activate
pip install -r requirements.txt  # if requirements changed
```

**If uploading manually:**
1. Upload changed files via "Files" tab
2. Replace the old files

**Then always:**
1. Go to **"Web"** tab
2. Click **"Reload"** button

---

## 📊 What You Get with Free Tier

✅ **Included:**
- One web app
- 512 MB disk space
- Your URL: `yourusername.pythonanywhere.com`
- SQLite database
- HTTPS included
- 100,000 seconds CPU time per day

❌ **Not Included:**
- Custom domain (need $5/month "Hacker" plan)
- Multiple web apps
- Automatic SSL for custom domains
- SSH access

---

## 💰 Upgrading Later

If you need more features:

**Hacker Plan ($5/month):**
- Custom domain (your own .com)
- 1 GB disk space
- MySQL database option
- More CPU time

**To upgrade:**
1. Click your username (top right)
2. Click **"Account"**
3. Click **"Upgrade"** button
4. Choose **"Hacker"** plan

---

## ✅ Final Checklist

After deployment:

- [ ] Site loads at `https://yourusername.pythonanywhere.com`
- [ ] Home page displays correctly
- [ ] Static files (CSS, images) loading
- [ ] Login works
- [ ] Admin dashboard accessible
- [ ] Forms submit correctly
- [ ] Database saving data
- [ ] Help system works
- [ ] No errors in error log

---

## 🎉 Success!

Your PenAsia LMS is now live on the internet!

**Your URLs:**
- **Live Site:** `https://yourusername.pythonanywhere.com`
- **Admin Login:** `https://yourusername.pythonanywhere.com/login`
- **Admin Credentials:** admin@penasia.edu.hk / admin123

**Share with:**
- Clients for demo
- Team members for testing
- Students for feedback

---

## 📚 Useful Links

- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Your Dashboard:** https://www.pythonanywhere.com/user/yourusername/
- **Error Logs:** Web tab → Log files section
- **Community Forum:** https://www.pythonanywhere.com/forums/

---

## 🆘 Need Help?

If you get stuck:

1. Check the error log (Web tab → Error log)
2. Read PythonAnywhere help docs
3. Ask in their forums
4. Or ask me! I'm here to help 😊

**Common first-time issues:**
- Forgetting to replace `yourusername` with actual username
- Not activating virtual environment
- Wrong paths in configuration
- Missing dependencies installation

**Remember:** Every deployment has small hiccups. Don't worry, we'll fix them! 🚀
