from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404

@staff_member_required
def admin_ai(request):
    # Placeholder. Later: call your MagicAI/OpenAI service.
    return render(request, "admin/tools/ai.html")

@staff_member_required
def admin_tool(request, slug):
    """
    Generic admin tool view that renders templates based on the slug.
    This allows the sidebar links to work properly.
    """
    # Define available tools and their templates
    tools = {
        'overview': 'admin/tools/overview.html',
        'home-preview': 'admin/tools/home-preview.html', 
        'domain-name': 'admin/tools/domain-name.html',
        'ai-assistant': 'ai_engine/assistant_dashboard.html',
        'hosting': 'admin/tools/hosting.html',
        'website': 'admin/tools/website.html',
        'seo': 'admin/tools/seo.html',
        'social-networks': 'admin/tools/social-networks.html',
        'ai': 'admin/tools/ai.html',
        'google': 'admin/tools/google.html',
        'qr-maker': 'admin/tools/qr-maker.html',
        'image-resizer': 'admin/tools/image-resizer.html',
        'stickers': 'admin/tools/stickers.html',
        'clothing': 'admin/tools/clothing.html',
        'prints-others': 'admin/tools/prints-others.html',
        'all_settings': 'admin/tools/all_settings.html',
    }
    
    if slug not in tools:
        raise Http404(f"Admin tool '{slug}' not found")
    
    # Handle Google Analytics dashboard
    if slug == 'google':
        from analytics.services import ga_service
        try:
            # Get filter parameters
            days = int(request.GET.get('days', 30))
            country_filter = request.GET.get('country', None)
            
            analytics_data = ga_service.get_overview_data(days=days, country_filter=country_filter)
        except Exception as e:
            analytics_data = {"error": str(e)}
        
        # Get real-time data for live user tracking
        try:
            realtime_data = ga_service.get_realtime_data()
        except Exception as e:
            realtime_data = {"error": str(e), "active_users": 0, "locations": [], "pages": [], "devices": []}
        
        context = {
            'tool_slug': slug,
            'sidebar_template': 'admin/sidebar.html',
            'analytics_data': analytics_data,
            'realtime_data': realtime_data,
            'current_days': days,
            'current_country': country_filter or 'all',
        }
        return render(request, tools[slug], context)
    
    # Handle settings form submissions for all_settings page
    if slug == 'all_settings' and request.method == 'POST':
        from core.models import SiteSettings
        from django.contrib import messages
        from django.shortcuts import redirect
        
        settings_obj, created = SiteSettings.objects.get_or_create(id=1)
        section = request.GET.get('section', '')
        
        if section == 'facebook':
            settings_obj.facebook_url = request.POST.get('facebook_url', '')
            messages.success(request, 'Facebook URL opgeslagen!')
        elif section == 'instagram':
            settings_obj.instagram_url = request.POST.get('instagram_url', '')
            messages.success(request, 'Instagram URL opgeslagen!')
        elif section == 'whatsapp':
            settings_obj.whatsapp_phone = request.POST.get('whatsapp_phone', '')
            messages.success(request, 'WhatsApp nummer opgeslagen!')
        elif section == 'phone_display':
            settings_obj.phone_display = request.POST.get('phone_display', '')
            messages.success(request, 'Telefoon weergave opgeslagen!')
        elif section == 'contact_email':
            settings_obj.contact_email_display = request.POST.get('contact_email_display', '')
            messages.success(request, 'Contact e-mail opgeslagen!')
        elif section == 'address':
            settings_obj.business_address = request.POST.get('business_address', '')
            messages.success(request, 'Bedrijfsadres opgeslagen!')
        elif section == 'kvk':
            settings_obj.kvk_number = request.POST.get('kvk_number', '')
            messages.success(request, 'KvK nummer opgeslagen!')
        
        settings_obj.save()
        return redirect('admin-tool', slug='all_settings')
    
    template_name = tools[slug]
    
    # Get SiteSettings for templates that need it
    from core.models import SiteSettings
    site_settings = SiteSettings.objects.first()
    
    context = {
        'tool_slug': slug,
        'sidebar_template': 'admin/sidebar.html',
        'SITE_SETTINGS': site_settings,
    }
    
    return render(request, template_name, context)


@staff_member_required
def realtime_analytics(request):
    """API endpoint for real-time analytics data"""
    from django.http import JsonResponse
    from analytics.services import ga_service
    
    try:
        realtime_data = ga_service.get_realtime_data()
        return JsonResponse({
            'success': True,
            'data': realtime_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': {
                'active_users': 0,
                'locations': [],
                'pages': [],
                'devices': [],
                'timestamp': None
            }
        })
