# Deployment to test3.hmdklusbedrijf.nl

## Quick Deployment Steps

### 1. Environment Variables Setup
Set these environment variables on your server:

```bash
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY="your-production-secret-key-here"
export ALLOWED_HOSTS="test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl"
export SECURE_SSL_REDIRECT=True
```

### 2. Deploy Files
Upload/sync your project files to the server.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

### 6. Web Server Configuration
Configure your web server (Apache/Nginx) to:
- Point to your Django project
- Serve static files from `/static/` → `staticfiles/`
- Serve media files from `/media/` → `media/`
- Forward all other requests to Django (WSGI/ASGI)

### 7. Test the Deployment
- Visit: https://test3.hmdklusbedrijf.nl
- Admin: https://test3.hmdklusbedrijf.nl/admin/

## Environment Variables Reference

| Variable | Development | Production |
|----------|-------------|------------|
| `DJANGO_DEBUG` | `True` (default) | `False` |
| `DJANGO_SECRET_KEY` | Auto-generated | **Required** |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost,testserver` | `test3.hmdklusbedrijf.nl,hmdklusbedrijf.nl` |
| `SECURE_SSL_REDIRECT` | `False` (default) | `True` |

## Notes
- Your project is already configured for production with proper security settings
- SSL/HTTPS security features activate automatically when `DEBUG=False`
- Static and media files are properly configured
- Database uses SQLite by default (consider PostgreSQL for production)