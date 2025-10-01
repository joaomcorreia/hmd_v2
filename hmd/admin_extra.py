from django.contrib import admin
from django.template.response import TemplateResponse
from django.template.loader import get_template
from django.http import Http404
from django.template.exceptions import TemplateDoesNotExist
from django.urls import path

TOOLS = {
    "home-preview": "Homepage Preview",
    "over-ons-preview": "Over Ons Preview",
    "overview": "Overview",
    "domain-name": "Domain Name",
    "hosting": "Hosting",
    "website": "Website",
    "google": "Google Tools",
    "seo": "SEO",
    "social-networks": "Social Networks",
    "facebook": "Facebook",
    "all_settings": "All Settings",
    "cards-and-brochures": "Cards & Brochures",
    "ai": "AI Tool", 
    # Prints section
    "cards": "Cards",
    "trifold": "Trifold / Quafold",
    "tags": "Tags",
    "stickers": "Stickers",
    "clothing": "Clothing",
    "prints-others": "Other Prints",
    # User tools
    "profile": "Profile",
    "users": "Users",
    # Free tools
    "qr-maker": "QR Code Maker",
    "image-resizer": "Image Resizer",
}

def admin_tool(request, slug: str):
    if slug not in TOOLS:
        raise Http404("Tool not found")

    ctx = admin.site.each_context(request)
    ctx["title"] = TOOLS[slug]
    ctx["tool_slug"] = slug

    # enable the full admin sidebar on tool pages
    ctx["available_apps"] = admin.site.get_app_list(request)
    ctx["nav_sidebar"] = True

    # allow per-tool sidebar overrides: prefer admin/sidebar_<slug>.html if it exists
    sidebar_candidate = f"admin/sidebar_{slug}.html"
    try:
        get_template(sidebar_candidate)
        ctx["sidebar_template"] = sidebar_candidate
    except TemplateDoesNotExist:
        ctx["sidebar_template"] = "admin/sidebar.html"

    # optional extra menu fragment: admin/sidebar_menu_<slug>.html
    menu_candidate = f"admin/sidebar_menu_{slug}.html"
    try:
        get_template(menu_candidate)
        ctx["menu_override"] = menu_candidate
    except TemplateDoesNotExist:
        ctx["menu_override"] = None

    tpl = f"admin/tools/{slug}.html"
    get_template(tpl)  # validate template exists
    return TemplateResponse(request, tpl, ctx)
