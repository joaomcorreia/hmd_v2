from django.db import models
from django.contrib.auth import get_user_model

class AIPlan(models.TextChoices):
    STARTER = "starter", "Starter"
    LOCAL   = "local",   "Local"
    PRO     = "pro",     "Pro"

class ServiceTag(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class LocationTag(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    radius_km = models.PositiveIntegerField(default=0)  # 0 = exact city
    def __str__(self): return self.name

class AIProfile(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    plan  = models.CharField(max_length=20, choices=AIPlan.choices, default=AIPlan.STARTER)
    languages = models.CharField(max_length=80, default="nl")  # csv e.g. "nl,en"
    max_services  = models.PositiveIntegerField(default=5)
    max_locations = models.PositiveIntegerField(default=1)
    auto_publish  = models.BooleanField(default=False)
    def __str__(self): return f"{self.owner or 'site'} [{self.plan}]"

class PromptTemplate(models.Model):
    key = models.CharField(max_length=50, unique=True)  # e.g. meta_title/meta_desc/jsonld/faq
    text = models.TextField()
    def __str__(self): return self.key

class AIContent(models.Model):
    KIND_CHOICES = [
        ("meta_title","Meta Title"),
        ("meta_desc","Meta Description"),
        ("jsonld","JSON-LD"),
        ("faq","FAQ"),
    ]
    profile   = models.ForeignKey(AIProfile, on_delete=models.CASCADE)
    service   = models.ForeignKey(ServiceTag, on_delete=models.CASCADE)
    location  = models.ForeignKey(LocationTag, on_delete=models.CASCADE, null=True, blank=True)
    language  = models.CharField(max_length=8, default="nl")
    kind      = models.CharField(max_length=20, choices=KIND_CHOICES)
    content   = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile","service","location","language","kind")

class AILog(models.Model):
    profile = models.ForeignKey(AIProfile, on_delete=models.CASCADE)
    event   = models.CharField(max_length=120)
    detail  = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.profile} - {self.event}"

# New AI Assistant Models
class AIAssistantConversation(models.Model):
    """Store AI assistant conversations for admin support"""
    CONVERSATION_TYPES = [
        ('admin_help', 'Admin Help'),
        ('business_insights', 'Business Insights'),
        ('content_generation', 'Content Generation'),
        ('demo', 'Demo Feature'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPES)
    question = models.TextField()
    ai_response = models.TextField()
    context_data = models.JSONField(default=dict, blank=True)  # Store context like analytics data
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.conversation_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AIInsight(models.Model):
    """Store generated business insights and recommendations"""
    INSIGHT_TYPES = [
        ('performance', 'Website Performance'),
        ('seo', 'SEO Recommendations'),
        ('content', 'Content Suggestions'),
        ('business', 'Business Opportunities'),
        ('analytics', 'Analytics Analysis'),
    ]
    
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    analytics_data = models.JSONField(default=dict, blank=True)
    is_premium = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.insight_type} - {self.title}"
