# analytics/services.py
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class GoogleAnalyticsService:
    """Service for fetching Google Analytics 4 data"""
    
    def __init__(self):
        self.property_id = getattr(settings, 'GA4_PROPERTY_ID', None)
        self.credentials_file = getattr(settings, 'GA4_CREDENTIALS_FILE', None)
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Google Analytics client"""
        if not self.property_id or not self.credentials_file:
            logger.warning("GA4_PROPERTY_ID or GA4_CREDENTIALS_FILE not configured")
            return None
            
        try:
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.oauth2 import service_account
            
            if os.path.exists(self.credentials_file):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_file
                )
                self.client = BetaAnalyticsDataClient(credentials=credentials)
                logger.info("Google Analytics client initialized successfully")
            else:
                logger.warning(f"Credentials file not found: {self.credentials_file}")
                
        except Exception as e:
            logger.error(f"Failed to initialize Google Analytics client: {e}")
            self.client = None
    
    def get_overview_data(self, days: int = 30, country_filter: str = None) -> Dict:
        """Get overview analytics data for the dashboard"""
        cache_key = f"ga_overview_{days}d_{country_filter or 'all'}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        if not self.client:
            # Return mock data if no client available
            return self._get_mock_data()
        
        try:
            data = self._fetch_analytics_data(days, country_filter)
            cache.set(cache_key, data, 3600)  # Cache for 1 hour
            return data
        except Exception as e:
            logger.error(f"Failed to fetch analytics data: {e}")
            return self._get_mock_data()
    
    def _fetch_analytics_data(self, days: int, country_filter: str = None) -> Dict:
        """Fetch real data from Google Analytics"""
        from google.analytics.data_v1beta import (
            RunReportRequest,
            Dimension,
            Metric,
            DateRange,
            Filter,
            FilterExpression,
        )
        
        # Define date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Basic metrics request - simplified for compatibility
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[
                Dimension(name="date"),
                Dimension(name="pagePath"),
                Dimension(name="country"),
                Dimension(name="deviceCategory"),
            ],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="bounceRate"),
                Metric(name="averageSessionDuration"),
                Metric(name="screenPageViews"),
            ],
            date_ranges=[DateRange(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )],
        )
        
        # Add country filter if specified
        if country_filter:
            request.dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="country",
                    string_filter=Filter.StringFilter(value=country_filter)
                )
            )
        
        response = self.client.run_report(request=request)
        
        # Also get daily data for charts
        daily_data = self._fetch_daily_chart_data(days, country_filter)
        
        # Process the response
        processed_data = self._process_analytics_response(response, country_filter)
        processed_data['daily_data'] = daily_data
        
        return processed_data
    
    def _fetch_daily_chart_data(self, days: int, country_filter: str = None) -> List[Dict]:
        """Fetch daily data for charts"""
        from google.analytics.data_v1beta import (
            RunReportRequest,
            Dimension,
            Metric,
            DateRange,
            Filter,
            FilterExpression,
        )
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
            ],
            date_ranges=[DateRange(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )],
        )
        
        if country_filter:
            request.dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="country",
                    string_filter=Filter.StringFilter(value=country_filter)
                )
            )
        
        response = self.client.run_report(request=request)
        
        daily_data = []
        for row in response.rows:
            date_str = row.dimension_values[0].value
            users = int(row.metric_values[0].value or 0)
            sessions = int(row.metric_values[1].value or 0)
            pageviews = int(row.metric_values[2].value or 0)
            
            daily_data.append({
                'date': date_str,
                'users': users,
                'sessions': sessions,
                'pageviews': pageviews,
            })
        
        return sorted(daily_data, key=lambda x: x['date'])
    
    def _process_analytics_response(self, response, country_filter: str = None) -> Dict:
        """Process the GA4 API response into dashboard data"""
        total_users = 0
        total_sessions = 0
        total_pageviews = 0
        bounce_rates = []
        session_durations = []
        
        page_views = {}
        countries = {}
        devices = {}
        
        for row in response.rows:
            # Extract metrics
            users = int(row.metric_values[0].value or 0)
            sessions = int(row.metric_values[1].value or 0)
            bounce_rate = float(row.metric_values[2].value or 0)
            avg_duration = float(row.metric_values[3].value or 0)
            pageviews = int(row.metric_values[4].value or 0)
            
            # Extract dimensions
            page_path = row.dimension_values[1].value
            country = row.dimension_values[2].value
            device = row.dimension_values[3].value
            
            # Aggregate data
            total_users += users
            total_sessions += sessions
            total_pageviews += pageviews
            
            if bounce_rate > 0:
                bounce_rates.append(bounce_rate)
            if avg_duration > 0:
                session_durations.append(avg_duration)
            
            # Track top pages
            if page_path in page_views:
                page_views[page_path] += pageviews
            else:
                page_views[page_path] = pageviews
            
            # Track countries
            if country in countries:
                countries[country] += users
            else:
                countries[country] = users
            
            # Track devices
            if device in devices:
                devices[device] += sessions
            else:
                devices[device] = sessions
        
        # Calculate averages
        avg_bounce_rate = sum(bounce_rates) / len(bounce_rates) if bounce_rates else 0
        avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
        
        # Get top items
        top_pages = sorted(page_views.items(), key=lambda x: x[1], reverse=True)[:5]
        top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]
        top_devices = sorted(devices.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "generated_at": datetime.now().isoformat(),
            "period": f"Last {len(set([row.dimension_values[0].value for row in response.rows]))} days",
            "overview": {
                "total_users": total_users,
                "total_sessions": total_sessions,
                "total_pageviews": total_pageviews,
                "bounce_rate": round(avg_bounce_rate, 1),
                "avg_session_duration": round(avg_session_duration, 0),
            },
            "top_pages": [{"page": page, "views": views} for page, views in top_pages],
            "top_countries": [{"country": country, "users": users} for country, users in top_countries],
            "device_breakdown": [{"device": device, "sessions": sessions} for device, sessions in top_devices],
        }
    
    def _get_mock_data(self) -> Dict:
        """Return mock data when real GA data is not available"""
        # Generate mock daily data
        daily_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6-i)
            daily_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'users': 45 + (i * 8),
                'sessions': 67 + (i * 12),
                'pageviews': 123 + (i * 20),
            })
        
        return {
            "generated_at": datetime.now().isoformat(),
            "period": "Last 30 days (Mock Data)",
            "overview": {
                "total_users": 1247,
                "total_sessions": 1891,
                "total_pageviews": 3456,
                "bounce_rate": 42.3,
                "avg_session_duration": 185,
            },
            "top_pages": [
                {"page": "/", "views": 892},
                {"page": "/diensten/", "views": 543},
                {"page": "/portfolio/", "views": 321},
                {"page": "/contact/", "views": 234},
                {"page": "/over-ons/", "views": 187},
            ],
            "top_countries": [
                {"country": "Netherlands", "users": 1089},
                {"country": "Belgium", "users": 87},
                {"country": "Germany", "users": 34},
                {"country": "United States", "users": 21},
                {"country": "France", "users": 16},
            ],
            "device_breakdown": [
                {"device": "desktop", "sessions": 1134},
                {"device": "mobile", "sessions": 623},
                {"device": "tablet", "sessions": 134},
            ],
            "daily_data": daily_data,
        }

# Initialize the service
ga_service = GoogleAnalyticsService()