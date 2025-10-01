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
    print('No superuser found')
else:
    c.force_login(u)
    r=c.get('/admin/core/homecarouselitem/')
    s=r.content.decode('utf-8')
    i=s.find('<nav id="nav-sidebar"')
    print('NAV_IDX',i)
    print(s[i:i+1200])
