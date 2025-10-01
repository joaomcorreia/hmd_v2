from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.http import require_GET
import io
from django.core.cache import caches

# simple cache alias (use default cache)
_cache = cache

def ga_summary(request):
    key = "ga_summary_v1"
    data = cache.get(key)
    if not data:
        # STUB DATA — replace later with GA4 API result
        data = {
            "generated_at": timezone.now().isoformat(),
            "cards": [
                {"title": "Users (7d)", "value": 421},
                {"title": "Sessions (7d)", "value": 613},
                {"title": "Bounce Rate", "value": "47%"},
                {"title": "Top Page", "value": "/diensten/"},
            ],
        }
        cache.set(key, data, 120)  # 2 minutes for GA
    return JsonResponse(data)

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
