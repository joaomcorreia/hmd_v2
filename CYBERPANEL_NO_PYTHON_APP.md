# Django on CyberPanel (Without Python App Section)

## Alternative Deployment Methods

Your CyberPanel might not have the Python App section enabled, but Django deployment is still straightforward!

### Method 1: Manual WSGI Setup (Recommended)

#### Step 1: Create Website in CyberPanel
1. Login to CyberPanel: `https://your-vps-ip:8090`
2. **Websites → Create Website**
3. Domain: `test3.hmdklusbedrijf.nl`
4. Create as a regular website

#### Step 2: Upload Your Project
1. **File Manager** in CyberPanel
2. Navigate to `/home/test3.hmdklusbedrijf.nl/public_html/`
3. Upload and extract `hmd_deployment.zip`

#### Step 3: Install Python Dependencies
SSH into your server:
```bash
cd /home/test3.hmdklusbedrijf.nl/public_html/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 4: Create WSGI Configuration
Create file: `/home/test3.hmdklusbedrijf.nl/public_html/.htaccess`
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /wsgi_handler.py/$1 [QSA,L]
```

Create file: `/home/test3.hmdklusbedrijf.nl/public_html/wsgi_handler.py`
```python
#!/home/test3.hmdklusbedrijf.nl/public_html/venv/bin/python

import os
import sys
import django.core.handlers.wsgi

# Add project directory to Python path
project_dir = '/home/test3.hmdklusbedrijf.nl/public_html'
sys.path.insert(0, project_dir)

# Set environment variables
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_SECRET_KEY'] = '&z@590t079)wa3nas6dsrlt$l+w@%1+jyu64nv(jny)k&u$nsm'
os.environ['ALLOWED_HOSTS'] = 'test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl'
os.environ['DJANGO_SETTINGS_MODULE'] = 'hmd.settings'

# Initialize Django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()

# WSGI application
def wsgi_application(environ, start_response):
    return application(environ, start_response)

if __name__ == '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(wsgi_application)
```

#### Step 5: Set Permissions
```bash
chmod +x /home/test3.hmdklusbedrijf.nl/public_html/wsgi_handler.py
chown cyberpanel:cyberpanel -R /home/test3.hmdklusbedrijf.nl/public_html/
```

#### Step 6: Configure Static Files
In CyberPanel:
1. **Websites → List Websites**
2. Click **Manage** for your domain
3. **Rewrite Rules** → Add:
```apache
# Static files
RewriteRule ^static/(.*)$ /staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /media/$1 [L]
```

### Method 2: Using mod_wsgi (If Available)

Check if mod_wsgi is available:
```bash
python3 -c "import mod_wsgi; print('mod_wsgi available')"
```

If available, create `/home/test3.hmdklusbedrijf.nl/public_html/django.wsgi`:
```python
import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add your project directory to sys.path
sys.path.insert(0, '/home/test3.hmdklusbedrijf.nl/public_html')

# Set environment variables
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_SECRET_KEY'] = '&z@590t079)wa3nas6dsrlt$l+w@%1+jyu64nv(jny)k&u$nsm'
os.environ['ALLOWED_HOSTS'] = 'test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmd.settings')

django.setup()
application = get_wsgi_application()
```

### Method 3: Subdirectory Installation

If the above methods don't work, install in a subdirectory:

#### Step 1: Create Subdirectory
```bash
mkdir /home/test3.hmdklusbedrijf.nl/public_html/app
cd /home/test3.hmdklusbedrijf.nl/public_html/app
# Upload your Django project here
```

#### Step 2: Create Index Redirect
Create `/home/test3.hmdklusbedrijf.nl/public_html/index.php`:
```php
<?php
header("Location: /app/");
exit();
?>
```

#### Step 3: Configure Django in Subfolder
Follow the same WSGI setup but in the `/app/` directory.

### Method 4: Enable Python Support in CyberPanel

Some CyberPanel installations need Python enabled:

#### Via SSH:
```bash
# Install Python LSAPI
cd /usr/src
wget https://www.litespeedtech.com/packages/lsapi/python-lsapi-1.7.tgz
tar xzf python-lsapi-1.7.tgz
cd python-lsapi-1.7
python3 ./configure.py
make
sudo make install
```

#### Enable in LiteSpeed:
1. Login to LiteSpeed WebAdmin: `https://your-vps-ip:7080`
2. **Actions → Graceful Restart**
3. **Script Handler** → Add:
   - **Suffixes**: `py`
   - **Type**: `LiteSpeed SAPI`
   - **Command**: `lspython`

### Method 5: Contact Hostinger Support

If none of the above work, contact Hostinger support and ask them to:
1. Enable Python/Django support
2. Install mod_wsgi
3. Enable Python App section in CyberPanel

## Quick Deployment Steps (Method 1)

1. **Create website** in CyberPanel for `test3.hmdklusbedrijf.nl`
2. **Upload files** via File Manager
3. **SSH setup**:
   ```bash
   cd /home/test3.hmdklusbedrijf.nl/public_html/
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic
   ```
4. **Create the WSGI files** (copy from above)
5. **Set permissions**
6. **Test**: Visit `https://test3.hmdklusbedrijf.nl`

## Troubleshooting

### Internal Server Error:
- Check error logs in CyberPanel
- Verify Python path in WSGI file
- Check file permissions

### Python Not Found:
```bash
which python3  # Find Python path
# Update wsgi_handler.py shebang line
```

### Static Files Not Loading:
- Run `python manage.py collectstatic`
- Check rewrite rules
- Verify static file paths

## Testing Your Setup

After deployment, test these URLs:
- **Homepage**: `https://test3.hmdklusbedrijf.nl`
- **Admin**: `https://test3.hmdklusbedrijf.nl/admin/`
- **Static file**: `https://test3.hmdklusbedrijf.nl/static/css/main.css`

Your Django app will work perfectly even without the Python App section! 🚀

Which method would you like to try first?