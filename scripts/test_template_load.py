import os
import sys
import django
from django.template import TemplateSyntaxError

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmd.settings')
django.setup()

from django.template.loader import get_template

candidates = [
    'admin/sidebar_ai.html',
    'admin/sidebar.html',
]

for tpl in candidates:
    try:
        t = get_template(tpl)
        print(f"Loaded template {tpl} OK")
    except TemplateSyntaxError as e:
        print(f"TemplateSyntaxError while loading {tpl}: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"Other error loading {tpl}: {e}")
        import traceback
        traceback.print_exc()
