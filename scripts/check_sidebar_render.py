import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hmd.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
c=Client()
User=get_user_model()
u=User.objects.filter(is_superuser=True).first()
if not u:
    print('NO_SUPERUSER')
else:
    c.force_login(u)
    r=c.get('/admin/core/homecarouselitem/')
    s=r.content.decode('utf-8')
    print('STATUS', r.status_code)
    print('HAS_CSS', 'admin_sidebar.css' in s)
    nav_idx = s.find('<nav id="nav-sidebar"')
    print('NAV_IDX', nav_idx)
    if nav_idx!=-1:
        snippet = s[nav_idx:nav_idx+800]
        print(snippet)
