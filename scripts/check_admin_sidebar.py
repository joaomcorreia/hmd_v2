import os
import sys
import django

# ensure project root is on sys.path so 'hmd' settings can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmd.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

u = User.objects.filter(is_superuser=True).first()
print('superuser:', bool(u))

c = Client()
if u:
    c.force_login(u)

resp = c.get('/admin/tools/ai/')
print('/admin/tools/ai/ status', resp.status_code)
content = resp.content.decode()
print('has sidebar?', 'admin-sidebar' in content)
print('has admin_main_styles.css?', 'admin_main_styles.css' in content)

resp2 = c.get('/admin/core/homecarouselitem/')
print('/admin/core/homecarouselitem/ status', resp2.status_code)
content2 = resp2.content.decode()
print('has sidebar?', 'admin-sidebar' in content2)
print('has admin_main_styles.css?', 'admin_main_styles.css' in content2)
