from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from .models import AIContent, AIAssistantConversation, AIInsight
from .services import admin_assistant, business_ai, demo_ai

@staff_member_required
def preview(request):
    items = AIContent.objects.order_by("-updated_at")[:200]
    return render(request, "ai_engine/preview.html", {"items": items})

@staff_member_required
def publish(request, pk):
    item = get_object_or_404(AIContent, pk=pk)
    item.is_published = True
    item.save()
    return redirect("ai_preview")

@staff_member_required
def ai_assistant_dashboard(request):
    """Main AI Assistant dashboard for admins"""
    
    # Get recent conversations
    recent_conversations = AIAssistantConversation.objects.filter(
        user=request.user
    )[:10]
    
    # Get demo insights
    demo_insights = demo_ai.get_demo_insights()
    
    # Get business analysis if premium enabled
    business_analysis = None
    if settings.AI_PREMIUM_FEATURES_ENABLED:
        business_analysis = business_ai.analyze_website_performance()
    
    # Get SiteSettings for template
    from core.models import SiteSettings
    site_settings = SiteSettings.objects.first()
    
    context = {
        'recent_conversations': recent_conversations,
        'demo_insights': demo_insights,
        'business_analysis': business_analysis,
        'premium_enabled': settings.AI_PREMIUM_FEATURES_ENABLED,
        'openai_configured': bool(settings.OPENAI_API_KEY),
        'site_settings': site_settings,
        'sidebar_template': 'admin/sidebar.html',  # For admin template consistency
    }
    
    return render(request, "ai_engine/assistant_dashboard.html", context)

@staff_member_required
@csrf_exempt
def ask_assistant(request):
    """Handle AI assistant questions via AJAX"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        context_type = data.get('context_type', 'general')
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Get AI response
        ai_response = admin_assistant.get_help(question, context_type)
        
        # Save conversation
        conversation = AIAssistantConversation.objects.create(
            user=request.user,
            conversation_type='admin_help',
            question=question,
            ai_response=ai_response,
            context_data={'context_type': context_type},
            is_premium=False  # Basic admin help is free
        )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'conversation_id': conversation.id,
            'timestamp': conversation.created_at.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def generate_business_insights(request):
    """Generate premium business insights"""
    
    if not settings.AI_PREMIUM_FEATURES_ENABLED:
        return JsonResponse({
            'error': 'Premium features not enabled',
            'demo': True
        }, status=403)
    
    try:
        # Generate business analysis
        analysis = business_ai.analyze_website_performance()
        
        # Save insight
        insight = AIInsight.objects.create(
            insight_type='business',
            title='AI Business Performance Analysis',
            content=analysis['analysis'],
            analytics_data=analysis['data_points'],
            is_premium=True,
            is_demo=False
        )
        
        return JsonResponse({
            'success': True,
            'analysis': analysis,
            'insight_id': insight.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def generate_content_suggestions(request):
    """Generate content suggestions for the website"""
    
    content_type = request.GET.get('type', 'services')
    
    try:
        suggestions = business_ai.generate_content_suggestions(content_type)
        
        # Save as conversation
        conversation = AIAssistantConversation.objects.create(
            user=request.user,
            conversation_type='content_generation',
            question=f"Generate {content_type} content suggestions",
            ai_response=suggestions,
            is_premium=settings.AI_PREMIUM_FEATURES_ENABLED
        )
        
        return JsonResponse({
            'success': True,
            'suggestions': suggestions,
            'conversation_id': conversation.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def conversation_history(request):
    """View conversation history"""
    
    conversations = AIAssistantConversation.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]
    
    context = {
        'conversations': conversations
    }
    
    return render(request, "ai_engine/conversation_history.html", context)

def health(request):
    return HttpResponse("ai ok")
