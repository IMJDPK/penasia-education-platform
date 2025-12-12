# 🖥️ PenAsia Project - Bash Commands Reference
**Date:** December 11, 2025  
**Purpose:** Quick reference for all common bash commands used in project management

---

## 🚀 Quick Start Commands

### Start the Application (Development)
```bash
cd "/home/imjd/Hong Kong University/Flask Website"
source flask_env/bin/activate
python app.py
```

**Access:** http://localhost:5000

### Stop the Application
```bash
pkill -f "python.*app.py"
```

### Run in Background
```bash
cd "/home/imjd/Hong Kong University/Flask Website"
source flask_env/bin/activate
python app.py &
```

---

## 📁 Directory Navigation

### Navigate to Project
```bash
cd "/home/imjd/Hong Kong University/Flask Website"
```

### Show Current Directory
```bash
pwd
```

### List Files in Current Directory
```bash
ls
```

### List with Detailed Info
```bash
ls -la
```

### List Only Directories
```bash
ls -d */
```

### Navigate to Templates
```bash
cd "/home/imjd/Hong Kong University/Flask Website/templates"
```

### Navigate to Static Files
```bash
cd "/home/imjd/Hong Kong University/Flask Website/static"
```

### Create New Directory
```bash
mkdir new_folder_name
```

### Remove Directory
```bash
rm -r directory_name
```

---

## 🐍 Python & Flask Commands

### Activate Virtual Environment
```bash
source flask_env/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Check Python Version
```bash
python --version
python3 --version
```

### Check Python Installation Location
```bash
which python
which python3
```

### Install Python Packages
```bash
pip install flask
pip install -r requirements.txt
```

### Upgrade All Packages
```bash
pip install -r requirements.txt --upgrade
```

### List Installed Packages
```bash
pip list
```

### Show Package Details
```bash
pip show flask
```

### Run Python Script
```bash
python create_sample_data.py
python test_admin.py
python demo_assignment_system.py
```

### Run Python in Interactive Mode
```bash
python
```

### Execute Python Command Directly
```bash
python -c "print('Hello World')"
```

### Check Syntax of Python File
```bash
python -m py_compile app.py
```

---

## 🗄️ Database Commands

### Create Database Tables
```bash
python << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("Database tables created!")
EOF
```

### Reset Database
```bash
rm instance/penasia.db
python << 'EOF'
from app import app, db
with app.app_context():
    db.create_all()
    print("Database reset!")
EOF
```

### Run Database Migrations
```bash
flask db upgrade
```

### Create New Migration
```bash
flask db migrate -m "Add new field"
flask db upgrade
```

### Check Database Status
```bash
python << 'EOF'
from app import app, db, User
with app.app_context():
    users = User.query.all()
    print(f"Total users: {len(users)}")
EOF
```

### View All Users
```bash
python << 'EOF'
from app import app, User
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"{u.id}: {u.email} ({u.role})")
EOF
```

### Create Admin User
```bash
python << 'EOF'
from app import app, db, User
with app.app_context():
    admin = User(
        email='admin@penasia.edu.hk',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
EOF
```

### Delete User by Email
```bash
python << 'EOF'
from app import app, db, User
with app.app_context():
    user = User.query.filter_by(email='user@example.com').first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("User deleted!")
    else:
        print("User not found!")
EOF
```

---

## 📦 Project File Commands

### Count Lines of Python Code
```bash
wc -l app.py
```

### Count Total Lines in All Python Files
```bash
find . -name "*.py" -type f | xargs wc -l | tail -1
```

### Count HTML Templates
```bash
find templates -name "*.html" | wc -l
```

### List All Python Files
```bash
find . -name "*.py" -type f
```

### Find Large Files
```bash
ls -lhS | head -20
```

### Find Recently Modified Files
```bash
find . -type f -mtime -1
```

### View File Size
```bash
du -h app.py
```

### View Directory Size
```bash
du -sh .
```

---

## 🔍 Search & Grep Commands

### Search Text in All Python Files
```bash
grep -r "search_term" --include="*.py"
```

### Search with Line Numbers
```bash
grep -n "search_term" app.py
```

### Search Case-Insensitive
```bash
grep -i "search_term" app.py
```

### Search Whole Words Only
```bash
grep -w "search_term" app.py
```

### Find Files Containing Text
```bash
grep -r "TODO" . --include="*.py"
```

### Count Occurrences
```bash
grep -c "search_term" app.py
```

### Show Context (lines before/after)
```bash
grep -B 2 -A 2 "search_term" app.py
```

### Search in Specific Directory
```bash
grep -r "search_term" templates/
```

---

## 🔧 File Editing Commands

### View File Contents
```bash
cat app.py
```

### View File with Line Numbers
```bash
cat -n app.py
```

### View First 50 Lines
```bash
head -50 app.py
```

### View Last 50 Lines
```bash
tail -50 app.py
```

### View Specific Lines (10-20)
```bash
sed -n '10,20p' app.py
```

### Edit File with Nano
```bash
nano app.py
```

### Edit File with Vim
```bash
vim app.py
```

### Copy File
```bash
cp source.py backup.py
```

### Move/Rename File
```bash
mv old_name.py new_name.py
```

### Delete File
```bash
rm file_name.py
```

### Create Empty File
```bash
touch new_file.py
```

---

## 📝 Git Commands

### Check Git Status
```bash
git status
```

### Add Files
```bash
git add .
git add filename.py
git add *.py
```

### Commit Changes
```bash
git commit -m "Your commit message"
```

### Push to GitHub
```bash
git push origin main
```

### Pull from GitHub
```bash
git pull origin main
```

### View Commit History
```bash
git log
git log --oneline
git log --oneline -10
```

### View Changes
```bash
git diff
git diff filename.py
```

### Show Specific Commit
```bash
git show abc1234
```

### Create New Branch
```bash
git branch feature-name
```

### Switch Branch
```bash
git checkout branch-name
```

### Create and Switch Branch
```bash
git checkout -b feature-name
```

### List Branches
```bash
git branch -a
```

### Delete Branch
```bash
git branch -d branch-name
```

### Check Remote URL
```bash
git remote -v
```

### Change Remote URL
```bash
git remote set-url origin https://github.com/IMJDPK/penasia-education-platform.git
```

### Stash Changes
```bash
git stash
git stash pop
```

### Undo Last Commit (keep changes)
```bash
git reset --soft HEAD~1
```

### View File History
```bash
git log --oneline -- filename.py
```

---

## 🧪 Testing Commands

### Run Test File
```bash
python test_admin.py
python test_apply_flow.py
python test_complete_funnel.py
```

### Run All Tests
```bash
python -m pytest
```

### Run Tests with Verbose Output
```bash
python -m pytest -v
```

### Run Specific Test
```bash
python -m pytest test_admin.py::test_login
```

### Run Demo Scripts
```bash
python demo_assignment_system.py
python create_sample_data.py
```

---

## 🔐 Permissions & Ownership

### Change File Permissions
```bash
chmod 644 file.py          # Read/write for owner, read for others
chmod 755 directory/       # Full permissions for owner
chmod +x script.sh         # Make executable
```

### Change Owner
```bash
chown user:group file.py
```

### View File Permissions
```bash
ls -la
```

---

## 📊 System & Process Commands

### Check Running Processes
```bash
ps aux | grep python
```

### Find Process by Name
```bash
pgrep -f "python.*app.py"
```

### Kill Process by Name
```bash
pkill -f "python.*app.py"
```

### Kill Process by PID
```bash
kill 12345
```

### Force Kill Process
```bash
kill -9 12345
```

### Check CPU and Memory Usage
```bash
top
```

### Check Disk Space
```bash
df -h
```

### Check Folder Size
```bash
du -sh *
```

### Monitor System Resources
```bash
watch -n 1 'free -h'
```

---

## 🌐 Network & Server Commands

### Check if Port is Open
```bash
lsof -i :5000
netstat -tuln | grep 5000
```

### Check Network Interfaces
```bash
ifconfig
ip addr
```

### Test Network Connectivity
```bash
ping google.com
```

### Check DNS
```bash
nslookup google.com
dig google.com
```

### Download File
```bash
wget https://example.com/file.zip
curl -O https://example.com/file.zip
```

---

## 📦 Backup & Archive Commands

### Create Backup of Project
```bash
tar -czf penasia_backup.tar.gz "/home/imjd/Hong Kong University/Flask Website"
```

### Extract Backup
```bash
tar -xzf penasia_backup.tar.gz
```

### Compress Directory
```bash
gzip filename.txt
```

### Decompress
```bash
gunzip filename.txt.gz
```

### Create Zip Archive
```bash
zip -r penasia_backup.zip "/home/imjd/Hong Kong University/Flask Website"
```

### Extract Zip
```bash
unzip penasia_backup.zip
```

### Copy Directory Recursively
```bash
cp -r source_dir/ destination_dir/
```

---

## 🐚 Useful Aliases

### Create Shortcuts (add to ~/.bashrc)
```bash
# Navigation
alias pjt='cd "/home/imjd/Hong Kong University/Flask Website"'
alias activate='source flask_env/bin/activate'

# Common Git commands
alias gst='git status'
alias gadd='git add .'
alias gcom='git commit -m'
alias gpush='git push origin main'
alias gpull='git pull origin main'

# Python commands
alias pystart='python app.py'
alias pytest='python -m pytest'

# Quick commands
alias countpy='find . -name "*.py" -type f | xargs wc -l | tail -1'
alias counthtml='find templates -name "*.html" | wc -l'
alias ls='ls -la'
```

### Load Aliases
```bash
source ~/.bashrc
```

---

## 📱 PythonAnywhere Commands

### SSH to PythonAnywhere
```bash
ssh imjdpk@ssh.pythonanywhere.com
```

### Pull Latest on PythonAnywhere
```bash
cd /home/imjdpk/mysite
git pull origin main
```

### Reload App on PythonAnywhere
```bash
touch /home/imjdpk/mysite/flask_app.wsgi
```

### Check Error Log on PythonAnywhere
```bash
tail -50 /var/log/imjdpk.pythonanywhere.com.error.log
```

---

## 🔧 Environment Variables

### Set Environment Variable (temporary)
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
```

### View Environment Variable
```bash
echo $FLASK_ENV
```

### View All Environment Variables
```bash
env
```

### Create .env File
```bash
cat > .env << 'EOF'
FLASK_ENV=development
SECRET_KEY=your-secret-key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EOF
```

### Load Environment Variables from .env
```bash
source .env
```

---

## 📋 Cheat Sheet - Most Used Commands

```bash
# Navigation
cd "/home/imjd/Hong Kong University/Flask Website"
ls -la
pwd

# Virtual Environment
source flask_env/bin/activate
deactivate

# Start/Stop App
python app.py
pkill -f "python.*app.py"

# Git Workflow
git status
git add .
git commit -m "message"
git push origin main
git pull origin main

# Database
flask db upgrade
python create_sample_data.py

# File Operations
cp source dest
mv old new
rm file
cat filename
grep "search" file

# Process Management
ps aux | grep python
pgrep -f "python.*app.py"
kill -9 12345

# Testing
python test_admin.py
python test_apply_flow.py

# System Info
df -h
du -sh .
ps aux
```

---

## 🎯 Common Workflow

### Daily Development Workflow
```bash
# Start your day
cd "/home/imjd/Hong Kong University/Flask Website"
source flask_env/bin/activate
git pull origin main
python app.py

# Make changes to files...

# End of day - push changes
git add .
git commit -m "Describe your changes"
git push origin main

# Stop the app
pkill -f "python.*app.py"
```

### Deployment Workflow
```bash
# 1. Test locally
python test_admin.py
python test_apply_flow.py

# 2. Commit and push
git add .
git commit -m "Feature complete"
git push origin main

# 3. Deploy to PythonAnywhere
ssh imjdpk@ssh.pythonanywhere.com
cd /home/imjdpk/mysite
git pull origin main
touch flask_app.wsgi
exit

# 4. Verify
# Visit https://imjdpk.pythonanywhere.com
# Test critical features
```

---

## 🆘 Troubleshooting Commands

### Check What's Using Port 5000
```bash
lsof -i :5000
```

### View Recent Error Logs
```bash
tail -100 /var/log/imjdpk.pythonanywhere.com.error.log
```

### Check Database Integrity
```bash
python << 'EOF'
from app import app, db
with app.app_context():
    try:
        db.session.execute("SELECT 1")
        print("Database is healthy!")
    except Exception as e:
        print(f"Database error: {e}")
EOF
```

### Test Email Service
```bash
python << 'EOF'
from email_service import email_service
result = email_service.send_email('test@example.com', 'Test', 'This is a test')
print(f"Email sent: {result}")
EOF
```

### Clear Python Cache
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

---

## 📚 Learning Resources

### Get Help on Commands
```bash
man ls
ls --help
python --help
git --help
```

### View System Manual
```bash
man bash
```

---

## ✅ Command Categories Quick Reference

| Category | Key Commands |
|----------|--------------|
| **Navigation** | cd, ls, pwd, mkdir |
| **File Ops** | cp, mv, rm, cat, grep |
| **Git** | status, add, commit, push, pull |
| **Python** | python, pip, flask |
| **Database** | flask db, python scripts |
| **Process** | ps, kill, pkill, pgrep |
| **System** | df, du, top, free |
| **Network** | ping, ifconfig, netstat |
| **Archive** | tar, zip, gzip |

---

## 🚀 You're Ready!

Save this guide and refer to it whenever you need to run bash commands. Most of these commands are essential for Flask development and deployment!

**Happy coding! 💻**
