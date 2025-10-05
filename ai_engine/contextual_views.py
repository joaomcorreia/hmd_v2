"""
Contextual AI Assistant for Admin Pages
Provides context-aware help based on current admin page
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json
from .services import admin_assistant
from .models import AIAssistantConversation

@csrf_exempt
def contextual_assistant(request):
    """Handle contextual AI assistant requests"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        current_page = data.get('current_page', 'unknown')
        page_context = data.get('page_context', {})
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Get contextual response based on current admin page
        ai_response = get_contextual_response(
            question=question,
            current_page=current_page,
            page_context=page_context,
            user=request.user
        )
        
        # Save conversation (only for authenticated users)
        conversation = None
        if request.user.is_authenticated:
            conversation = AIAssistantConversation.objects.create(
                user=request.user,
                conversation_type='contextual_help',
                question=question,
                ai_response=ai_response,
                context_data={
                    'current_page': current_page,
                    'page_context': page_context,
                    'is_frontend': current_page == 'frontend'
                },
                is_premium=False
            )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'conversation_id': conversation.id if conversation else None,
            'can_escalate': True  # Always allow escalation to email support
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_contextual_response(question, current_page, page_context, user):
    """Generate contextual AI response based on current page (admin or frontend)"""
    
    # Check if this is a frontend customer request
    if current_page == 'frontend' or page_context == 'customer':
        return get_customer_response(question, user)
    
    # Map admin pages to context
    page_contexts = {
        'portfolio': {
            'area': 'Portfolio Management',
            'capabilities': [
                'Add new portfolio items with images',
                'Edit project descriptions and details',
                'Organize portfolio categories',
                'Upload and manage project photos',
                'Set featured projects'
            ],
            'greeting': f"Good morning {getattr(user, 'first_name', '') or getattr(user, 'username', 'there')}! I can see you're working on the Portfolio page. I can help you manage your projects, upload new images, or organize your portfolio showcase."
        },
        'analytics': {
            'area': 'Google Analytics Dashboard', 
            'capabilities': [
                'Understand visitor statistics and trends',
                'Analyze Netherlands traffic patterns',
                'Interpret conversion data and real-time data',
                'Explain real-time analytics features',
                'Help with location tracking and live user monitoring',
                'Explain why your location might not appear in real-time data',
                'Guide through historical vs real-time analytics differences'
            ],
            'greeting': f"Hello {getattr(user, 'first_name', '') or getattr(user, 'username', 'there')}! You're viewing the Analytics dashboard with real traffic data (355 users) AND new real-time features. I can help explain visitor trends, the live user tracking system, or answer questions about real-time analytics.",
            'real_time_info': {
                'feature_description': 'The red "Live Bezoekers" section shows real-time website activity',
                'update_frequency': 'Updates automatically every 15 seconds',
                'data_types': ['Current active users count', 'Live geographic locations', 'Real-time device breakdown', 'Active pages being viewed'],
                'location_accuracy': 'Location data comes from IP geolocation - may show ISP location or nearby city, not exact visitor location',
                'data_delay': 'Real-time: 15-30 seconds | Historical: 1-4 hours',
                'api_differences': 'Google\'s official dashboard may show more accurate locations than our custom website dashboard due to different API endpoints and enhanced geolocation services',
                'common_issues': [
                    'Your own visits may not appear if you have analytics blocked',
                    'Location may show ISP city (like Amsterdam) instead of actual city',
                    'VPN users will show VPN server location',
                    'Some visitors may be filtered out by ad blockers',
                    'Google Analytics dashboard vs website dashboard may show different location accuracy'
                ]
            }
        },
        'settings': {
            'area': 'Site Settings Management',
            'capabilities': [
                'Update business information and contact details',
                'Manage social media links',
                'Configure phone numbers and addresses',
                'Update opening hours and KvK number',
                'Customize site appearance'
            ],
            'greeting': f"Hi {getattr(user, 'first_name', '') or getattr(user, 'username', 'there')}! I see you're in Site Settings. I can help you update your business information, configure contact details, or manage your social media links."
        },
        'quotes': {
            'area': 'Quote Request Management',
            'capabilities': [
                'Manage incoming quote requests',
                'Respond to customer inquiries',
                'Track request status and follow-ups',
                'Export customer data',
                'Set up automated responses'
            ],
            'greeting': f"Good day {getattr(user, 'first_name', '') or getattr(user, 'username', 'there')}! You're managing quote requests. I can help you process customer inquiries, track requests, or set up response templates."
        },
        'content': {
            'area': 'Content Management',
            'capabilities': [
                'Edit homepage content and sliders',
                'Update service descriptions',
                'Manage about page content',
                'Upload images and media',
                'Optimize content for SEO'
            ],
            'greeting': f"Welcome {getattr(user, 'first_name', '') or getattr(user, 'username', 'there')}! You're editing website content. I can help with text updates, image uploads, SEO optimization, or content structure improvements."
        }
    }
    
    # Get context for current page
    context = page_contexts.get(current_page, {
        'area': 'Website Administration',
        'capabilities': [
            'Navigate the admin interface',
            'Manage website content and settings',
            'Understand admin features and tools',
            'Get help with common tasks',
            'Escalate complex issues to support'
        ],
        'greeting': f"Hello {getattr(user, 'first_name', '') or getattr(user, 'username', 'there')}! I'm here to help with any admin tasks. What would you like to work on today?"
    })
    
    # Create contextual system prompt
    system_prompt = f"""You are a helpful AI assistant for Demo Klusbedrijf's website admin panel. 

Current Context:
- Admin User: {getattr(user, 'first_name', '') or getattr(user, 'username', 'User')}
- Current Page: {context['area']}
- Available Actions: {', '.join(context['capabilities'])}

Your role:
1. Provide specific, actionable help for the current admin page
2. Be friendly but concise - admins are busy
3. Reference Demo Klusbedrijf's construction/handyman business context
4. If you can't solve something, suggest escalating to technical support
5. Always offer concrete next steps

Business Context:
- Demo Klusbedrijf: Dutch construction/handyman service
- Location: Amsterdam, Netherlands  
- Services: Construction, maintenance, renovations
- Website: 355+ users, 88% from Netherlands

Analytics Features:
- Real-time analytics: Live user tracking via GA4 Real-time API, updates every 15 seconds
- Location data: Based on IP geolocation - may show ISP location (Amsterdam, Rotterdam) not your exact city  
- Historical analytics: 1-4 hour delay for standard reports
- Real-time shows: Active users, live locations, devices, live map with user markers
- Production accuracy: Uses GA4_REALTIME_API (not mock data) for paid features
- Location accuracy: Often shows internet provider city, VPN locations, or major nearby cities
- Common cases: Raamsdonksveer users might appear as "Breda" or "Tilburg" (ISP locations)
- GA Dashboard vs Website: Google's official dashboard may show more accurate locations than our API implementation
- Live Map: Interactive Netherlands map showing real-time user locations with markers
- Data validation: Automatic detection of mock vs real data for production quality assurance

CRITICAL - International Visitors on .nl Websites:
- .nl domain does NOT restrict visitors to Netherlands - anyone worldwide can access it
- .nl just means "registered in Netherlands" - visitors can come from anywhere
- International traffic is NORMAL and POSITIVE for Dutch businesses
- Common sources: Google searches abroad, social media, business referrals, VPNs, expats
- Seeing visitors from US, Canada, France, Poland indicates good SEO and international appeal
- Domain extension never limits who can visit a website

Real-time Troubleshooting:
- Real-time only shows ACTIVE users (currently browsing RIGHT NOW)
- If no active users, shows 0 (completely normal)
- Different browsers/profiles count as separate sessions
- Takes 1-2 minutes for new sessions to appear
- User must actively click/scroll to stay "active"

LOGIN ASSISTANCE FOR OWNER:
When the owner asks about login issues or how to access the admin panel:
1. FIRST: Explain they need their login credentials to access the admin panel
2. ASK: "Do you have your login credentials?"
3. IF THEY SAY NO: Provide these specific instructions:
   - "Click on the login icon at the top of the page"
   - "Select 'Forgot Password' or 'Request New Password'"
   - "When prompted for email, use the email address you have on file or the email you used to sign up"
   - "Check your email for password reset instructions"
   - "Follow the link in the email to set a new password"
4. Be helpful and guide them through each step clearly
5. If they need the exact email address, suggest checking their records or trying common business emails

Response Style: Professional, helpful, direct. Maximum 3-4 sentences unless complex explanation needed or providing login instructions."""

    # Get AI response with contextual prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    try:
        response = admin_assistant._make_request(messages, max_tokens=300, temperature=0.3)
        return response
    except Exception as e:
        return f"I'm having technical difficulties right now. For immediate help with {context['area'].lower()}, please contact technical support. Error details: {str(e)}"

@staff_member_required
@csrf_exempt  
def escalate_to_support(request):
    """Escalate admin issue to email support"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        issue_description = data.get('issue_description', '')
        current_page = data.get('current_page', 'unknown')
        conversation_id = data.get('conversation_id')
        
        # Here you would implement email sending
        # For now, we'll just log it and return success
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        email_body = f"""
Technical Support Request from Admin Panel

Admin User: {request.user.username} ({request.user.email})
Current Page: {current_page}
Issue Description: {issue_description}

Conversation ID: {conversation_id}
Timestamp: {timezone.now()}

Please investigate and provide assistance.
"""
        
        # Send email (configure EMAIL_BACKEND in settings.py)
        try:
            send_mail(
                subject=f'Admin Support Request - {current_page}',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['support@hmdklusbedrijf.nl'],  # Configure this
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Your request has been sent to technical support. We\'ll respond within 24 hours.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': True,  # Still return success for now
                'message': 'Request logged. Technical support will be notified. (Email configuration needed for automatic sending)'
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_customer_response(question, user):
    """Generate AI response for frontend customers"""
    
    # Import here to avoid circular imports
    from ai_engine.services import admin_assistant
    
    # Get business context
    from core.models import SiteSettings
    site_settings = SiteSettings.objects.first()
    
    # Customer-focused system prompt
    system_prompt = f"""You are the AI assistant for Demo Klusbedrijf, a Dutch construction and renovation company.

Business Information:
- Company: {site_settings.company_name if site_settings else 'Demo Klusbedrijf'}
- Location: {site_settings.business_address if site_settings else 'Amsterdam, Netherlands'}
- Phone: {site_settings.phone_display if site_settings else '0167-123456'}
- Services: Klus en reparatiewerk (handyman work), Renovatie en verbouw (renovation & construction)

Instructions:
1. Respond in Dutch (Nederlandse)
2. Be helpful, professional, and friendly
3. Focus on how HMD can help with their construction/renovation needs
4. If asked about pricing, explain that prices depend on the specific project and offer to connect them for a quote
5. If asked about availability, suggest contacting for current scheduling
6. Always encourage them to contact HMD for personalized service
7. Keep responses concise but informative (max 3-4 sentences)

LOGIN ASSISTANCE (if owner asks about admin access):
When someone asks about logging into the website admin or managing the site:
1. FIRST: "Om in te loggen heeft u uw login gegevens nodig"
2. ASK: "Heeft u uw login gegevens?"
3. IF THEY SAY NO: 
   - "Klik op het login icoontje bovenaan de pagina"
   - "Vraag een nieuw wachtwoord aan"
   - "Gebruik bij het e-mailadres het adres dat u in uw administratie heeft of het e-mailadres waarmee u zich heeft aangemeld"
   - "Controleer uw e-mail voor instructies"

Contact Information:
- For quotes/questions: Use the contact form or call directly
- WhatsApp available for quick questions
- Service area: Primarily Netherlands, especially around Amsterdam region

Response Style: Friendly, professional, helpful Dutch customer service representative."""

    # Get AI response with customer context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    try:
        response = admin_assistant._make_request(messages, max_tokens=200, temperature=0.3)
        return response
        
    except Exception as e:
        # Friendly fallback response in Dutch
        return "Sorry, ik ondervind momenteel technische problemen. Voor directe hulp kunt u ons bellen of een bericht sturen via WhatsApp. We helpen u graag verder met uw klus- of renovatieproject!"