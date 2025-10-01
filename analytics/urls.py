from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .views import ga_summary, fb_summary, qr_image

# these are relative paths; included at project level under admin/api/
urlpatterns = [
    path("ga/summary/", staff_member_required(ga_summary), name="ga_summary"),
    path("fb/summary/", staff_member_required(fb_summary), name="fb_summary"),
    path("qr/", staff_member_required(qr_image), name="qr_image"),
]
