# HMD Project Deployment Guide

## Overview
This guide covers deploying the HMD project to both a subdomain for testing and the main domain for production.

## Environment Setup

### 1. Development Environment (Local)
```bash
# Clone the repository
git clone <repository-url>
cd hmd

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 2. Staging Environment (Subdomain)
Deploy to `test3.hmdklusbedrijf.nl` or similar subdomain for testing.

### 3. Production Environment (Main Domain)
Deploy to `hmdklusbedrijf.nl` after testing is complete.

## Environment Variables

Copy `.env.example` and configure for your environment:

### For Development (Optional .env file):
```bash
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### For Staging:
```bash
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-staging-secret-key
ALLOWED_HOSTS=test3.hmdklusbedrijf.nl
SECURE_SSL_REDIRECT=False  # if no SSL yet
```

### For Production:
```bash
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=hmdklusbedrijf.nl,www.hmdklusbedrijf.nl
SECURE_SSL_REDIRECT=True
```

## Deployment Steps

### Step 1: Prepare for Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Check deployment readiness
python manage.py check --deploy
```

### Step 2: Deploy to Staging
1. Upload code to staging server
2. Set environment variables in hosting control panel
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Collect static files: `python manage.py collectstatic --noinput`
6. Test functionality thoroughly

### Step 3: Deploy to Production
1. After staging tests pass, deploy to main domain
2. Update environment variables for production
3. Repeat deployment steps
4. Update DNS if needed

## Server Configuration

### WSGI Configuration (for Apache/Nginx)
```python
# wsgi.py is already configured
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmd.settings')
application = get_wsgi_application()
```

### Static Files
- Static files are collected to `staticfiles/` directory
- Media files are stored in `media/` directory
- Configure your web server to serve these directly

### Database
- Development: SQLite (included)
- Production: Can use PostgreSQL/MySQL by updating DATABASES in settings.py

## Security Checklist

- [x] DEBUG=False in production
- [x] Strong SECRET_KEY in production
- [x] ALLOWED_HOSTS properly configured
- [x] HTTPS/SSL enabled (SECURE_SSL_REDIRECT=True)
- [x] Security headers enabled
- [x] Email configuration for notifications

## Monitoring & Maintenance

### Logs
Check Django logs and web server logs for any issues.

### Backups
- Database: Regular SQLite backups or use managed database service
- Media files: Backup the `media/` directory
- Code: Version controlled in Git

### Updates
1. Test updates in staging first
2. Always backup before deploying updates
3. Run migrations after code updates
4. Collect static files if CSS/JS changed

## Troubleshooting

### Common Issues:
- **500 Errors**: Check DEBUG=False and SECRET_KEY is set
- **Static files not loading**: Run `collectstatic` and configure web server
- **Admin not accessible**: Check ALLOWED_HOSTS includes your domain
- **SSL issues**: Verify SECURE_SSL_REDIRECT setting matches your SSL setup

### Quick Commands:
```bash
# Check if everything is working
python manage.py check

# Check deployment readiness
python manage.py check --deploy

# Show current settings
python manage.py shell -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)"
```

## Support

For deployment issues, check:
1. Server error logs
2. Django debug information (if DEBUG=True in staging)
3. Network connectivity and DNS settings
4. SSL certificate validity

---

## Environment-Specific Notes

The project is configured to work seamlessly across environments:
- **Settings**: Automatically adapt based on environment variables
- **Static files**: Collected appropriately for each environment
- **Security**: Production security features auto-enable when DEBUG=False
- **Templates**: Admin sidebar and all templates work consistently

This setup allows you to:
1. Develop locally with minimal setup
2. Test on subdomain with production-like settings
3. Deploy to main domain with full security
4. Continue development while production runs