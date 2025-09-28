from django.contrib import admin
from django.template.response import TemplateResponse
from django.template.loader import get_template
from django.http import Http404

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
    "all_settings": "All Settings",
    "cards-and-brochures": "Cards & Brochures",
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

    tpl = f"admin/tools/{slug}.html"
    get_template(tpl)  # validate template exists
    return TemplateResponse(request, tpl, ctx)
