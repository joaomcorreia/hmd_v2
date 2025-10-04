# core/admin.py
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.db import models
from .models import Slide, HomeAboutPanel, HomeValueBlock, HomeCarouselItem, AboutHero, AboutCarouselItem, AboutCompanyBlock, AboutProcessStep, AboutBenefit, PortfolioItem, SiteSettings, ContactSubmission, QuoteRequest

# Admin branding
admin.site.site_header = "HMD Klusbedrijf — Admin"
admin.site.site_title = "HMD Admin"
admin.site.index_title = "Beheer & overzicht"

# Hide Groups if unused
try:
    from django.contrib.auth.models import Group
    admin.site.unregister(Group)
except NotRegistered:
    pass

User = get_user_model()

# Unregister the default User admin so we can re-register
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    actions = ["send_password_setup"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)
        return qs

    def get_readonly_fields(self, request, obj=None):
        base = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return base + (
                "is_superuser",
                "is_staff",
                "user_permissions",
                "groups",
                "last_login",
                "date_joined",
            )
        return base

    def send_password_setup(self, request, queryset):
        sent = 0
        for user in queryset:
            if not user.email:
                continue
            form = PasswordResetForm({"email": user.email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name="registration/password_reset_email.html",
                    subject_template_name="registration/password_reset_subject.txt",
                )
                sent += 1
        self.message_user(request, f"{sent} uitnodiging(en) verzonden.")

    send_password_setup.short_description = "Stuur wachtwoord-aanmaaklink"

class PreviewReturnMixin:
    change_form_template = "admin/preview_change_form.html"

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        ctx = extra_context or {}
        preview_next = request.GET.get('next') or request.POST.get('_preview_next')
        if preview_next:
            ctx = {**ctx, 'preview_next': preview_next}
        return super().changeform_view(request, object_id, form_url, extra_context=ctx)

    def response_change(self, request, obj):
        preview_next = request.POST.get('_preview_next')
        if preview_next and '_save' in request.POST:
            return HttpResponseRedirect(preview_next)
        return super().response_change(request, obj)

# -------- Content models --------




@admin.register(AboutHero)
class AboutHeroAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("title",)

@admin.register(AboutCarouselItem)
class AboutCarouselItemAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("alt_text", "order")
    list_editable = ("order",)

@admin.register(AboutCompanyBlock)
class AboutCompanyBlockAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("heading",)

@admin.register(AboutBenefit)
class AboutBenefitAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)

@admin.register(AboutProcessStep)
class AboutProcessStepAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("step_title", "order", "heading")
    list_editable = ("order",)

@admin.register(HomeValueBlock)
class HomeValueBlockAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("title_emphasis",)

@admin.register(HomeCarouselItem)
class HomeCarouselItemAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("alt_text", "order")
    list_editable = ("order",)

@admin.register(HomeAboutPanel)
class HomeAboutPanelAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("title_emphasis",)

@admin.register(Slide)
class SlideAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("title", "subtitle")

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title",)
    list_editable = ("is_active",)

@admin.register(SiteSettings)
class SiteSettingsAdmin(PreviewReturnMixin, admin.ModelAdmin):
    list_display = ("contact_email",)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")
    readonly_fields = ("name", "email", "phone", "message")

# -------- Static “Tools” pages in Admin (no DB, full sidebar) --------
class AdminStaticPage(models.Model):
    class Meta:
        managed = False
        app_label = "tools"
        default_permissions = ()

class Overview(AdminStaticPage):
    class Meta:
        proxy = True
        verbose_name = "Overview"
        verbose_name_plural = "Overview"

class DomainName(AdminStaticPage):
    class Meta:
        proxy = True
        verbose_name = "Domain Name"
        verbose_name_plural = "Domain Name"

class Hosting(AdminStaticPage):
    class Meta:
        proxy = True
        verbose_name = "Hosting"
        verbose_name_plural = "Hosting"

class Website(AdminStaticPage):
    class Meta:
        proxy = True
        verbose_name = "Website"
        verbose_name_plural = "Website"

class SEO(AdminStaticPage):
    class Meta:
        proxy = True
        verbose_name = "SEO"
        verbose_name_plural = "SEO"

class SocialNetworks(AdminStaticPage):
    class Meta:
        proxy = True
        verbose_name = "Social Networks"
        verbose_name_plural = "Social Networks"

class StaticPageAdmin(admin.ModelAdmin):
    change_list_template = None  # set per subclass

    # disable CRUD
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

    def changelist_view(self, request, extra_context=None):
        ctx = self.admin_site.each_context(request)  # gives full admin sidebar
        if extra_context:
            ctx.update(extra_context)
        return TemplateResponse(request, self.change_list_template, ctx)

@admin.register(Overview)
class OverviewAdmin(StaticPageAdmin):
    change_list_template = "admin/tools/overview.html"

@admin.register(DomainName)
class DomainNameAdmin(StaticPageAdmin):
    change_list_template = "admin/tools/domain-name.html"

@admin.register(Hosting)
class HostingAdmin(StaticPageAdmin):
    change_list_template = "admin/tools/hosting.html"

@admin.register(Website)
class WebsiteAdmin(StaticPageAdmin):
    change_list_template = "admin/tools/website.html"

@admin.register(SEO)
class SEOAdmin(StaticPageAdmin):
    change_list_template = "admin/tools/seo.html"

@admin.register(SocialNetworks)
class SocialNetworksAdmin(StaticPageAdmin):
    change_list_template = "admin/tools/social-networks.html"


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    change_list_template = 'admin/core/quoterequest/change_list.html'
    change_form_template = 'admin/core/quoterequest/change_form.html'
    add_form_template = 'admin/core/quoterequest/change_form.html'
    
    list_display = ['name', 'phone', 'city', 'get_services_display', 'status', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'flexible_timing']
    search_fields = ['name', 'phone', 'address', 'city', 'description']
    readonly_fields = ['submitted_at', 'ip_address', 'user_agent', 'get_whatsapp_message']
    
    fieldsets = (
        ('Contactgegevens', {
            'fields': ('name', 'phone', 'address', 'city')
        }),
        ('Diensten & Planning', {
            'fields': ('services', 'preferred_date', 'flexible_timing', 'description')
        }),
        ('Status & Notities', {
            'fields': ('status', 'notes')
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('WhatsApp Bericht', {
            'fields': ('get_whatsapp_message',),
            'classes': ('collapse',)
        })
    )
    
    def get_services_display(self, obj):
        services_list = obj.get_services_list()
        return ', '.join(services_list) if services_list else 'Geen diensten geselecteerd'
    get_services_display.short_description = 'Diensten'
    
    def get_whatsapp_message(self, obj):
        return obj.get_whatsapp_message()
    get_whatsapp_message.short_description = 'WhatsApp Bericht'

