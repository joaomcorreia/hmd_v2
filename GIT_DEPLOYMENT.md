# Django Deployment via Git in CyberPanel

## Git Deployment (Recommended Method)

CyberPanel's Git feature can deploy directly from your GitHub repository - this is actually the modern, preferred way!

### Step 1: Prepare Your Repository

First, let's make sure your GitHub repo is deployment-ready:

#### A. Add Environment Variables Support
Your project already supports environment variables perfectly!

#### B. Create Production Requirements (Optional)
If you want to separate dev/prod dependencies, create `requirements-prod.txt`:
```
Django>=4.2,<5.0
# Add only production dependencies here
```

#### C. Add Deployment Scripts
Create `deploy.sh` in your repo root:
```bash
#!/bin/bash
echo "Starting Django deployment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Set environment variables (will be overridden by CyberPanel)
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY:-fallback-key}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS:-test3.hmdklusbedrijf.nl}"

# Run Django management commands
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Set permissions
chmod +x manage.py
chmod -R 755 staticfiles/
chmod -R 755 media/

echo "Django deployment completed!"
```

### Step 2: Push Changes to GitHub

```bash
# In your local project directory
git add .
git commit -m "Prepare for CyberPanel Git deployment"
git push origin main
```

### Step 3: Configure Git Deployment in CyberPanel

#### A. Create Website
1. Login to CyberPanel: `https://your-vps-ip:8090`
2. **Websites → Create Website**
3. Domain: `test3.hmdklusbedrijf.nl`

#### B. Set Up Git Deployment
1. **Websites → List Websites**
2. Click **Manage** for `test3.hmdklusbedrijf.nl`
3. Look for **Git** section (might be under Website Management)
4. Configure:
   - **Repository URL**: `https://github.com/joaomcorreia/hmd.git`
   - **Branch**: `main`
   - **Deploy Path**: `/home/test3.hmdklusbedrijf.nl/public_html/`
   - **Build Command**: `bash deploy.sh` (if you created the script)

#### C. Set Environment Variables
In CyberPanel Git settings or via SSH:
1. **Environment Variables** section (if available in CyberPanel)
2. Or create `.env` file via File Manager:
```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=&z@590t079)wa3nas6dsrlt$l+w@%1+jyu64nv(jny)k&u$nsm
ALLOWED_HOSTS=test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl
```

### Step 4: Deploy

1. In CyberPanel Git section, click **Deploy** or **Pull from Git**
2. CyberPanel will:
   - Clone your repository
   - Run deployment scripts
   - Set up the website

### Step 5: Configure Django for Production

#### A. Create WSGI Configuration
Via SSH or File Manager, create `/home/test3.hmdklusbedrijf.nl/public_html/.htaccess`:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !^/(static|media)/
RewriteRule ^(.*)$ /wsgi.py/$1 [QSA,L]
```

Create `/home/test3.hmdklusbedrijf.nl/public_html/wsgi.py`:
```python
#!/home/test3.hmdklusbedrijf.nl/public_html/venv/bin/python3

import os
import sys
from pathlib import Path

# Add project to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env if it exists
env_file = project_root / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmd.settings')

# Initialize Django
import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# CGI Handler
if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
```

#### B. Set Permissions
```bash
chmod +x /home/test3.hmdklusbedrijf.nl/public_html/wsgi.py
chown -R cyberpanel:cyberpanel /home/test3.hmdklusbedrijf.nl/public_html/
```

### Step 6: Configure Static Files

In CyberPanel:
1. **Websites → List Websites → Manage**
2. **Rewrite Rules** → Add:
```apache
# Serve static files directly
RewriteRule ^static/(.*)$ /staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /media/$1 [L]
```

## Alternative: GitHub Actions Auto-Deploy

You can also set up automatic deployment when you push to GitHub:

### Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Hostinger VPS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        password: ${{ secrets.PASSWORD }}
        script: |
          cd /home/test3.hmdklusbedrijf.nl/public_html/
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          python manage.py migrate --noinput
          python manage.py collectstatic --noinput
```

## Advantages of Git Deployment

✅ **Automatic Updates**: Just `git push` to deploy  
✅ **Version Control**: Easy rollbacks  
✅ **Consistent Environment**: Same code everywhere  
✅ **Modern Workflow**: Industry standard  
✅ **Easy Collaboration**: Team members can deploy  

## Testing Your Deployment

After Git deployment:
1. **Homepage**: `https://test3.hmdklusbedrijf.nl`
2. **Admin**: `https://test3.hmdklusbedrijf.nl/admin/`
3. **Check logs**: CyberPanel → Logs

## Troubleshooting Git Deployment

### Repository Access Issues:
- Make sure repo is public, or add SSH keys for private repos
- Check GitHub repository URL is correct

### Build Failures:
- Check deployment logs in CyberPanel
- Ensure `deploy.sh` has correct permissions
- Verify Python/pip paths

### Django Not Loading:
- Check WSGI configuration
- Verify environment variables
- Check file permissions

This Git-based deployment is actually better than traditional file upload - you get automatic deployments and version control! 🚀

Would you like me to help you set up the Git deployment, or do you prefer the simple file upload method?