# Django Deployment on Hostinger VPS (CyberPanel + AlmaLinux 9)

## Overview
Your setup is ideal for Django:
- **CyberPanel**: Web-based control panel (makes deployment easier)
- **AlmaLinux 9**: Enterprise-grade Linux (Python 3.9+ pre-installed)
- **LiteSpeed Web Server**: Built into CyberPanel (faster than Apache)

## Step-by-Step Deployment

### 1. Access Your VPS
```bash
# SSH into your VPS
ssh root@your-vps-ip
# Or use CyberPanel terminal (browser-based)
```

### 2. Check Python Installation
```bash
python3 --version  # Should show Python 3.9+
pip3 --version     # Should be available
```

### 3. Create Website in CyberPanel

**Via CyberPanel Web Interface:**
1. Login to CyberPanel: `https://your-vps-ip:8090`
2. Go to **Websites → Create Website**
3. Domain: `test3.hmdklusbedrijf.nl`
4. Select your main domain or create new
5. Choose **Python** as the application type
6. Click **Create Website**

### 4. Upload Your Django Project

**Option A - Via CyberPanel File Manager:**
1. Go to **File Manager** in CyberPanel
2. Navigate to `/home/test3.hmdklusbedrijf.nl/public_html/`
3. Upload your `hmd_deployment.zip`
4. Extract it

**Option B - Via SSH/SFTP:**
```bash
cd /home/test3.hmdklusbedrijf.nl/public_html/
# Upload your zip file here, then:
unzip hmd_deployment.zip
mv hmd_deployment/* .  # Move files to root
rm -rf hmd_deployment  # Clean up
```

### 5. Set Up Python Environment

```bash
cd /home/test3.hmdklusbedrijf.nl/public_html/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Configure Environment Variables

**Create .env file:**
```bash
nano .env
```

**Add these contents:**
```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=&z@590t079)wa3nas6dsrlt$l+w@%1+jyu64nv(jny)k&u$nsm
ALLOWED_HOSTS=test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl
SECURE_SSL_REDIRECT=True
```

**Or export directly:**
```bash
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY="&z@590t079)wa3nas6dsrlt$l+w@%1+jyu64nv(jny)k&u$nsm"
export ALLOWED_HOSTS="test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl"
```

### 7. Django Setup Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Test Django (optional)
python manage.py runserver 0.0.0.0:8000
```

### 8. Configure CyberPanel for Django

**Via CyberPanel Interface:**
1. Go to **Websites → List Websites**
2. Click **Manage** for `test3.hmdklusbedrijf.nl`
3. Go to **Python → Setup Python App**
4. Set these values:
   - **App Directory**: `/home/test3.hmdklusbedrijf.nl/public_html`
   - **App URI**: `/` (root)
   - **Startup File**: `hmd/wsgi.py`
   - **Python Executable**: `/home/test3.hmdklusbedrijf.nl/public_html/venv/bin/python`
   - **App Type**: `wsgi`

### 9. Configure Static & Media Files

**In CyberPanel:**
1. Go to **Websites → Static Context**
2. Add these contexts:

**Static Files:**
- **URI**: `/static/`
- **Path**: `/home/test3.hmdklusbedrijf.nl/public_html/staticfiles/`
- **Accessible**: Yes

**Media Files:**
- **URI**: `/media/`
- **Path**: `/home/test3.hmdklusbedrijf.nl/public_html/media/`
- **Accessible**: Yes

### 10. Set File Permissions

```bash
cd /home/test3.hmdklusbedrijf.nl/public_html/
chown -R cyberpanel:cyberpanel .
chmod -R 755 .
chmod +x manage.py
```

### 11. SSL Certificate (Recommended)

**In CyberPanel:**
1. Go to **SSL → Manage SSL**
2. Select your domain: `test3.hmdklusbedrijf.nl`
3. Choose **Let's Encrypt** (free SSL)
4. Click **Issue SSL**

### 12. DNS Configuration

**Point your subdomain to VPS:**
1. In your domain DNS settings (where you registered the domain):
2. Add A record:
   - **Name**: `test3`
   - **Value**: `your-vps-ip-address`
   - **TTL**: 300 (or default)

## Testing Your Deployment

1. **Homepage**: `https://test3.hmdklusbedrijf.nl`
2. **Admin**: `https://test3.hmdklusbedrijf.nl/admin/`
3. **Check logs**: CyberPanel → Logs → Error Logs

## Troubleshooting

### Python App Not Starting:
```bash
# Check logs in CyberPanel → Logs
# Or manually:
tail -f /usr/local/lsws/Example/logs/error.log
```

### Permission Issues:
```bash
chown -R cyberpanel:cyberpanel /home/test3.hmdklusbedrijf.nl/public_html/
chmod 755 -R /home/test3.hmdklusbedrijf.nl/public_html/
```

### Static Files Not Loading:
- Verify static context in CyberPanel
- Check `python manage.py collectstatic`
- Ensure correct permissions

### Database Issues:
```bash
# SQLite permissions
chmod 664 db.sqlite3
chown cyberpanel:cyberpanel db.sqlite3
```

## Hostinger VPS Specific Tips

1. **CyberPanel Login**: `https://your-vps-ip:8090`
2. **Default SSH Port**: Usually 22 (check Hostinger panel)
3. **Firewall**: CyberPanel manages firewall automatically
4. **Backups**: Use CyberPanel backup features
5. **Resource Monitoring**: Available in CyberPanel dashboard

## Quick Commands Reference

```bash
# Restart LiteSpeed (if needed)
systemctl restart lsws

# Check Django process
ps aux | grep python

# View Django logs
tail -f /home/test3.hmdklusbedrijf.nl/public_html/logs/error.log

# Activate virtual environment
cd /home/test3.hmdklusbedrijf.nl/public_html/
source venv/bin/activate
```

## Advantages of Your Setup

✅ **CyberPanel**: Easy web interface for all configurations  
✅ **LiteSpeed**: Faster than Apache/Nginx  
✅ **AlmaLinux 9**: Stable, enterprise-grade OS  
✅ **Python 3.9+**: Already installed  
✅ **One-Click SSL**: Let's Encrypt integration  
✅ **File Manager**: No need for separate FTP client  

Your Django app will run beautifully on this setup! 🚀

## Next Steps

1. Upload your `hmd_deployment.zip` to CyberPanel
2. Follow steps 1-12 above
3. Your site will be live at `https://test3.hmdklusbedrijf.nl`

Need help with any specific step? Let me know!