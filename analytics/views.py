from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import io
from django.core.cache import caches
from .services import ga_service

# simple cache alias (use default cache)
_cache = cache

def ga_summary(request):
    """API endpoint for Google Analytics summary data"""
    try:
        data = ga_service.get_overview_data(days=30)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@staff_member_required
def analytics_dashboard(request):
    """Main analytics dashboard view"""
    try:
        analytics_data = ga_service.get_overview_data(days=30)
    except Exception as e:
        analytics_data = {"error": str(e)}
    
    context = {
        'analytics_data': analytics_data,
        'sidebar_template': 'admin/sidebar.html',
    }
    return render(request, 'admin/tools/google.html', context)

def fb_summary(request):
    key = "fb_summary_v1"
    data = cache.get(key)
    if not data:
        # STUB DATA — replace later with Graph API result
        data = {
            "generated_at": timezone.now().isoformat(),
            "cards": [
                {"title": "Page Likes (28d)", "value": 37},
                {"title": "Post Reach (7d)", "value": 1803},
                {"title": "Messages (7d)", "value": 12},
                {"title": "Best Post", "value": "Keuken renovatie"},
            ],
        }
        cache.set(key, data, 900)  # 15 minutes for FB
    return JsonResponse(data)


@require_GET
def qr_image(request):
    """Return a PNG QR image for ?text=...&size=... .
    Falls back with 501 if server-side libs are not installed.
    """
    text = request.GET.get('text', '')
    try:
        size = int(request.GET.get('size', 220))
    except Exception:
        size = 220

    # try to import qrcode & Pillow; if missing, return 501 so client can fallback
    try:
        import qrcode
        from PIL import Image
    except Exception:
        return HttpResponse('Server-side QR generation not available', status=501)

    key = f"qr:{text}:{size}"
    data = _cache.get(key)
    if data:
        return HttpResponse(data, content_type='image/png')

    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # resize to requested size
    img = img.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    png = buf.getvalue()
    _cache.set(key, png, 60 * 10)
    return HttpResponse(png, content_type='image/png')
