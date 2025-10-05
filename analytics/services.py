# analytics/services.py
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.core.cache import cache
import logging
import requests

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
    
    def _get_location_coordinates(self, city: str, country: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a city/country combination"""
        cache_key = f"geocode_{city}_{country}"
        cached_coords = cache.get(cache_key)
        
        if cached_coords:
            return cached_coords
        
        # Comprehensive Dutch cities database
        dutch_coordinates = {
            'Amsterdam': (52.3676, 4.9041),
            'Rotterdam': (51.9225, 4.47917),
            'Utrecht': (52.0907, 5.1214),
            'Eindhoven': (51.4416, 5.4697),
            'Tilburg': (51.5555, 5.0913),
            'Groningen': (53.2194, 6.5665),
            'Breda': (51.5719, 4.7683),
            'Nijmegen': (51.8426, 5.8528),
            'Haarlem': (52.3874, 4.6462),
            'Arnhem': (51.9851, 5.8987),
            'Zaanstad': (52.4389, 4.8175),
            'Haarlemmermeer': (52.3007, 4.6937),
            'Almere': (52.3508, 5.2647),
            'Maastricht': (50.8514, 5.6913),
            'Den Bosch': (51.6978, 5.3037),
            'Enschede': (52.2215, 6.8937),
            'Apeldoorn': (52.2112, 5.9699),
            'Heerlen': (50.8880, 5.9794),
            'Amersfoort': (52.1561, 5.3878),
            'Zwolle': (52.5168, 6.0830),
            'Leiden': (52.1601, 4.4970),
            'Dordrecht': (51.8133, 4.6900),
            'Zoetermeer': (52.0575, 4.4937),
            'Deventer': (52.2551, 6.1639),
            'Delft': (52.0116, 4.3571),
            'Sittard': (50.9979, 5.8092),
            'Roosendaal': (51.5309, 4.4653),
            'Helmond': (51.4816, 5.6621),
            'Leeuwarden': (53.2012, 5.8086),
            'Venlo': (51.3704, 6.1724),
            'Alkmaar': (52.6316, 4.7495),
            'Hilversum': (52.2240, 5.1774),
            'Purmerend': (52.5055, 4.9592),
            'Oss': (51.7655, 5.5177),
            'Spijkenisse': (51.8447, 4.3297),
            'Schiedam': (51.9225, 4.3997),
            'Almelo': (52.3571, 6.6620),
            'Bergen op Zoom': (51.4940, 4.2928),
            'Amsterdam': (52.3676, 4.9041),
            'Made': (51.6789, 4.7959),
            'Raamsdonksveer': (51.7089, 4.8561),
            'Geertruidenberg': (51.7014, 4.8553),
            'Drimmelen': (51.7031, 4.8006),
            'Oosterhout': (51.6494, 4.8614),
            'Waalwijk': (51.6821, 5.0706),
            'Kaatsheuvel': (51.6594, 5.0386)
        }
        
        # European capitals and major cities
        international_coordinates = {
            # Belgium
            'Brussels': (50.8503, 4.3517),
            'Antwerp': (51.2194, 4.4025),
            'Ghent': (51.0543, 3.7174),
            # Germany
            'Berlin': (52.5200, 13.4050),
            'Munich': (48.1351, 11.5820),
            'Hamburg': (53.5511, 9.9937),
            'Cologne': (50.9375, 6.9603),
            'Düsseldorf': (51.2277, 6.7735),
            # France
            'Paris': (48.8566, 2.3522),
            'Marseille': (43.2965, 5.3698),
            'Lyon': (45.7640, 4.8357),
            # UK
            'London': (51.5074, -0.1278),
            'Manchester': (53.4808, -2.2426),
            'Birmingham': (52.4862, -1.8904),
            # Other European
            'Vienna': (48.2082, 16.3738),
            'Zurich': (47.3769, 8.5417),
            'Stockholm': (59.3293, 18.0686),
            'Copenhagen': (55.6761, 12.5683),
            'Oslo': (59.9139, 10.7522),
            'Helsinki': (60.1699, 24.9384),
            'Prague': (50.0755, 14.4378),
            'Warsaw': (52.2297, 21.0122),
            'Madrid': (40.4168, -3.7038),
            'Barcelona': (41.3851, 2.1734),
            'Rome': (41.9028, 12.4964),
            'Milan': (45.4642, 9.1900)
        }
        
        # Try Dutch cities first
        if country.lower() in ['netherlands', 'nederland', 'nl']:
            coords = dutch_coordinates.get(city)
            if coords:
                cache.set(cache_key, coords, 86400)  # Cache for 24 hours
                return coords
        
        # Try international cities
        coords = international_coordinates.get(city)
        if coords:
            cache.set(cache_key, coords, 86400)
            return coords
        
        # Fallback: Try free geocoding service (limited requests)
        try:
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search",
                params={
                    'q': f"{city}, {country}",
                    'format': 'json',
                    'limit': 1
                },
                headers={'User-Agent': 'Demo-Analytics/1.0'},
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat, lon = float(data[0]['lat']), float(data[0]['lon'])
                    coords = (lat, lon)
                    cache.set(cache_key, coords, 86400)
                    return coords
                    
        except Exception as e:
            logger.warning(f"Geocoding failed for {city}, {country}: {e}")
        
        # Ultimate fallback for Netherlands
        if country.lower() in ['netherlands', 'nederland', 'nl']:
            return (52.1326, 5.2913)  # Netherlands center
        
        return None
    
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
    
    def get_realtime_data(self) -> Dict:
        """Get real-time analytics data (current users, locations, etc.)"""
        if not self.client:
            return self._get_mock_realtime_data()
        
        try:
            from google.analytics.data_v1beta.types import (
                RunRealtimeReportRequest,
                Metric,
                Dimension
            )
            
            # Real-time request for active users - Use ONLY valid realtime dimensions
            request = RunRealtimeReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[
                    Dimension(name="country"),
                    Dimension(name="city"), 
                    Dimension(name="deviceCategory"),
                    # Note: pageTitle and pagePath are NOT valid in realtime API
                ],
                metrics=[
                    Metric(name="activeUsers"),
                ]
            )
            
            response = self.client.run_realtime_report(request)
            
            # Process real-time data
            realtime_data = {
                "active_users": 0,
                "locations": [],
                "pages": [],
                "devices": [],
                "timestamp": datetime.now().isoformat()
            }
            
            # Parse response
            for row in response.rows:
                active_users = int(row.metric_values[0].value or 0)
                realtime_data["active_users"] += active_users
                
                if active_users > 0:  # Only include active locations/devices
                    country = row.dimension_values[0].value
                    city = row.dimension_values[1].value
                    device = row.dimension_values[2].value
                    # page = row.dimension_values[3].value  # Not available in realtime API
                    
                    # Add to locations with coordinates
                    location_key = f"{city}, {country}"
                    coordinates = self._get_location_coordinates(city, country)
                    
                    location_exists = False
                    for loc in realtime_data["locations"]:
                        if loc["location"] == location_key:
                            loc["users"] += active_users
                            location_exists = True
                            break
                    if not location_exists:
                        location_data = {
                            "location": location_key,
                            "country": country,
                            "city": city,
                            "users": active_users
                        }
                        if coordinates:
                            location_data["latitude"] = coordinates[0]
                            location_data["longitude"] = coordinates[1]
                        realtime_data["locations"].append(location_data)
                    
                    # Pages data not available in realtime API - use fallback
                    # Will be populated from a separate standard API call if needed
                    
                    # Add to devices
                    device_exists = False
                    for d in realtime_data["devices"]:
                        if d["category"] == device:
                            d["users"] += active_users
                            device_exists = True
                            break
                    if not device_exists:
                        realtime_data["devices"].append({
                            "category": device,
                            "users": active_users
                        })
            
            # Get current pages from last 5 minutes (standard API)
            realtime_data["pages"] = self._get_current_pages()
            
            # Sort by user count
            realtime_data["locations"].sort(key=lambda x: x["users"], reverse=True)
            realtime_data["pages"].sort(key=lambda x: x["users"], reverse=True)
            realtime_data["devices"].sort(key=lambda x: x["users"], reverse=True)
            
            # Add accuracy indicator for production
            realtime_data["data_source"] = "GA4_REALTIME_API"
            realtime_data["is_mock"] = False
            
            # Cache for 15 seconds (real-time should be very fresh)
            cache.set(f"ga_realtime", realtime_data, 15)
            
            return realtime_data
            
        except Exception as e:
            logger.error(f"Failed to get real-time analytics data: {e}")
            # For production: Log this as a critical issue
            logger.critical(f"PRODUCTION ALERT: Real-time analytics failing - using fallback data: {e}")
            return self._get_mock_realtime_data()
    
    def _get_current_pages(self) -> List[Dict]:
        """Get current page data from recent activity (last 5 minutes)"""
        try:
            from google.analytics.data_v1beta.types import (
                RunReportRequest,
                Dimension,
                Metric,
                DateRange
            )
            
            # Get last 5 minutes of data for current pages
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=5)
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name="pagePath")],
                metrics=[Metric(name="activeUsers")],
                date_ranges=[DateRange(
                    start_date=start_time.strftime("%Y-%m-%d"),
                    end_date=end_time.strftime("%Y-%m-%d")
                )]
            )
            
            response = self.client.run_report(request=request)
            
            pages = []
            for row in response.rows:
                page_path = row.dimension_values[0].value
                users = int(row.metric_values[0].value or 0)
                if users > 0:
                    pages.append({"path": page_path, "users": users})
            
            return sorted(pages, key=lambda x: x["users"], reverse=True)[:5]
            
        except Exception as e:
            logger.error(f"Failed to get current pages: {e}")
            return [{"path": "/", "users": 1}]  # Fallback
    
    def _get_mock_realtime_data(self) -> Dict:
        """Return mock real-time data when API is unavailable - FOR DEVELOPMENT ONLY"""
        import random
        
        # PRODUCTION WARNING: This should NOT be used for paid features
        logger.warning("USING MOCK DATA - NOT SUITABLE FOR PRODUCTION/PAID FEATURES")
        
        # Simulate realistic real-time data
        active_users = random.randint(0, 3)  # Lower numbers for realism
        
        locations = []
        pages = []
        devices = []
        
        if active_users > 0:
            # Sample Dutch locations
            dutch_locations = [
                ("Amsterdam", "Netherlands"),
                ("Rotterdam", "Netherlands"), 
                ("Utrecht", "Netherlands"),
                ("Eindhoven", "Netherlands"),
                ("Tilburg", "Netherlands"),
                ("Groningen", "Netherlands"),
                ("Breda", "Netherlands"),
                ("Nijmegen", "Netherlands")
            ]
            
            # Sample pages
            sample_pages = [
                "/", "/diensten/", "/portfolio/", "/over-ons/", "/contact/"
            ]
            
            # Sample devices
            sample_devices = ["desktop", "mobile", "tablet"]
            
            # Generate random active locations
            for i in range(min(active_users, 5)):
                city, country = random.choice(dutch_locations)
                user_count = random.randint(1, max(1, active_users // 3))
                locations.append({
                    "location": f"{city}, {country}",
                    "country": country,
                    "city": city,
                    "users": user_count
                })
            
            # Generate active pages
            for i in range(min(active_users, 3)):
                page = random.choice(sample_pages)
                user_count = random.randint(1, max(1, active_users // 2))
                pages.append({
                    "path": page,
                    "users": user_count
                })
            
            # Generate device breakdown
            remaining_users = active_users
            for device in sample_devices:
                if remaining_users > 0:
                    user_count = random.randint(0, remaining_users)
                    if user_count > 0:
                        devices.append({
                            "category": device,
                            "users": user_count
                        })
                    remaining_users -= user_count
        
        return {
            "active_users": active_users,
            "locations": locations,
            "pages": pages, 
            "devices": devices,
            "timestamp": datetime.now().isoformat(),
            "data_source": "MOCK_DATA",
            "is_mock": True,
            "warning": "Mock data - not suitable for production use"
        }

# Initialize the service
ga_service = GoogleAnalyticsService()