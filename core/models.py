from django.db import models

# --- Slider ---
class Slide(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='slider/')
    cta1_label = models.CharField(max_length=40, blank=True)
    cta1_url = models.URLField(blank=True)
    cta2_label = models.CharField(max_length=40, blank=True)
    cta2_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order} · {self.title}"


# --- Portfolio (single, canonical definition) ---


# --- Homepage about block ---
class HomeAboutPanel(models.Model):
    title_emphasis = models.CharField(max_length=60, default='Toegewijd')
    title_rest = models.CharField(max_length=160, default='aan kwaliteit en vakmanschap.')
    lead_text = models.TextField(blank=True, default='HMD Klusbedrijf is opgericht door Juma Al Huseyin en staat voor betrouwbaarheid, kwaliteit en eerlijke service. Met oog voor detail voert hij elke klus uit alsof het zijn eigen huis is.')
    body_text = models.TextField(blank=True, default='Of het nu gaat om kleine reparaties, schilderwerk, timmerklussen of een volledige badkamerrenovatie - HMD Klusbedrijf levert professioneel werk binnen een straal van 50 km rond Dinteloord.')
    cta_label = models.CharField(max_length=80, default='Lees Meer')
    cta_url = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        verbose_name = 'Homepage about panel'
        verbose_name_plural = 'Homepage about panel'

    def __str__(self):
        return f"About panel: {self.title_emphasis} {self.title_rest}"





class HomeValueBlock(models.Model):
    image = models.ImageField(upload_to='home-value/', blank=True)
    image_alt = models.CharField(max_length=160, blank=True, default='Werk in uitvoering')
    title_emphasis = models.CharField(max_length=80, default='Wij leveren')
    title_rest = models.CharField(max_length=160, default='vakwerk waar u op kunt vertrouwen')
    body = models.TextField(blank=True, default='HMD Klusbedrijf voert elke klus met zorg en vakmanschap uit. Of het nu gaat om een kleine reparatie of een complete renovatie, wij staan klaar voor particulieren in de regio Dinteloord en omgeving.')
    link_1_label = models.CharField(max_length=120, blank=True, default='Klus en Reparatiewerk')
    link_1_url = models.CharField(max_length=200, blank=True, default='/diensten/kluswerk/')
    link_2_label = models.CharField(max_length=120, blank=True, default='Timmerwerk & interieur')
    link_2_url = models.CharField(max_length=200, blank=True, default='/diensten/timmerwerk/')
    link_3_label = models.CharField(max_length=120, blank=True, default='Badkamerrenovatie & buitenwerk')
    link_3_url = models.CharField(max_length=200, blank=True, default='/diensten/badkamer-renovatie/')

    class Meta:
        verbose_name = 'Homepage value block'
        verbose_name_plural = 'Homepage value block'

    def __str__(self):
        return f"Value block: {self.title_emphasis} {self.title_rest}"

class HomeCarouselItem(models.Model):
    image = models.ImageField(upload_to='home-carousel/')
    alt_text = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.alt_text or f'Carousel item {self.pk}'



class AboutHero(models.Model):
    title = models.CharField(max_length=160, default='Wij bouwen aan kwaliteit en sterkere gemeenschappen.')
    background_image = models.ImageField(upload_to='about-hero/', blank=True)

    class Meta:
        verbose_name = 'About hero'
        verbose_name_plural = 'About hero'

    def __str__(self):
        return 'About hero'


class AboutCarouselItem(models.Model):
    image = models.ImageField(upload_to='about-carousel/')
    alt_text = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'About carousel item'

    def __str__(self):
        return self.alt_text or f'About slide {self.pk}'


class AboutCompanyBlock(models.Model):
    years_number = models.CharField(max_length=10, default='25')
    years_label = models.CharField(max_length=60, default='Jaar Ervaring')
    heading = models.CharField(max_length=160, default='Leefkwaliteit verbeteren met een persoonlijke en vakkundige aanpak.')
    body = models.TextField(blank=True, default='Bij HMD Klusbedrijf draait alles om vakmanschap, betrouwbaarheid en oog voor detail. Al 25 jaar levert oprichter Juma Al Huseyin kwalitatief werk in en rond Dinteloord - van schilderwerk tot volledige renovaties.')
    cta_label = models.CharField(max_length=120, blank=True, default='Neem contact op')
    cta_url = models.CharField(max_length=200, blank=True, default='/contact/')

    class Meta:
        verbose_name = 'About company block'

    def __str__(self):
        return self.heading


class AboutBenefit(models.Model):
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='about-benefits/', blank=True)
    image_alt = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'About benefit'
        verbose_name_plural = 'About benefits'

    def __str__(self):
        return self.title or f'Benefit {self.pk}'

class AboutProcessStep(models.Model):
    order = models.PositiveIntegerField(default=1)
    step_title = models.CharField(max_length=60, default='Stap 1')
    heading = models.CharField(max_length=160)
    description = models.TextField()
    image = models.ImageField(upload_to='about-process/', blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'About process step'
        verbose_name_plural = 'About process steps'

    def __str__(self):
        return f"{self.step_title} - {self.heading}"

class PortfolioItem(models.Model):
    # choices used by admin forms
    CAT_CHOICES = [
        ("1", "Keuken"),
        ("2", "Badkamer"),
        ("3", "Vloeren"),
        ("4", "Kluswerk Algemeen"),
        ("5", "Klus en Reparatiewerk"),
        ("6", "Timmerwerk"),
        ("7", "Elektrisch Werk"),
        ("8", "Loodgieterij"),
        ("9", "Stukwerk"),
    ]

    # map to URL/CSS slugs
    SLUGS = {
        "1": "keuken",
        "2": "badkamer",
        "3": "vloeren",
        "4": "kluswerk-algemeen",
        "5": "klus-en-reparatiewerk",
        "6": "timmerwerk",
        "7": "elektrisch-werk",
        "8": "loodgieterij",
        "9": "stukwerk",
    }

    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="portfolio/")
    category = models.CharField(max_length=2, choices=CAT_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created"]

    def __str__(self):
        return self.title or f"Item {self.pk}"

    @property
    def category_slug(self) -> str:
        return self.SLUGS.get(self.category, "overig")


# --- Core / site ---
class SiteSettings(models.Model):
    company_name = models.CharField(max_length=120, blank=True, default="HMD Klusbedrijf")
    contact_email = models.EmailField(default="justcodeworks@gmail.com")
    whatsapp = models.CharField(max_length=32, blank=True, default="+31687111289")
    phone_display = models.CharField(max_length=32, blank=True, default="06 87111289")

    @property
    def whatsapp_digits(self) -> str:
        raw = self.whatsapp or ""
        digits = ''.join(ch for ch in raw if ch.isdigit())
        if digits.startswith('00'):
            digits = digits[2:]
        return digits or '31687111289'

    @property
    def whatsapp_url(self) -> str:
        return f"https://wa.me/{self.whatsapp_digits}"

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} • {self.created_at:%Y-%m-%d %H:%M}"


# --- Facebook integration ---
class FacebookSettings(models.Model):
    page_id = models.CharField(max_length=64, blank=True)
    page_name = models.CharField(max_length=255, blank=True)
    ad_account_id = models.CharField(max_length=64, blank=True)
    app_id = models.CharField(max_length=64, blank=True)
    app_secret = models.CharField(max_length=128, blank=True)
    user_access_token = models.TextField(blank=True)      # short-lived
    page_access_token = models.TextField(blank=True)      # long-lived
    token_expires = models.DateTimeField(null=True, blank=True)
    connected = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Facebook settings"
        verbose_name_plural = "Facebook settings"

    def __str__(self):
        return "Facebook settings"


class FacebookPost(models.Model):
    page_post_id = models.CharField(max_length=128, unique=True)  # {page_id}_{post_id}
    created_time = models.DateTimeField()
    message = models.TextField(blank=True)
    permalink = models.URLField(max_length=500, blank=True)
    media_url = models.URLField(max_length=500, blank=True)
    reactions = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_time"]


class FacebookLead(models.Model):
    lead_id = models.CharField(max_length=64, unique=True)
    form_id = models.CharField(max_length=64)
    created_time = models.DateTimeField()
    data = models.JSONField()
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_time"]


class FacebookCampaign(models.Model):
    campaign_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=32)
    daily_budget = models.IntegerField(null=True, blank=True)  # cents
    objective = models.CharField(max_length=64, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_stop = models.DateField(null=True, blank=True)
    spend = models.FloatField(default=0.0)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)


# --- Quote Requests ---
class QuoteRequest(models.Model):
    # Contact Information
    name = models.CharField(max_length=100, verbose_name="Naam")
    phone = models.CharField(max_length=20, verbose_name="Telefoon")
    address = models.CharField(max_length=200, blank=True, verbose_name="Adres")
    city = models.CharField(max_length=100, blank=True, verbose_name="Plaats")
    
    # Services (stored as comma-separated string for simplicity)
    services = models.TextField(verbose_name="Gewenste Diensten")
    
    # Planning
    preferred_date = models.DateField(null=True, blank=True, verbose_name="Gewenste Datum")
    flexible_timing = models.BooleanField(default=False, verbose_name="Datum Flexibel")
    
    # Description
    description = models.TextField(blank=True, verbose_name="Opmerking/Beschrijving")
    
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Aangevraagd op")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Adres")
    user_agent = models.TextField(blank=True, verbose_name="Browser Info")
    
    # Status tracking
    STATUS_CHOICES = [
        ('new', 'Nieuw'),
        ('contacted', 'Contact opgenomen'),
        ('quoted', 'Offerte verstuurd'),
        ('accepted', 'Geaccepteerd'),
        ('completed', 'Voltooid'),
        ('declined', 'Afgewezen'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    notes = models.TextField(blank=True, verbose_name="Interne notities")
    
    class Meta:
        verbose_name = "Offerte Aanvraag"
        verbose_name_plural = "Offerte Aanvragen"
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone} ({self.submitted_at.strftime('%d/%m/%Y %H:%M')})"
    
    def get_services_list(self):
        """Return services as a list for display"""
        return [s.strip() for s in self.services.split(',') if s.strip()]
    
    def get_whatsapp_message(self):
        """Generate the WhatsApp message that was sent"""
        message = f"*OFFERTE AANVRAAG*\n========================\n\n"
        message += f"*CONTACTGEGEVENS*\nNaam: {self.name}\nTelefoon: {self.phone}\n"
        if self.address:
            message += f"Adres: {self.address}\n"
        if self.city:
            message += f"Plaats: {self.city}\n"
        message += f"\n*GEWENSTE DIENSTEN*\n"
        for service in self.get_services_list():
            message += f"- {service}\n"
        if self.preferred_date or self.flexible_timing:
            message += f"\n*PLANNING*\n"
            if self.preferred_date:
                message += f"Gewenste datum: {self.preferred_date}\n"
            if self.flexible_timing:
                message += f"Datum is flexibel\n"
        if self.description:
            message += f"\n*OPMERKING*\n{self.description}\n"
        message += f"\nAangevraagd op: {self.submitted_at.strftime('%d-%m-%Y')}\nVia: HMD Klusbedrijf website"
        return message

