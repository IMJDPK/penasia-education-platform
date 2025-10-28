# PenAsia LMS - Complete Deployment Guide

## 📋 Pre-Deployment Checklist

Before deploying, ensure you've completed these steps:

- [ ] All features tested locally
- [ ] Database migrations up to date
- [ ] Static files optimized
- [ ] Environment variables configured
- [ ] SECRET_KEY changed from default
- [ ] DEBUG mode set to False
- [ ] CSRF protection enabled
- [ ] Email service configured
- [ ] Database backup created
- [ ] Requirements.txt updated

## 🚀 Deployment Options

### Option 1: Quick Deploy - PythonAnywhere (Easiest, Free Tier)
**Best for:** Testing, small-scale deployment, learning
**Cost:** Free tier available (500MB storage, 1 web app)

### Option 2: Professional Deploy - DigitalOcean/AWS/Linode
**Best for:** Production use, scalability, full control
**Cost:** $5-20/month depending on resources

### Option 3: Platform as a Service - Heroku/Railway
**Best for:** Quick deployment, automatic scaling
**Cost:** Free to $7/month for basic tier

### Option 4: Vercel Deployment (Serverless)
**Best for:** Static content, API routes, modern frameworks
**Cost:** Free tier available (100GB bandwidth)
**⚠️ Note:** Flask requires serverless adaptation, external database needed

---

## 🎯 Option 1: PythonAnywhere Deployment (Recommended for Beginners)

### Step 1: Prepare Your Project

```bash
# 1. Create requirements.txt if not exists
pip freeze > requirements.txt

# 2. Add to requirements.txt if missing:
gunicorn==21.2.0
python-dotenv==1.0.0

# 3. Create .env file for production settings
touch .env
```

### Step 2: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com/
2. Click "Pricing & signup"
3. Create a free Beginner account
4. Confirm your email

### Step 3: Upload Your Project

**Option A: Using Git (Recommended)**
```bash
# On your local machine, push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main

# On PythonAnywhere Console (Bash):
git clone YOUR_GITHUB_REPO_URL
cd Flask\ Website
```

**Option B: Upload Files Directly**
1. Go to "Files" tab
2. Create folder: `/home/yourusername/Flask Website`
3. Upload all files (or use "Upload a file" button)

### Step 4: Set Up Virtual Environment

In PythonAnywhere Bash Console:
```bash
cd ~/Flask\ Website
python3.10 -m venv flask_env
source flask_env/bin/activate
pip install -r requirements.txt
```

### Step 5: Configure Database

```bash
# Create instance directory
mkdir -p instance

# Initialize database
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("Database created!")
EOF
```

### Step 6: Create WSGI Configuration

Go to "Web" tab → "Add a new web app" → Manual configuration → Python 3.10

Edit the WSGI configuration file (click on it):

```python
# /var/www/yourusername_pythonanywhere_com_wsgi.py

import sys
import os

# Add your project directory to the sys.path
project_folder = '/home/yourusername/Flask Website'
if project_folder not in sys.path:
    sys.path.insert(0, project_folder)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-super-secret-production-key-change-this'

# Import Flask app
from app import app as application
```

### Step 7: Configure Virtual Environment

In Web tab, under "Virtualenv":
- Enter: `/home/yourusername/Flask Website/flask_env`

### Step 8: Set Static Files

In Web tab, under "Static files":
- URL: `/static/`
- Directory: `/home/yourusername/Flask Website/static`

### Step 9: Configure App for Production

Edit `app.py` to add production config:

```python
import os

# At the top of app.py, add:
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    # Force HTTPS
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

### Step 10: Reload and Test

1. Click "Reload" button in Web tab
2. Visit: `https://yourusername.pythonanywhere.com`
3. Test all features

---

## 🏢 Option 2: DigitalOcean/AWS Deployment (Production-Grade)

### Step 1: Set Up Server

**Create Droplet/EC2 Instance:**
- OS: Ubuntu 22.04 LTS
- Size: Basic ($6/month - 1GB RAM, 1 CPU)
- Region: Choose closest to your users
- Authentication: SSH keys (recommended)

### Step 2: Initial Server Setup

```bash
# SSH into your server
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3-pip python3-venv nginx supervisor postgresql postgresql-contrib -y

# Create deployment user
adduser penasia
usermod -aG sudo penasia
su - penasia
```

### Step 3: Clone and Setup Project

```bash
# Clone your project
git clone YOUR_GITHUB_REPO_URL
cd Flask\ Website

# Create virtual environment
python3 -m venv flask_env
source flask_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### Step 4: Configure PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE penasia_lms;
CREATE USER penasiauser WITH PASSWORD 'strong_password_here';
ALTER ROLE penasiauser SET client_encoding TO 'utf8';
ALTER ROLE penasiauser SET default_transaction_isolation TO 'read committed';
ALTER ROLE penasiauser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE penasia_lms TO penasiauser;
\q
```

### Step 5: Update App Configuration

Create `config.py`:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://penasiauser:strong_password_here@localhost/penasia_lms'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': ProductionConfig
}
```

Update `app.py`:

```python
from config import config
import os

# Replace existing config with:
config_name = os.environ.get('FLASK_CONFIG', 'production')
app.config.from_object(config[config_name])
```

### Step 6: Set Environment Variables

```bash
# Create .env file
cat > .env << EOF
SECRET_KEY='generate-a-very-long-random-string-here'
DATABASE_URL='postgresql://penasiauser:strong_password_here@localhost/penasia_lms'
FLASK_CONFIG='production'
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USERNAME='your-email@gmail.com'
MAIL_PASSWORD='your-app-password'
EOF

# Load environment variables
source .env
```

### Step 7: Initialize Database

```bash
source flask_env/bin/activate
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("Database initialized!")
EOF
```

### Step 8: Configure Gunicorn

Create `gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
threads = 2
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
accesslog = '/home/penasia/Flask Website/logs/gunicorn-access.log'
errorlog = '/home/penasia/Flask Website/logs/gunicorn-error.log'
loglevel = 'info'
```

Create logs directory:
```bash
mkdir -p logs
```

### Step 9: Configure Supervisor (Process Manager)

```bash
sudo nano /etc/supervisor/conf.d/penasia.conf
```

Add:

```ini
[program:penasia]
directory=/home/penasia/Flask Website
command=/home/penasia/Flask Website/flask_env/bin/gunicorn -c gunicorn_config.py app:app
user=penasia
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/penasia/penasia.err.log
stdout_logfile=/var/log/penasia/penasia.out.log
environment=PATH="/home/penasia/Flask Website/flask_env/bin",FLASK_CONFIG="production"
```

Create log directory and restart supervisor:

```bash
sudo mkdir -p /var/log/penasia
sudo chown penasia:penasia /var/log/penasia
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start penasia
```

### Step 10: Configure Nginx (Web Server)

```bash
sudo nano /etc/nginx/sites-available/penasia
```

Add:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    client_max_body_size 20M;
    
    location /static/ {
        alias /home/penasia/Flask Website/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/penasia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 11: Configure SSL with Let's Encrypt (Free HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow prompts and choose redirect HTTP to HTTPS
```

### Step 12: Configure Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Step 13: Set Up Automated Backups

Create backup script:

```bash
nano ~/backup.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR="/home/penasia/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
pg_dump penasia_lms > $BACKUP_DIR/db_$DATE.sql

# Backup uploaded files (if any)
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /home/penasia/Flask\ Website/instance/

# Keep only last 7 days of backups
find $BACKUP_DIR -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable and add to crontab:

```bash
chmod +x ~/backup.sh
crontab -e

# Add daily backup at 2 AM:
0 2 * * * /home/penasia/backup.sh
```

---

## 🚂 Option 3: Railway Deployment (Modern Platform)

### Step 1: Prepare Project

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:

```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

Update `requirements.txt`:

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
Flask-Mail==0.9.1
Flask-Migrate==4.0.5
email-validator==2.0.0
WTForms==3.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.7
python-dotenv==1.0.0
```

### Step 2: Deploy to Railway

1. Go to https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys

### Step 3: Add PostgreSQL Database

1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway automatically sets `DATABASE_URL` environment variable
3. Update app.py to use it:

```python
import os
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

### Step 4: Set Environment Variables

In Railway dashboard:
- Variables tab
- Add: `SECRET_KEY`, `FLASK_ENV=production`

### Step 5: Deploy

Push to GitHub - Railway auto-deploys on every push!

---

## 🔒 Production Security Checklist

### Essential Security Updates

1. **Change SECRET_KEY**
```python
# Use a strong random key
import secrets
print(secrets.token_hex(32))
# Use this as your SECRET_KEY
```

2. **Disable DEBUG Mode**
```python
app.config['DEBUG'] = False
```

3. **Use Environment Variables**
```python
import os
from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

4. **Configure HTTPS Only**
```python
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

5. **Set Up CORS Properly**
```python
from flask_cors import CORS
CORS(app, origins=['https://yourdomain.com'])
```

6. **Rate Limiting**
```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
```

7. **Input Validation**
- Already using WTForms ✓
- CSRF protection enabled ✓

8. **SQL Injection Protection**
- Using SQLAlchemy ORM ✓

---

## 📧 Email Configuration

### Using Gmail (Free)

```python
# In app.py
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Use App Password
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@penasia.edu.hk'
```

**Generate Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. App Passwords → Generate for "Mail"
4. Use this 16-character password

### Using SendGrid (Recommended for Production)

```bash
pip install sendgrid
```

```python
app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY')
```

---

## 🔄 Deployment Workflow

### Quick Update Process

**For PythonAnywhere:**
```bash
cd ~/Flask\ Website
git pull origin main
source flask_env/bin/activate
pip install -r requirements.txt
# Click "Reload" in Web tab
```

**For DigitalOcean/VPS:**
```bash
cd ~/Flask\ Website
git pull origin main
source flask_env/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart penasia
```

**For Railway:**
```bash
git push origin main
# Automatic deployment!
```

**For Vercel:**
```bash
git push origin main
# Automatic deployment!
# Or use: vercel --prod
```

---

## 🔷 Option 4: Vercel Deployment (Serverless)

### ⚠️ Important Considerations

**Limitations with Flask on Vercel:**
- No persistent file system (must use external database)
- Serverless function timeout (10-50 seconds)
- Cold starts may cause first request delays
- Session management needs external store (Redis)

**Recommended for:**
- API-first Flask apps
- Apps with external PostgreSQL/MySQL
- Serverless microservices
- Apps that can tolerate cold starts

**NOT recommended if you need:**
- File uploads to local storage
- Long-running background tasks
- WebSocket connections
- Sqlite database

### Step 1: Prepare Project for Serverless

Create `vercel.json` in project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### Step 2: Create Vercel Entry Point

Create `api/index.py`:

```python
from app import app

# Vercel requires the app to be named 'app' or exported as handler
def handler(request):
    return app(request.environ, request.start_response)

# For Vercel
app = app
```

Or update `vercel.json` to point directly to app:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Step 3: Update Requirements for Vercel

Ensure your `requirements.txt` doesn't include system-level packages:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
Flask-Mail==0.9.1
Flask-Migrate==4.0.5
email-validator==2.0.0
WTForms==3.0.1
# Don't include gunicorn for Vercel
# Don't include psycopg2-binary (Vercel provides it)
python-dotenv==1.0.0
```

### Step 4: Configure External Database

Vercel doesn't provide database. Use external service:

**Option A: Neon (PostgreSQL - Recommended)**
- Free tier: 3GB storage
- Serverless PostgreSQL
- Sign up: https://neon.tech/

**Option B: PlanetScale (MySQL)**
- Free tier: 5GB storage
- Serverless MySQL
- Sign up: https://planetscale.com/

**Option C: Supabase (PostgreSQL)**
- Free tier: 500MB database
- Includes auth, storage
- Sign up: https://supabase.com/

### Step 5: Update Database Configuration

In `app.py`, update for Vercel:

```python
import os
from urllib.parse import urlparse

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Parse URL for Vercel compatibility
    url = urlparse(DATABASE_URL)
    
    # Convert postgres:// to postgresql:// if needed
    if url.scheme == 'postgres':
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Fallback to SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/penasia.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### Step 6: Handle File Uploads

Since Vercel has no persistent storage, use cloud storage:

**Option A: Vercel Blob Storage**
```bash
npm install -g vercel
```

```python
import os

# For file uploads, use Vercel Blob or S3
UPLOAD_FOLDER = os.environ.get('VERCEL_BLOB_URL') or '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```

**Option B: AWS S3**
```bash
pip install boto3
```

```python
import boto3
from werkzeug.utils import secure_filename

s3_client = boto3.client('s3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)

def upload_to_s3(file, bucket_name, folder='uploads'):
    filename = secure_filename(file.filename)
    key = f"{folder}/{filename}"
    s3_client.upload_fileobj(file, bucket_name, key)
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"
```

### Step 7: Deploy to Vercel

**Method 1: Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd "/path/to/Flask Website"
vercel

# For production
vercel --prod
```

**Method 2: GitHub Integration (Recommended)**

1. Push code to GitHub:
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

2. Go to https://vercel.com/
3. Click "Import Project"
4. Select your GitHub repository
5. Vercel auto-detects Python
6. Click "Deploy"

### Step 8: Configure Environment Variables

In Vercel dashboard:

1. Go to your project
2. Settings → Environment Variables
3. Add:

```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/dbname
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Step 9: Initialize Database

Since Vercel is serverless, initialize your external database locally:

```bash
# Set DATABASE_URL to your external database
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# Initialize database
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("Database initialized!")
EOF
```

### Step 10: Configure Custom Domain

In Vercel dashboard:
1. Settings → Domains
2. Add your domain (e.g., penasia.edu.hk)
3. Update DNS records at your domain provider:

```
Type    Name    Value
CNAME   @       cname.vercel-dns.com
CNAME   www     cname.vercel-dns.com
```

### Vercel-Specific Optimizations

**1. Reduce Cold Start Time**

Create `vercel.json` optimization:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.9"
      }
    }
  ],
  "functions": {
    "app.py": {
      "memory": 1024,
      "maxDuration": 10
    }
  }
}
```

**2. Cache Static Files**

Update `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

**3. Use Edge Functions for Fast Responses**

For simple API endpoints, use Vercel Edge Functions (faster):

Create `api/health.py`:

```python
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'healthy'}).encode())
```

### Troubleshooting Vercel Deployment

**Issue 1: "Module not found"**
```bash
# Make sure requirements.txt is in root
# Redeploy
vercel --prod
```

**Issue 2: "Function timeout"**
```json
// Increase timeout in vercel.json
{
  "functions": {
    "app.py": {
      "maxDuration": 10
    }
  }
}
```

**Issue 3: "Database connection failed"**
```python
# Use connection pooling
from sqlalchemy.pool import NullPool
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': NullPool
}
```

**Issue 4: "Static files not loading"**
```json
// Check vercel.json routes
{
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    }
  ]
}
```

### Vercel vs Other Options

| Feature | Vercel | Railway | PythonAnywhere | DigitalOcean |
|---------|--------|---------|----------------|--------------|
| **Setup Time** | 5 min | 5 min | 15 min | 30-60 min |
| **Free Tier** | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Database** | External | Included | SQLite | Full control |
| **Auto Deploy** | ✅ Yes | ✅ Yes | ❌ Manual | ❌ Manual |
| **Cold Starts** | Yes | No | No | No |
| **Scaling** | Automatic | Manual | Limited | Manual |
| **WebSockets** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | APIs | Full apps | Learning | Production |

### When to Use Vercel

✅ **Use Vercel if:**
- You have an external database (Neon, Supabase, PlanetScale)
- Your app is mostly API/JSON responses
- You want automatic GitHub deployments
- You need global CDN for static files
- Cold starts are acceptable

❌ **Don't use Vercel if:**
- You need persistent file storage
- You have long-running tasks
- You need WebSockets
- You want to use SQLite
- You need background workers

### Recommended: Hybrid Approach

**Best setup for Flask + Vercel:**

1. **Vercel**: Frontend (static files, API routes)
2. **Railway/DigitalOcean**: Flask app (main logic)
3. **Neon**: PostgreSQL database
4. **AWS S3**: File storage
5. **SendGrid**: Email service

This gives you the best of all worlds!

**For Railway:**
```bash
git push origin main
# Automatic deployment!
```

---

## 📊 Monitoring & Maintenance

### Set Up Monitoring

1. **Application Monitoring:**
   - Use Sentry: https://sentry.io/ (Free tier available)
   - Error tracking and performance monitoring

2. **Uptime Monitoring:**
   - Use UptimeRobot: https://uptimerobot.com/ (Free)
   - Sends alerts if site goes down

3. **Log Management:**
```bash
# View logs
tail -f /var/log/penasia/penasia.err.log
tail -f logs/gunicorn-access.log
```

### Regular Maintenance Tasks

**Weekly:**
- [ ] Check error logs
- [ ] Monitor disk space: `df -h`
- [ ] Check backup status

**Monthly:**
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review security advisories
- [ ] Database optimization
- [ ] Performance testing

---

## 🎯 Domain Setup

### Connect Custom Domain

1. **Purchase domain** (Namecheap, GoDaddy, etc.)

2. **Configure DNS Records:**
```
Type    Name    Value                   TTL
A       @       your_server_ip          300
A       www     your_server_ip          300
```

3. **For PythonAnywhere:**
   - Upgrade to paid account ($5/month)
   - Add domain in Web tab

4. **Wait for DNS propagation** (can take 24-48 hours)

---

## 💰 Cost Comparison

| Option | Monthly Cost | Best For | Database | Auto Deploy |
|--------|-------------|----------|----------|-------------|
| **PythonAnywhere Free** | $0 | Testing, learning | SQLite | ❌ Manual |
| **PythonAnywhere Hacker** | $5 | Small production | SQLite/MySQL | ❌ Manual |
| **DigitalOcean Droplet** | $6+ | Full control, scalable | PostgreSQL | ❌ Manual |
| **Railway Hobby** | $5 | Quick modern deploy | PostgreSQL | ✅ Auto |
| **Vercel Free** | $0 | APIs, serverless | External* | ✅ Auto |
| **Vercel Pro** | $20 | Production serverless | External* | ✅ Auto |
| **AWS Lightsail** | $3.50+ | AWS ecosystem | Full control | ❌ Manual |
| **Heroku Basic** | $7 | Classic PaaS | PostgreSQL | ✅ Auto |

_*Vercel requires external database (Neon/Supabase free tier available)_

### Total Cost Examples

**Budget Setup (Free):**
- Vercel Free + Neon Free + Vercel Blob Free = **$0/month**
- Limitations: 100GB bandwidth, 3GB database, serverless only

**Starter Setup ($5-6):**
- Railway $5 + Built-in PostgreSQL = **$5/month**
- OR PythonAnywhere Hacker $5 = **$5/month**
- OR DigitalOcean $6 + PostgreSQL = **$6/month**

**Production Setup ($15-25):**
- DigitalOcean $12 + Managed PostgreSQL $15 = **$27/month**
- OR Vercel Pro $20 + Neon $5 = **$25/month**

---

## 🚀 Quick Start Recommendations

### For Beginners:
1. Start with **PythonAnywhere Free** ($0)
2. Test everything works
3. Upgrade when ready ($5/month)

### For Modern Developers:
1. Use **Vercel Free** + **Neon Free** ($0)
2. Push to GitHub for auto-deploy
3. Great for APIs and serverless

### For Production:
1. Use **DigitalOcean** ($6/month)
2. PostgreSQL database
3. Nginx + Gunicorn
4. SSL certificate
5. Automated backups

### For Quick Production:
1. Use **Railway** ($5/month)
2. Push to GitHub
3. Auto-deploy on commit
4. Built-in PostgreSQL

---

## 🎯 My Recommendation for Your LMS

Based on your PenAsia LMS requirements:

### **Option 1: Best for Learning/Testing**
**PythonAnywhere Free → $5/month when ready**
- ✅ Easy setup (20 minutes)
- ✅ No credit card needed
- ✅ Perfect for demos
- ✅ Built-in database
- ❌ Manual updates
- ❌ Limited to SQLite on free tier

### **Option 2: Best Balance (My Top Pick)**
**Railway $5/month**
- ✅ Auto-deploy from GitHub
- ✅ Built-in PostgreSQL
- ✅ Easy scaling
- ✅ Modern developer experience
- ✅ Custom domains included
- ✅ Fast deployment (5 minutes)

### **Option 3: Best for Serverless/APIs**
**Vercel Free + Neon Free = $0**
- ✅ Completely free
- ✅ Global CDN
- ✅ Auto-deploy from GitHub
- ⚠️ Requires code modifications
- ⚠️ External database needed
- ⚠️ Cold starts (slower first request)
- ❌ Not ideal for full Flask apps

### **Option 4: Best for Production Control**
**DigitalOcean $6/month**
2. PostgreSQL database
3. Nginx + Gunicorn
4. SSL certificate
5. Automated backups

### For Modern/Quick:
1. Use **Railway** ($5/month)
2. Push to GitHub
3. Auto-deploy on commit
4. Built-in PostgreSQL

---

## 📝 Post-Deployment Testing

After deploying, test:

- [ ] Home page loads
- [ ] Login works (admin@penasia.edu.hk)
- [ ] Student registration works
- [ ] Application submission works
- [ ] Contact form works
- [ ] Admin dashboard accessible
- [ ] Static files load (CSS, images)
- [ ] Forms submit correctly
- [ ] Email notifications send
- [ ] Help system works
- [ ] Mobile responsive
- [ ] HTTPS enabled (if configured)

---

## 🆘 Troubleshooting

### Common Issues:

**500 Internal Server Error:**
```bash
# Check logs
tail -f /var/log/penasia/penasia.err.log
```

**Database Connection Failed:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql
# Test connection
psql -U penasiauser -d penasia_lms
```

**Static Files Not Loading:**
```nginx
# Check Nginx config
sudo nginx -t
# Verify static path in config
```

**Gunicorn Not Starting:**
```bash
# Check supervisor status
sudo supervisorctl status penasia
# Restart
sudo supervisorctl restart penasia
```

---

## 📚 Additional Resources

- **Flask Deployment:** https://flask.palletsprojects.com/en/2.3.x/deploying/
- **DigitalOcean Tutorials:** https://www.digitalocean.com/community/tutorials
- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Railway Docs:** https://docs.railway.app/
- **Let's Encrypt:** https://letsencrypt.org/

---

## ✅ Final Deployment Checklist

Before going live:

- [ ] All tests passing locally
- [ ] SECRET_KEY changed to strong random value
- [ ] DEBUG = False in production
- [ ] Database using PostgreSQL (not SQLite)
- [ ] Environment variables configured
- [ ] Email service working
- [ ] SSL certificate installed (HTTPS)
- [ ] Domain configured
- [ ] Backups automated
- [ ] Monitoring set up
- [ ] Error tracking enabled
- [ ] Admin account created
- [ ] Test data removed
- [ ] Documentation updated
- [ ] Load testing completed
- [ ] Security audit done

**🎉 You're ready to launch PenAsia LMS!**
