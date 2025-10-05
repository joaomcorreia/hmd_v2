from django.urls import path
from . import views, contextual_views

urlpatterns = [
    path("health/", views.health, name="ai_health"),
    path("preview/", views.preview, name="ai_preview"),
    path("publish/<int:pk>/", views.publish, name="ai_publish"),
    
    # AI Assistant URLs
    path("assistant/", views.ai_assistant_dashboard, name="ai_assistant_dashboard"),
    path("assistant/ask/", views.ask_assistant, name="ai_ask_assistant"),
    path("assistant/insights/", views.generate_business_insights, name="ai_business_insights"),
    path("assistant/content/", views.generate_content_suggestions, name="ai_content_suggestions"),
    path("assistant/history/", views.conversation_history, name="ai_conversation_history"),
    
    # Contextual AI Assistant (floating widget)
    path("contextual/", contextual_views.contextual_assistant, name="contextual_assistant"),
    path("escalate/", contextual_views.escalate_to_support, name="escalate_support"),
]
