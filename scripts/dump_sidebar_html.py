from django.conf import settings
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
c=Client()
User=get_user_model()
u=User.objects.filter(is_superuser=True).first()
c.force_login(u)
r=c.get('/admin/core/homecarouselitem/')
s=r.content.decode('utf-8')
i=s.find('class="admin-sidebar"')
print('INDEX:'+str(i))
start=max(0,i-400)
end=i+800
print(s[start:end])
