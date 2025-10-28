# Production Deployment Configuration
# PenAsia Continuing Education Centre Website

## Server Requirements
- Python 3.8+
- PostgreSQL 12+ (or MySQL 8+)
- Nginx or Apache
- Gunicorn (WSGI server)
- SSL Certificate (Let's Encrypt)
- Minimum 2GB RAM
- 20GB Storage

## Environment Variables (.env)
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/penasia_db
# or for MySQL:
# DATABASE_URL=mysql://username:password@localhost:3306/penasia_db

# Email Configuration (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password

# Application Settings
MAX_CONTENT_LENGTH=16777216  # 16MB max file upload
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Admin Email (for error notifications)
ADMIN_EMAIL=admin@penasia.edu.hk

# WhatsApp Contact
WHATSAPP_NUMBER=85228936788
```

## Gunicorn Configuration (gunicorn_config.py)
```python
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '/var/log/penasia/access.log'
errorlog = '/var/log/penasia/error.log'
loglevel = 'info'

# Process naming
proc_name = 'penasia_web'

# Server mechanics
daemon = False
pidfile = '/var/run/penasia/gunicorn.pid'
user = 'www-data'
group = 'www-data'
umask = 0o007

# SSL (if terminating at Gunicorn instead of Nginx)
# keyfile = '/etc/ssl/private/penasia.key'
# certfile = '/etc/ssl/certs/penasia.crt'
```

## Nginx Configuration (/etc/nginx/sites-available/penasia)
```nginx
upstream penasia_server {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name penasia.edu.hk www.penasia.edu.hk;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name penasia.edu.hk www.penasia.edu.hk;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/penasia.edu.hk/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/penasia.edu.hk/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Max upload size
    client_max_body_size 16M;
    
    # Root directory
    root /var/www/penasia/;
    
    # Access and error logs
    access_log /var/log/nginx/penasia_access.log;
    error_log /var/log/nginx/penasia_error.log;
    
    # Static files
    location /static {
        alias /var/www/penasia/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
        
        # Compress static assets
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/css text/javascript application/javascript application/json image/svg+xml;
    }
    
    # Media files (user uploads)
    location /media {
        alias /var/www/penasia/media;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Favicon
    location = /favicon.ico {
        alias /var/www/penasia/static/images/favicon.ico;
        access_log off;
        log_not_found off;
    }
    
    # Robots.txt
    location = /robots.txt {
        alias /var/www/penasia/static/robots.txt;
        access_log off;
        log_not_found off;
    }
    
    # Main application
    location / {
        proxy_pass http://penasia_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Systemd Service (/etc/systemd/system/penasia.service)
```ini
[Unit]
Description=PenAsia Education Website
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=penasia
WorkingDirectory=/var/www/penasia
Environment="PATH=/var/www/penasia/venv/bin"
ExecStart=/var/www/penasia/venv/bin/gunicorn -c /var/www/penasia/gunicorn_config.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always

[Install]
WantedBy=multi-user.target
```

## Deployment Steps

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib supervisor

# Create application user
sudo useradd -m -s /bin/bash penasia
```

### 2. Application Setup
```bash
# Create application directory
sudo mkdir -p /var/www/penasia
sudo chown penasia:penasia /var/www/penasia

# Switch to application user
sudo su - penasia

# Clone/upload your application
cd /var/www/penasia
# (upload your files here)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Create .env file
nano .env
# (add your environment variables)
```

### 3. Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE penasia_db;
CREATE USER penasia_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE penasia_db TO penasia_user;
\q

# Initialize database
source venv/bin/activate
flask db upgrade
python create_sample_data.py  # Optional: create sample data
```

### 4. Static Files
```bash
# Ensure proper permissions
sudo chown -R www-data:www-data /var/www/penasia/static
sudo chmod -R 755 /var/www/penasia/static

# Create media directory for uploads
sudo mkdir -p /var/www/penasia/media
sudo chown -R www-data:www-data /var/www/penasia/media
```

### 5. Nginx Configuration
```bash
# Copy nginx config
sudo cp nginx_config /etc/nginx/sites-available/penasia

# Enable site
sudo ln -s /etc/nginx/sites-available/penasia /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d penasia.edu.hk -d www.penasia.edu.hk

# Auto-renewal is configured automatically
```

### 7. Start Application
```bash
# Copy systemd service
sudo cp penasia.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable penasia
sudo systemctl start penasia

# Check status
sudo systemctl status penasia
```

### 8. Logging Setup
```bash
# Create log directory
sudo mkdir -p /var/log/penasia
sudo chown www-data:www-data /var/log/penasia

# Configure logrotate
sudo nano /etc/logrotate.d/penasia
```

Add:
```
/var/log/penasia/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload penasia > /dev/null 2>&1 || true
    endscript
}
```

## Monitoring & Maintenance

### Check Application Status
```bash
# Service status
sudo systemctl status penasia

# View logs
sudo tail -f /var/log/penasia/error.log
sudo tail -f /var/log/penasia/access.log

# Restart application
sudo systemctl restart penasia
```

### Database Backup
```bash
# Manual backup
pg_dump -U penasia_user penasia_db > backup_$(date +%Y%m%d).sql

# Automated backup (add to crontab)
0 2 * * * /usr/bin/pg_dump -U penasia_user penasia_db | gzip > /backups/penasia_$(date +\%Y\%m\%d).sql.gz
```

### Performance Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor processes
htop

# Monitor database
sudo -u postgres psql penasia_db
SELECT * FROM pg_stat_activity;
```

## Troubleshooting

### Application won't start
```bash
# Check service logs
sudo journalctl -u penasia -n 50

# Check gunicorn logs
sudo tail -50 /var/log/penasia/error.log

# Verify Python environment
source /var/www/penasia/venv/bin/activate
which python
python --version
```

### 502 Bad Gateway
- Check if Gunicorn is running: `sudo systemctl status penasia`
- Check Nginx error log: `sudo tail -50 /var/log/nginx/penasia_error.log`
- Verify socket/port connectivity

### Static files not loading
- Check file permissions: `ls -la /var/www/penasia/static`
- Verify Nginx configuration: `sudo nginx -t`
- Check Nginx error log

### Database connection errors
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check DATABASE_URL in .env
- Test connection: `psql -U penasia_user -d penasia_db`

## Security Checklist

- [x] DEBUG=False in production
- [x] Strong SECRET_KEY generated
- [x] Database credentials secured
- [x] SSL/TLS enabled (HTTPS)
- [x] Security headers configured
- [x] File upload limits set
- [x] CSRF protection enabled (Flask-WTF)
- [x] SQL injection protection (SQLAlchemy)
- [x] XSS protection enabled
- [ ] Regular security updates scheduled
- [ ] Firewall configured (UFW)
- [ ] Fail2ban configured
- [ ] Regular backups automated

## Performance Optimization

- [x] Gzip compression enabled
- [x] Static file caching (30 days)
- [x] Database connection pooling
- [ ] Redis for session storage (optional)
- [ ] CDN for static assets (optional)
- [ ] Image optimization/compression
- [ ] Database query optimization
- [ ] HTTP/2 enabled

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (HAProxy, AWS ELB)
- Shared session storage (Redis/Memcached)
- Distributed file storage (S3, NFS)

### Vertical Scaling
- Increase worker processes
- Add more RAM
- Upgrade CPU

### Database Scaling
- Read replicas for queries
- Connection pooling (PgBouncer)
- Database sharding (if needed)

---

**Last Updated**: January 2025  
**Version**: 1.0 - Production Ready
