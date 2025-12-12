# 🚀 PythonAnywhere Complete Deployment Guide
**For:** PenAsia Education Platform  
**Repository:** IMJDPK/penasia-education-platform  
**Date:** December 11, 2025  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Account Setup](#account-setup)
2. [Initial Deployment](#initial-deployment)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Email Configuration](#email-configuration)
6. [Static Files & Media](#static-files--media)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Monitoring & Logs](#monitoring--logs)
9. [Updates & Maintenance](#updates--maintenance)
10. [Troubleshooting](#troubleshooting)
11. [Backup & Recovery](#backup--recovery)

---

## Account Setup

### Step 1: Create PythonAnywhere Account

1. Go to **https://www.pythonanywhere.com**
2. Click **Sign Up** (choose Free or Paid plan)
3. Enter username: `imjdpk`
4. Enter email and password
5. Verify email
6. Log in to dashboard

**Plans Comparison:**

| Feature | Free | Beginner | Pro |
|---------|------|----------|-----|
| **Price** | Free | $5/month | $20/month |
| **Concurrent Web Apps** | 1 | 1 | 2 |
| **CPU Time** | 100 secs/day | Unlimited | Unlimited |
| **Scheduled Tasks** | No | Yes | Yes |
| **SSL Certificate** | No | Yes | Yes |
| **Always On** | No | Yes | Yes |
| **RAM** | 512MB | 1GB | 2GB |

**Recommendation:** Start with **Beginner Plan** for production deployment

### Step 2: Set Up SSH Key (Optional but Recommended)

1. On local machine, generate SSH key:
```bash
ssh-keygen -t rsa -b 4096
```

2. Copy public key:
```bash
cat ~/.ssh/id_rsa.pub
```

3. In PythonAnywhere:
   - Go to **Account** → **SSH Keys**
   - Click **Add a new SSH key**
   - Paste your public key
   - Click **Save**

4. Test SSH connection:
```bash
ssh imjdpk@ssh.pythonanywhere.com
```

---

## Initial Deployment

### Step 1: Access PythonAnywhere Web Console

1. Log into **https://www.pythonanywhere.com**
2. Click **Consoles** at top
3. Click **Start a new console** → **Bash**

### Step 2: Clone Your Repository

```bash
git clone https://github.com/IMJDPK/penasia-education-platform.git mysite
cd mysite
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask==2.3.3 Flask-Login==0.6.3 ...
```

### Step 5: Initialize Database

```bash
python << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("Database initialized!")
EOF
```

### Step 6: Load Sample Data (Optional)

```bash
python create_sample_data.py
```

---

## Configuration

### Step 1: Set Up Web App

1. Go to **Web** menu
2. Click **Add a new web app**
3. Choose domain: `imjdpk.pythonanywhere.com`
4. Select **Python 3.10** (or latest available)
5. Click **Next**
6. Select **Flask**
7. Select **Python 3.10**
8. Set project path: `/home/imjdpk/mysite`
9. Click **Next**

### Step 2: Configure WSGI File

1. Go to **Web** menu
2. Click your app: `imjdpk.pythonanywhere.com`
3. Scroll to **Code** section
4. Click **WSGI configuration file**
5. Edit the file with this content:

```python
import os
import sys

path = '/home/imjdpk/mysite'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

# Activate virtual environment
activate_this = os.path.join(path, 'venv', 'bin', 'activate_this.py')
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

from app import app as application
```

6. Click **Save**

### Step 3: Configure Environment Variables

1. Go to **Web** menu
2. Scroll to **Environment variables**
3. Add these variables:

```
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-key-here-min-32-chars
DATABASE_URL=sqlite:////home/imjdpk/mysite/instance/penasia.db
```

**Generate secure SECRET_KEY:**
```bash
python << 'EOF'
import secrets
print(secrets.token_urlsafe(32))
EOF
```

4. Click **Reload** button

---

## Database Setup

### Option 1: SQLite (Recommended for Small-Medium Projects)

Already set up by default. No additional configuration needed.

**Location:** `/home/imjdpk/mysite/instance/penasia.db`

### Option 2: PostgreSQL (Recommended for Production)

#### Step 1: Create PostgreSQL Database

1. Go to **Databases** in PythonAnywhere
2. Click **Create a new database**
3. Choose **PostgreSQL**
4. Enter database name: `penasia_db`
5. Click **Create**
6. Note the connection string

#### Step 2: Update Configuration

1. Go to **Web** → **Environment variables**
2. Update DATABASE_URL:
```
DATABASE_URL=postgres://imjdpk:your-password@imjdpk.mysql.pythonanywhere-services.com/imjdpk$penasia_db
```

#### Step 3: Run Migrations

```bash
cd /home/imjdpk/mysite
source venv/bin/activate
flask db upgrade
python create_sample_data.py
```

### Create Admin User

```bash
cd /home/imjdpk/mysite
source venv/bin/activate

python << 'EOF'
from app import app, db, User
with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(email='admin@penasia.edu.hk').first()
    if not admin:
        admin = User(
            email='admin@penasia.edu.hk',
            first_name='Admin',
            last_name='User',
            role='admin',
            is_active=True,
            email_verified=True
        )
        admin.set_password('admin123')  # Change this!
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")
    else:
        print("✅ Admin user already exists")
EOF
```

**Admin Credentials:**
- Email: `admin@penasia.edu.hk`
- Password: `admin123` (Change immediately after first login!)

---

## Email Configuration

### Step 1: Enable SMTP Service

1. Go to **Web** menu
2. Click your web app
3. Scroll to **Environment variables**
4. Add email settings:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
MAIL_FROM=noreply@penasia.edu.hk
```

### Step 2: Get Gmail App Password

1. Go to **https://myaccount.google.com/security**
2. Enable 2-Factor Authentication
3. Go to **App passwords**
4. Select **Mail** and **Windows Computer**
5. Copy the 16-character password
6. Paste in `SMTP_PASSWORD` environment variable

### Step 3: Test Email Service

```bash
cd /home/imjdpk/mysite
source venv/bin/activate

python << 'EOF'
from email_service import email_service
result = email_service.send_email(
    'your-email@gmail.com',
    'Test Email',
    'This is a test email from PythonAnywhere!'
)
print(f"Email sent: {result}")
EOF
```

---

## Static Files & Media

### Step 1: Configure Static Files

1. Go to **Web** menu
2. Click your web app
3. Scroll to **Static files** section
4. Click **Add a new static files mapping**
5. Add mapping:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/imjdpk/mysite/static` |

6. Click **Save**

### Step 2: Collect Static Files

```bash
cd /home/imjdpk/mysite
source venv/bin/activate
python -c "from app import app; app.run()" &
# Or manually copy files
cp -r static/* /home/imjdpk/mysite/static/
```

### Step 3: Upload Media Files

```bash
# Create directories for uploads
mkdir -p /home/imjdpk/mysite/uploads/courses
mkdir -p /home/imjdpk/mysite/uploads/profiles
mkdir -p /home/imjdpk/mysite/uploads/documents

# Set permissions
chmod -R 755 /home/imjdpk/mysite/uploads
```

---

## SSL/HTTPS Setup

### Option 1: Free SSL (Beginner+ Plan)

1. Go to **Web** menu
2. Click your web app
3. Scroll to **Security** section
4. Click **Force HTTPS**
5. PythonAnywhere will set up free SSL automatically

**Setup takes 5-10 minutes**

### Option 2: Custom Domain with SSL

1. Register domain (e.g., penasia.edu.hk)
2. Go to **Web** → **Domain settings**
3. Add your domain
4. Configure DNS:
   - Add CNAME: `www` → `imjdpk.pythonanywhere.com`
   - Or A record → PythonAnywhere IP
5. PythonAnywhere auto-generates SSL certificate (Let's Encrypt)

### Verify SSL

```bash
# Test HTTPS connection
curl -I https://imjdpk.pythonanywhere.com

# Should see:
# HTTP/2 200
# Strict-Transport-Security: max-age=31536000
```

---

## Monitoring & Logs

### View Error Logs

1. Go to **Web** menu
2. Click your web app
3. Scroll to **Logs** section
4. Click **Error log**

Or via console:
```bash
tail -50 /var/log/imjdpk.pythonanywhere.com.error.log
```

### View Access Logs

1. Go to **Web** menu
2. Click **Access log**

Or via console:
```bash
tail -50 /var/log/imjdpk.pythonanywhere.com.access.log
```

### Monitor Performance

1. Go to **Dashboard**
2. Check:
   - CPU time usage
   - Quota usage
   - Web app status

### Set Up Scheduled Tasks

1. Go to **Tasks** menu
2. Click **Create a new scheduled task**
3. Set up maintenance tasks:

```bash
# Daily backup at 2 AM
02 * * * * cd /home/imjdpk/mysite && tar -czf backups/db_$(date +\%Y\%m\%d).tar.gz instance/
```

---

## Updates & Maintenance

### Pull Latest Code from GitHub

```bash
cd /home/imjdpk/mysite
git pull origin main
```

### Update Dependencies

```bash
cd /home/imjdpk/mysite
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Reload Web App

**Method 1: Via Web Console**
1. Go to **Web** menu
2. Click your app
3. Click green **Reload** button

**Method 2: Via Console**
```bash
touch /home/imjdpk/mysite/flask_app.wsgi
```

**Method 3: Touch WSGI File**
```bash
cd /home/imjdpk/mysite
touch /var/www/imjdpk_pythonanywhere_com_wsgi.py
```

### Run Database Migrations

```bash
cd /home/imjdpk/mysite
source venv/bin/activate
flask db upgrade
```

### Update Complete Checklist

```bash
# 1. Pull latest code
git pull origin main

# 2. Activate venv
source venv/bin/activate

# 3. Update dependencies
pip install -r requirements.txt --upgrade

# 4. Run migrations
flask db upgrade

# 5. Reload app
# (via Web console or touch WSGI)

# 6. Verify
# Visit https://imjdpk.pythonanywhere.com
```

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
cd /home/imjdpk/mysite
source venv/bin/activate
pip install -r requirements.txt
touch /var/www/imjdpk_pythonanywhere_com_wsgi.py
```

### Issue 2: "502 Bad Gateway"

**Causes & Solutions:**
1. Virtual environment not activated in WSGI file
2. Syntax error in code
3. Missing dependencies

**Debug:**
```bash
# Check error log
tail -100 /var/log/imjdpk.pythonanywhere.com.error.log

# Test Flask app directly
cd /home/imjdpk/mysite
source venv/bin/activate
python -c "from app import app; print('App imported successfully!')"
```

### Issue 3: "404 Not Found" on static files

**Solution:**
1. Go to **Web** menu
2. Verify static files mapping exists
3. Check directory permissions:
```bash
chmod -R 755 /home/imjdpk/mysite/static
```

### Issue 4: Database errors

**Solution:**
```bash
cd /home/imjdpk/mysite
source venv/bin/activate

# Check database
python << 'EOF'
from app import app, db
with app.app_context():
    try:
        db.session.execute("SELECT 1")
        print("✅ Database is healthy!")
    except Exception as e:
        print(f"❌ Database error: {e}")
EOF

# Reset if necessary
rm instance/penasia.db
python << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Database reset!")
EOF
```

### Issue 5: Emails not sending

**Solution:**
1. Verify SMTP credentials in environment variables
2. Check Gmail app password (not regular password)
3. Test email service:
```bash
python << 'EOF'
from email_service import email_service
result = email_service.send_email('test@example.com', 'Test', 'Test email')
print(f"Result: {result}")
EOF
```

### Issue 6: Changes not reflecting after update

**Solution:**
1. Clear Python cache:
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

2. Hard refresh browser: `Ctrl+Shift+R`
3. Reload web app
4. Clear browser cache manually

### Issue 7: "Permission denied" errors

**Solution:**
```bash
# Fix permissions
chmod -R 755 /home/imjdpk/mysite
chmod -R 775 /home/imjdpk/mysite/instance
chmod -R 775 /home/imjdpk/mysite/uploads

# Check permissions
ls -la /home/imjdpk/mysite/
```

---

## Backup & Recovery

### Step 1: Set Up Regular Backups

```bash
# Create backup directory
mkdir -p /home/imjdpk/backups

# Backup database (manual)
cd /home/imjdpk/mysite
cp instance/penasia.db /home/imjdpk/backups/penasia_$(date +%Y%m%d_%H%M%S).db

# Backup entire project
tar -czf /home/imjdpk/backups/mysite_$(date +%Y%m%d_%H%M%S).tar.gz /home/imjdpk/mysite
```

### Step 2: Automated Daily Backup

1. Go to **Tasks** menu
2. Click **Create a new scheduled task**
3. Time: `02:00` (2 AM UTC)
4. Command:
```bash
cd /home/imjdpk && tar -czf backups/backup_$(date +\%Y\%m\%d).tar.gz mysite/instance/
```

### Step 3: Restore from Backup

```bash
# Restore database
cp /home/imjdpk/backups/penasia_YYYYMMDD_HHMMSS.db /home/imjdpk/mysite/instance/penasia.db

# Restore entire project
cd /home/imjdpk
tar -xzf backups/mysite_YYYYMMDD_HHMMSS.tar.gz

# Verify
cd mysite
source venv/bin/activate
python -c "from app import app; print('✅ App restored!')"
```

---

## Post-Deployment Checklist

### Immediate (After Deployment)

- [ ] Access website: https://imjdpk.pythonanywhere.com
- [ ] Test homepage loads
- [ ] Test login page
- [ ] Test course listing
- [ ] Test application form
- [ ] Test admin login
- [ ] Check error logs for any warnings
- [ ] Verify SSL certificate (HTTPS working)
- [ ] Test email sending
- [ ] Check static files load (CSS, JS, images)

### Configuration (First Week)

- [ ] Update admin password (not default `admin123`)
- [ ] Configure SMTP email
- [ ] Set up payment gateway keys (if using)
- [ ] Configure database backup schedule
- [ ] Set up error monitoring
- [ ] Test all critical workflows
- [ ] Verify responsive design on mobile
- [ ] Check performance metrics

### Ongoing Maintenance

- [ ] Monitor error logs daily
- [ ] Check disk usage weekly
- [ ] Update dependencies monthly
- [ ] Review access logs weekly
- [ ] Backup database daily
- [ ] Test backup restoration monthly
- [ ] Update security patches promptly
- [ ] Monitor uptime/availability

---

## Useful Commands for PythonAnywhere

### SSH Connection

```bash
ssh imjdpk@ssh.pythonanywhere.com
```

### List Running Processes

```bash
ps aux | grep python
```

### Check Disk Usage

```bash
df -h
du -sh /home/imjdpk/mysite
```

### Test Web App

```bash
curl -I https://imjdpk.pythonanywhere.com
```

### View Python Version

```bash
python3 --version
```

### List Environment Variables

```bash
env | grep -E "FLASK|DATABASE|SMTP"
```

---

## Performance Optimization Tips

### 1. Enable Caching

Add to `app.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/courses')
@cache.cached(timeout=300)
def courses():
    # Your code
```

### 2. Optimize Database Queries

```python
# Good: eager load relationships
courses = Course.query.options(joinedload('enrollments')).all()

# Bad: N+1 queries
courses = Course.query.all()
for course in courses:
    print(len(course.enrollments))  # Additional query per course!
```

### 3. Compress Static Files

```bash
gzip -9 static/css/style.css
gzip -9 static/js/main.js
```

### 4. Use CDN for Static Files

Configure CloudFlare or similar for:
- Static files (CSS, JS)
- Images
- Fonts

---

## Security Best Practices

### 1. Change Default Credentials

```bash
# After first deployment, change admin password
# Log in and update admin account
```

### 2. Use Environment Variables

Never commit secrets to GitHub:
```bash
# ❌ Don't do this
SECRET_KEY = "my-secret-key"

# ✅ Do this
import os
SECRET_KEY = os.getenv('SECRET_KEY')
```

### 3. Enable HTTPS

- [x] PythonAnywhere automatically sets up free SSL
- [x] Enable "Force HTTPS" in Web settings
- [x] Update links to use https://

### 4. Regular Security Updates

```bash
# Update dependencies regularly
pip install -r requirements.txt --upgrade

# Check for vulnerabilities
pip install safety
safety check
```

### 5. Database Security

- Use strong database password
- Backup regularly
- Verify backups can be restored
- Restrict database access

---

## Monitoring & Analytics

### Set Up Monitoring

1. Go to **Dashboard**
2. Monitor:
   - CPU time (green zone = < 80% of quota)
   - Web app status (should be green)
   - Disk usage (< 80% of quota)

### Access Logs Analysis

```bash
# See most requested pages
tail -1000 /var/log/imjdpk.pythonanywhere.com.access.log | \
  awk '{print $7}' | sort | uniq -c | sort -rn | head -20

# See error status codes
tail -1000 /var/log/imjdpk.pythonanywhere.com.access.log | \
  awk '{print $9}' | sort | uniq -c | sort -rn
```

---

## Useful Links

| Resource | URL |
|----------|-----|
| **PythonAnywhere** | https://www.pythonanywhere.com |
| **Dashboard** | https://www.pythonanywhere.com/user/imjdpk/account |
| **Web Apps** | https://www.pythonanywhere.com/user/imjdpk/webapps |
| **Databases** | https://www.pythonanywhere.com/user/imjdpk/databases |
| **Consoles** | https://www.pythonanywhere.com/user/imjdpk/consoles |
| **Tasks** | https://www.pythonanywhere.com/user/imjdpk/tasks |
| **Files** | https://www.pythonanywhere.com/user/imjdpk/files |
| **Help** | https://help.pythonanywhere.com |
| **Status** | https://www.pythonanywhere.com/status/ |

---

## Quick Reference: Common Tasks

### Update Website

```bash
# 1. Push to GitHub (from local machine)
git push origin main

# 2. SSH into PythonAnywhere
ssh imjdpk@ssh.pythonanywhere.com

# 3. Pull latest code
cd mysite
git pull origin main

# 4. Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. Run migrations (if needed)
flask db upgrade

# 6. Reload app
# (via Web dashboard or touch WSGI file)

# 7. Verify
# Visit https://imjdpk.pythonanywhere.com
```

### View Errors

```bash
# View recent errors
tail -50 /var/log/imjdpk.pythonanywhere.com.error.log

# Search for specific error
grep "ERROR" /var/log/imjdpk.pythonanywhere.com.error.log

# Follow log in real-time
tail -f /var/log/imjdpk.pythonanywhere.com.error.log
```

### Database Maintenance

```bash
cd /home/imjdpk/mysite
source venv/bin/activate

# Check database health
python << 'EOF'
from app import app, db
with app.app_context():
    result = db.session.execute("SELECT COUNT(*) FROM user")
    print(f"Total users: {result.scalar()}")
EOF

# Backup
cp instance/penasia.db /home/imjdpk/backups/penasia_backup.db
```

---

## Support & Help

**If you encounter issues:**

1. **Check error logs** first: `/var/log/imjdpk.pythonanywhere.com.error.log`
2. **Review this guide** for troubleshooting section
3. **Visit PythonAnywhere Help**: https://help.pythonanywhere.com
4. **Check Flask documentation**: https://flask.palletsprojects.com/
5. **Review project documentation**: See DOCUMENTATION_INDEX.md

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-11 | 1.0 | Initial comprehensive guide |

---

**You're ready to deploy on PythonAnywhere! 🚀**

This guide covers everything from initial setup through production maintenance. Bookmark this page for quick reference!

**Questions? Check the Troubleshooting section or visit PythonAnywhere Help.**
