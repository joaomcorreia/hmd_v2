DIENSTEN = [
    "Schilderwerk", "Elektra", "Tegelwerk", "Stucwerk",
    "Badkamer renovatie", "Keuken montage", "Vloeren", "Dakwerk",
]

from .models import SiteSettings

def site_constants(request):
    settings_obj = SiteSettings.objects.first()
    return {
        "DIENSTEN": DIENSTEN,
        "SITE_SETTINGS": settings_obj,
        "SITE_SETTINGS_WA_URL": settings_obj.whatsapp_url if settings_obj else "https://wa.me/31687111289",
        "SITE_SETTINGS_WA_DIGITS": settings_obj.whatsapp_digits if settings_obj else "31687111289",
        "SITE_SETTINGS_PHONE_DISPLAY": settings_obj.phone_display if settings_obj and settings_obj.phone_display else "06 87111289",
        "SITE_SETTINGS_EMAIL": settings_obj.contact_email if settings_obj and settings_obj.contact_email else "info@hmdklusbedrijf.nl",
        "SITE_SETTINGS_WHATSAPP_E164": settings_obj.whatsapp if settings_obj and settings_obj.whatsapp else "+31687111289",
    }

from .constants import SERVICES_TICKER
def diensten_ticker(request):
    return {"diensten": SERVICES_TICKER}