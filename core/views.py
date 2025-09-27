# core/views.py
from django.conf import settings as dj_settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.urls import reverse

from .forms import ContactForm
from .models import (
    Slide,
    HomeAboutPanel,
    HomeValueBlock,
    HomeCarouselItem,
    AboutHero,
    AboutCarouselItem,
    AboutCompanyBlock,
    AboutProcessStep,
    PortfolioItem,
    SiteSettings,
    ContactSubmission,
)


# -------- helpers --------
def _abs_static(request, path: str) -> str:
    return request.build_absolute_uri(static(path))

def _contact_to_email() -> str:
    s = SiteSettings.objects.first()
    return s.contact_email if s and s.contact_email else "justcodeworks@gmail.com"


# -------- pages --------
def index(request):
    slides = Slide.objects.filter(is_active=True)
    carousel_items = HomeCarouselItem.objects.all()
    value_block = HomeValueBlock.objects.first()
    about_panel = HomeAboutPanel.objects.first()
    about_url = reverse("over-ons")
    meta = {
        "title": "Home | HMD Klusbedrijf",
        "description": "Betrouwbaar klusbedrijf voor renovatie, onderhoud en reparaties in Dinteloord en omgeving.",
        "canonical": request.build_absolute_uri("/"),
        "type": "website",
        "image_abs": _abs_static(request, "img/og-default.jpg"),
        "robots": "index,follow",
    }
    return render(request, "index.html", {
        "slides": slides,
        "carousel_items": carousel_items,
        "value_block": value_block,
        "about_panel": about_panel,
        "about_url": about_url,
        "meta": meta,
    })


def over_ons(request):
    hero = AboutHero.objects.first()
    about_carousel = AboutCarouselItem.objects.all()
    company_block = AboutCompanyBlock.objects.first()
    process_steps = AboutProcessStep.objects.all()
    meta = {
        "title": "Over Ons | HMD Klusbedrijf",
        "description": "Ontdek HMD Klusbedrijf: 25 jaar vakmanschap in schilderwerk, vloeren, keukens en stukwerk. Betrouwbare service in Dinteloord en omgeving.",
        "canonical": request.build_absolute_uri(),
        "type": "website",
        "image_abs": _abs_static(request, "img/og-default.jpg"),
        "robots": "index,follow",
    }
    return render(request, "over-ons.html", {
        "meta": meta,
        "hero": hero,
        "about_carousel": about_carousel,
        "company_block": company_block,
        "process_steps": process_steps,
    })


def diensten(request):
    meta = {
        "title": "Diensten | HMD Klusbedrijf",
        "description": "Overzicht van alle diensten: kluswerk, renovaties, badkamers, timmerwerk, elektra en loodgieterij.",
        "canonical": request.build_absolute_uri(),
        "type": "website",
        "image_abs": _abs_static(request, "img/og-default.jpg"),
        "robots": "index,follow",
    }
    return render(request, "diensten.html", {"meta": meta})


def portfolio(request):
    items = PortfolioItem.objects.all()  # no is_active filter
    codes = list(items.values_list("category", flat=True).distinct())
    label_map = dict(PortfolioItem.CAT_CHOICES)
    categories = [(c, label_map.get(c, c)) for c in sorted(codes)]
    meta = {
        "title": "Portfolio | HMD Klusbedrijf",
        "description": "Projecten en referenties. Afbeeldingen in verschillende formaten, klik om te vergroten.",
        "canonical": request.build_absolute_uri(),
        "type": "website",
        "image_abs": _abs_static(request, "img/og-default.jpg"),
        "robots": "index,follow",
    }
    return render(request, "portfolio.html", {
        "items": items,
        "categories": categories,
        "meta": meta,
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactSubmission.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                message=form.cleaned_data["message"],
            )
            to_addr = _contact_to_email()
            subject = f"Nieuw contactformulier • {form.cleaned_data['name']}"
            body = (
                f"Naam: {form.cleaned_data['name']}\n"
                f"E-mail: {form.cleaned_data['email']}\n"
                f"Telefoon: {form.cleaned_data.get('phone','')}\n\n"
                f"Bericht:\n{form.cleaned_data['message']}\n"
            )
            send_mail(
                subject,
                body,
                getattr(dj_settings, "DEFAULT_FROM_EMAIL", to_addr),
                [to_addr],
                fail_silently=False,
            )
            messages.success(request, "Bericht verzonden. We nemen contact met u op.")
            return redirect("contact")
    else:
        form = ContactForm()

    meta = {
        "title": "Contact | HMD Klusbedrijf",
        "description": "Neem contact op voor vragen of een vrijblijvende offerte.",
        "canonical": request.build_absolute_uri(),
        "type": "website",
        "image_abs": _abs_static(request, "img/og-default.jpg"),
        "robots": "index,follow",
    }
    return render(request, "contact.html", {"form": form, "meta": meta})


# -------- service detail --------
# Slugs must match files: templates/diensten/<slug>.html
SERVICES = {
    "badkamer": {
        "name": "Badkamer",
        "desc": "Complete badkamer en renovaties op maat, van sloop tot afwerking.",
        "image": "img/diensten/badkamer.jpg",
    },
    "bouw-renovatie": {
        "name": "Bouw en Renovatie",
        "desc": "Kleine verbouwingen en renovaties strak gepland en opgeleverd.",
        "image": "img/diensten/bouwrenovatie.jpg",
    },
    "buitenwerk": {
        "name": "Buitenwerk",
        "desc": "Schuttingen, tuinhuizen en buitenafwerking met duurzaam materiaal.",
        "image": "img/diensten/buitenwerk.jpg",
    },
    "elektrisch-werk": {
        "name": "Elektrisch werk",
        "desc": "Groepenkast, schakelmateriaal en verlichting — veilig gemonteerd.",
        "image": "img/diensten/elektra-01.jpg",
    },
    "interieur-afwerking": {
        "name": "Interieur Afwerking",
        "desc": "Plinten, sierlijsten, lambrisering en strak kitwerk.",
        "image": "img/diensten/interieurafwerking.jpg",
    },
    "interieurstyling": {
        "name": "Interieur Styling",
        "desc": "Kleuradvies, verlichting en nette afwerking die past bij uw stijl.",
        "image": "img/diensten/interieur-styling.jpg",
    },
    "keukenrenovatie": {
        "name": "Keukenrenovatie",
        "desc": "Complete keukenrenovaties en plaatsing van maatwerk keukens.",
        "image": "img/diensten/keukenrerenovatie.jpg",
    },
    "klus-en-reparatiewerk": {
        "name": "Klus en Reparatiewerk",
        "desc": "Montage en herstel van dagelijks wooncomfort.",
        "image": "img/diensten/klus-advies.jpg",
    },
    "klus-onderhoud": {
        "name": "Klus en Onderhoud",
        "desc": "Kleine problemen snel en netjes opgelost.",
        "image": "img/diensten/klus-onderhoud.jpg",
    },
    "klusadvies": {
        "name": "Klus Advies",
        "desc": "Eerlijk advies over materialen, planning en uitvoering.",
        "image": "img/diensten/klus-advies.jpg",
    },
    "kluswerk-algemeen": {
        "name": "Kluswerk Algemeen",
        "desc": "Ophangen, monteren en kleine reparaties — netjes afgewerkt.",
        "image": "img/diensten/kluswerk-algemeen.jpg",
    },
    "loodgieterij": {
        "name": "Loodgieterij",
        "desc": "Lekkages, sanitair, afvoer en leidingwerk.",
        "image": "img/diensten/loodgieterij.jpg",
    },
    "materiaalkeuze": {
        "name": "Materiaal Keuze",
        "desc": "Keuzes voor vloer, verf, sanitair en profielen — passend bij het gebruik.",
        "image": "img/diensten/materiaalkeuze.jpg",
    },
    "onderhoud-en-reiniging": {
        "name": "Onderhoud en Reiniging",
        "desc": "Hogedruk, gevel- en dakgootreiniging, houtonderhoud.",
        "image": "img/diensten/onderhoud-reiniging.jpg",
    },
    "renovatie-en-verbouw": {
        "name": "Renovatie en Verbouw",
        "desc": "Keuken/badkamer, wanden/plafonds en vloeren met heldere planning.",
        "image": "img/diensten/renovatie-en-verbouw.jpg",
    },
    "schilderwerk": {
        "name": "Schilderwerk",
        "desc": "Binnen- en buitenschilderwerk met duurzame afwerking.",
        "image": "img/diensten/schilderwerk.jpg",
    },
    "stukwerk": {
        "name": "Stukwerk",
        "desc": "Strakke muren en plafonds met vakmanschap gestuct.",
        "image": "img/diensten/stukwerk.jpg",
    },
    "timmerwerk": {
        "name": "Timmerwerk",
        "desc": "Maatwerk, plaatsing en reparatie binnen/buiten.",
        "image": "img/diensten/timmerwerk.jpg",
    },
    "vloeren": {
        "name": "Vloeren",
        "desc": "Laminaat, PVC en hout met strakke afwerking.",
        "image": "img/diensten/vloeren.jpg",
    },
    "woning-renovatie": {
        "name": "Woningrenovatie",
        "desc": "Van vloer tot plafond — nette afwerking en betrouwbare uitvoering.",
        "image": "img/diensten/woningrenovatie.jpg",
    },
}


def service_detail(request, slug):
    svc = SERVICES.get(slug)
    if not svc:
        raise Http404
    meta = {
        "title": f"{svc['name']} | HMD Klusbedrijf",
        "description": svc["desc"],
        "canonical": request.build_absolute_uri(),
        "type": "website",
        "image_abs": _abs_static(request, svc.get("image", "img/og-default.jpg")),
        "robots": "index,follow",
    }
    return render(request, f"diensten/{slug}.html", {"meta": meta, "svc": svc})
