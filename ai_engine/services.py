"""
AI Services for HMD Project
Provides OpenAI-powered features for admin assistance and business intelligence
"""
import os
import openai
from django.conf import settings
from django.core.cache import cache
from core.models import SiteSettings
from analytics.services import ga_service
from typing import Dict, List, Any
import json
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Base AI Service using OpenAI API"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
    def _make_request(self, messages: List[Dict], max_tokens: int = 1000, temperature: float = 0.7):
        """Make OpenAI API request with error handling"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Sorry, I'm experiencing technical difficulties. Please try again later."

class AdminAssistant(AIService):
    """AI Assistant for website administrators"""
    
    def __init__(self):
        super().__init__()
        self.context = self._get_admin_context()
    
    def _get_admin_context(self):
        """Get current website context for AI assistant"""
        try:
            site_settings = SiteSettings.objects.first()
            analytics_data = ga_service.get_overview_data()
            
            context = {
                'business_name': site_settings.company_name if site_settings else 'Demo Klusbedrijf',
                'website_type': 'Construction/Handyman Services',
                'current_users': analytics_data.get('overview', {}).get('total_users', 0),
                'main_market': 'Netherlands',
                'admin_features': [
                    'Google Analytics Dashboard',
                    'Site Settings Management', 
                    'Content Management',
                    'Business Information',
                    'Social Media Integration'
                ]
            }
            return context
        except Exception as e:
            logger.error(f"Error getting admin context: {e}")
            return {'business_name': 'Demo Klusbedrijf', 'website_type': 'Construction Services'}
    
    def get_help(self, question: str, context_type: str = "general") -> str:
        """Provide contextual help for admin questions"""
        
        system_prompt = f"""You are an AI assistant for {self.context['business_name']}, a {self.context['website_type']} website.
        
Current website stats:
- Total users: {self.context.get('current_users', 'N/A')}
- Main market: {self.context.get('main_market', 'Netherlands')}
- Available admin features: {', '.join(self.context.get('admin_features', []))}

You help website administrators with:
1. How to use the admin dashboard
2. Managing site settings and content
3. Understanding Google Analytics data
4. Best practices for website management
5. Technical guidance for Django admin

Be helpful, concise, and specific to this construction/handyman business.
If asked about features not available, suggest alternatives or explain limitations."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question about {context_type}: {question}"}
        ]
        
        return self._make_request(messages, max_tokens=500, temperature=0.3)

class BusinessIntelligenceAI(AIService):
    """AI for business insights and recommendations"""
    
    def analyze_website_performance(self) -> Dict[str, Any]:
        """Analyze current website performance and provide insights"""
        
        try:
            # Get analytics data
            analytics_data = ga_service.get_overview_data()
            
            # Get site settings
            site_settings = SiteSettings.objects.first()
            
            analysis_prompt = f"""Analyze this website performance data for {site_settings.company_name if site_settings else 'Demo Klusbedrijf'}, a construction/handyman service in the Netherlands:

Analytics Data:
- Total Users: {analytics_data.get('overview', {}).get('total_users', 0)}
- Sessions: {analytics_data.get('overview', {}).get('sessions', 0)}
- Main Country: Netherlands ({analytics_data.get('overview', {}).get('netherlands_users', 0)} users)
- Website: Construction/Handyman services
- Business Location: Netherlands

Provide insights on:
1. Performance summary (2-3 sentences)
2. Key strengths (2 points)
3. Improvement opportunities (2 specific recommendations)
4. Market insights for Netherlands construction market

Keep it business-focused, actionable, and under 200 words total."""

            messages = [
                {"role": "system", "content": "You are a business intelligence analyst specializing in construction/service businesses."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            analysis = self._make_request(messages, max_tokens=300, temperature=0.4)
            
            return {
                'analysis': analysis,
                'data_points': {
                    'total_users': analytics_data.get('overview', {}).get('total_users', 0),
                    'sessions': analytics_data.get('overview', {}).get('sessions', 0),
                    'netherlands_users': analytics_data.get('overview', {}).get('netherlands_users', 0),
                },
                'generated_at': analytics_data.get('generated_at', 'Unknown')
            }
            
        except Exception as e:
            logger.error(f"Error in business intelligence analysis: {e}")
            return {
                'analysis': 'Unable to generate analysis at this time. Please check your analytics connection.',
                'data_points': {},
                'generated_at': 'Error'
            }
    
    def generate_content_suggestions(self, content_type: str = "services") -> str:
        """Generate content suggestions for the website"""
        
        try:
            site_settings = SiteSettings.objects.first()
            business_name = site_settings.company_name if site_settings else 'Demo Klusbedrijf'
            
            content_prompt = f"""Generate content suggestions for {business_name}, a construction/handyman service business in the Netherlands.

Business Details:
- Name: {business_name}
- Location: Netherlands (Amsterdam area)
- Services: General construction, handyman services
- Target Market: Dutch homeowners and businesses

Generate 3 specific {content_type} suggestions that would:
1. Appeal to Dutch customers
2. Highlight local expertise
3. Include relevant keywords for SEO
4. Be practical and actionable

Format as numbered list with brief explanations."""

            messages = [
                {"role": "system", "content": "You are a content marketing specialist for construction businesses in the Netherlands."},
                {"role": "user", "content": content_prompt}
            ]
            
            return self._make_request(messages, max_tokens=400, temperature=0.6)
            
        except Exception as e:
            logger.error(f"Error generating content suggestions: {e}")
            return "Unable to generate content suggestions at this time."

class DemoAI(AIService):
    """Demo AI features to showcase premium capabilities"""
    
    def get_demo_insights(self) -> Dict[str, str]:
        """Provide sample AI insights for demonstration"""
        
        demo_insights = {
            'trend_analysis': "📈 Your website traffic shows 88% visitors from Netherlands, indicating strong local market presence. Peak activity occurs on weekdays, suggesting B2B opportunities.",
            
            'seo_suggestion': "🔍 Consider adding content about 'Klusbedrijf Amsterdam' and 'Handyman Utrecht' to capture more local search traffic in your region.",
            
            'business_opportunity': "💡 Premium Feature: AI suggests targeting 'bathroom renovation' and 'garden maintenance' services based on seasonal trends in your area.",
            
            'content_idea': "✍️ Recommended blog post: 'Winter Maintenance Tips for Dutch Homes' - targets seasonal keywords and establishes expertise.",
            
            'conversion_tip': "🎯 Premium Analytics shows most users visit your services page first - consider adding a quote request form there for 23% higher conversions."
        }
        
        return demo_insights

# Initialize AI services
admin_assistant = AdminAssistant()
business_ai = BusinessIntelligenceAI()
demo_ai = DemoAI()