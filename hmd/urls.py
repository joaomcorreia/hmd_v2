from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core
from . import admin_preview
from hmd.admin_extra import admin_tool
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/preview/<str:app_label>/<str:model_name>/<int:pk>/", admin.site.admin_view(admin_preview.preview_edit), name="admin-preview-edit"),

    path("admin/tools/<slug:slug>/", admin.site.admin_view(admin_tool), name="admin-tool"),
    # include analytics API endpoints before the admin site so /admin/api/ routes resolve
    path("admin/api/", include("analytics.urls")),
    path("admin/", admin.site.urls),

    # Admin password reset alias so the admin login page can show a working "Forgotten your login credentials?" link
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_set_email.txt",
        subject_template_name="registration/password_set_subject.txt",
        success_url=reverse_lazy("password_reset_done"),
    ), name="admin_password_reset"),
    path("admin/password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ), name="admin_password_reset_done"),

    # public site
    path("", core.index, name="index"),
    path("over-ons/", core.over_ons, name="over-ons"),
    path("diensten/", core.diensten, name="diensten"),
    path("portfolio/", core.portfolio, name="portfolio"),
    path("contact/", core.contact, name="contact"),
    path("diensten/<slug:slug>/", core.service_detail, name="service-detail"),
    path("api/quote-request/", core.submit_quote_request, name="submit-quote-request"),

    # auth
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_set_email.txt",
        subject_template_name="registration/password_set_subject.txt",
        success_url=reverse_lazy("password_reset_done"),
    ), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete"),
    ), name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name="password_reset_complete"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ai/", include("ai_engine.urls")),
    # analytics API endpoints (GA / FB summaries)
    path("admin/api/", include("analytics.urls")),
    # removed erroneous include("HMD.urls") — public routes are defined above
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
