# Copilot Instructions for AI Coding Agents

## Project Overview
This is a **production-ready Django web application** for HMD Klusbedrijf with **real Google Analytics integration**. The application features a comprehensive admin dashboard with live GA4 data, dynamic site settings, and professional analytics visualizations.

### Current Status (October 2025)
- ✅ **Fully Operational**: All systems working correctly
- ✅ **Live Analytics**: Real GA4 data (355 users, 313 from Netherlands)
- ✅ **Enhanced Admin**: Custom dashboards with Chart.js integration
- ✅ **Dynamic Content**: SiteSettings model manages all site-wide content
- ✅ **Professional UI**: Responsive design with interactive charts

### Core Components
- `hmd/`: Project settings, URLs, **custom admin views** (`views_admin.py`)
- `core/`: Business logic, **SiteSettings model**, context processors
- `analytics/`: **Google Analytics integration** with real GA4 API service
- `pages/`: Page content management
- `ai_engine/`: AI features and management commands
- `media/`: User uploads organized by feature (portfolio, slider, etc.)
- `static/`: Static assets (CSS, JS, images)
- `templates/`: HTML templates including **enhanced admin dashboards**

## Architecture & Data Flow
- **Real-time Analytics**: `analytics/services.py` → GA4 API → Dashboard visualization
- **Dynamic Settings**: `core/models.SiteSettings` → Context processors → All templates
- **Admin Tools**: Custom dashboards in `hmd/views_admin.py` → `templates/admin/tools/`
- **Data Integration**: Live GA4 data with Netherlands filtering and Chart.js visualization
- Each app follows Django patterns but with **enhanced admin functionality**
- Static and media files served separately; media for uploads, static for assets

## Developer Workflows
- **Run server:** `python manage.py runserver`
- **Apply migrations:** `python manage.py migrate`
- **Create migrations:** `python manage.py makemigrations <appname>`
- **Run tests:** `python manage.py test <appname>`
- **Debug:** Use Django's built-in error pages and logging in `settings.py`.

## Google Analytics Integration (CRITICAL - October 2025)
### WORKING FEATURES ✅
- **Real GA4 API**: Property ID 502191337 with live data (355 users, 313 Netherlands)
- **Service Account Auth**: `google-analytics-credentials.json` (keep secure!)
- **Netherlands Filtering**: 88% of users from Netherlands (313/355)
- **Interactive Charts**: Chart.js daily trends with period selection (7/30/90 days)
- **Enhanced Dashboard**: Professional styling with responsive design

### Key Analytics Files
- `analytics/services.py`: **GoogleAnalyticsService** - Core GA4 integration
- `templates/admin/tools/google.html`: Enhanced dashboard with Chart.js
- `hmd/views_admin.py`: Admin tools including `admin_tool` function
- `hmd/settings.py`: GA4_PROPERTY_ID = 502191337

### Analytics Access Points
- Main Dashboard: `/admin/` (custom index with analytics widgets)
- Google Analytics Tool: `/admin/tools/google/` (full dashboard)
- Settings Management: `/admin/tools/all_settings/` (dynamic site settings)

## Project-Specific Conventions
### ENHANCED ADMIN SYSTEM 🎯
- **Custom Admin Tools**: `hmd/views_admin.py` with real-time analytics
- **Dynamic Site Settings**: Single `SiteSettings` instance manages all content
- **Context Processors**: `core/context_processors.py` injects site-wide variables
- **Enhanced Templates**: `templates/admin/tools/` for custom dashboards
- **Business Data**: KvK, address, phone, social media URLs in SiteSettings

### WORKING INTEGRATIONS 🔗
- **Google Analytics 4**: Real data via `analytics/services.py`
- **Facebook API**: Legacy integration in `core/facebook_api.py` 
- **Chart.js**: Interactive visualizations in admin dashboard
- **Context System**: Global template variables via context processors

## Technical Dependencies & Configuration
### CURRENT WORKING SETUP ✅
- **Database**: SQLite (`db.sqlite3`) - production ready
- **Python**: 3.11 with virtual environment at `.venv/`
- **Django**: 5.0.7 with custom admin extensions
- **Google Analytics**: google-analytics-data package with service account
- **Charts**: Chart.js for interactive data visualization

### Critical Configuration
- `GA4_PROPERTY_ID = 502191337` in `hmd/settings.py`
- `google-analytics-credentials.json` - service account file (secure)
- `SiteSettings` model - single instance ID=1 for all site content
- Custom admin URLs in `hmd/urls.py` for tools

## Development Patterns & Examples
### GOOGLE ANALYTICS INTEGRATION 📊
```python
# analytics/services.py - Real GA4 service
from analytics.services import ga_service
data = ga_service.get_overview_data()  # Real data: 355 users
chart_data = ga_service.get_chart_data()  # Daily trends

# Custom admin view - hmd/views_admin.py
def admin_tool(request):
    # Real analytics dashboard with filtering
```

### SITE SETTINGS SYSTEM 🏢
```python
# core/models.py - Dynamic content management
class SiteSettings(models.Model):
    business_name = models.CharField(max_length=200, default="HMD Klusbedrijf")
    kvk_number = models.CharField(max_length=20, default="87654321")
    # ... all business data in single model
```

### CONTEXT PROCESSORS 🌐
```python
# core/context_processors.py - Global template variables
def site_constants(request):
    # Injects SiteSettings into all templates
```

## Key Files & Critical Locations
### MUST-KNOW FILES 🔥
- `analytics/services.py`: **GoogleAnalyticsService** (real GA4 integration)
- `core/models.py`: **SiteSettings** model (all business data)
- `hmd/views_admin.py`: **admin_tool** function (main dashboard)
- `templates/admin/tools/google.html`: Enhanced analytics dashboard
- `google-analytics-credentials.json`: GA4 service account (SECURE!)

### WORKING DIRECTORIES 📁
- `analytics/`: Google Analytics integration (NEW - October 2025)
- `core/`: Business logic and SiteSettings
- `templates/admin/tools/`: Custom admin dashboards
- `hmd/`: Project settings with GA4 configuration
- `media/`, `static/`: Assets (standard Django)

## TROUBLESHOOTING & COMMON ISSUES 🚨

### Docker Conflicts (CRITICAL)
- **Problem**: Docker containers override Django server on port 8000
- **Solution**: `docker stop $(docker ps -q)` then `python manage.py runserver`
- **Check**: `netstat -ano | findstr :8000` to verify port is free

### Google Analytics Issues
- **Problem**: "Mock data" instead of real data
- **Solution**: Verify `google-analytics-credentials.json` exists and GA4_PROPERTY_ID=502191337
- **Test**: `python manage.py test_ga` should show real user count

### SiteSettings Problems  
- **Problem**: Template variables not showing
- **Solution**: Ensure SiteSettings instance exists: `SiteSettings.objects.get_or_create(id=1)`
- **Context**: Check `core/context_processors.py` is in TEMPLATES settings

### Migration Conflicts
- **Problem**: Migration errors on startup
- **Solution**: Delete problematic migrations, recreate with `makemigrations core`
- **Safe Reset**: Use `git reset --hard` to known working commit

## AI AGENT GUIDANCE 🤖

### CRITICAL SUCCESS FACTORS ✅
1. **ALWAYS verify Google Analytics is working** - Real data (355 users) not mock data
2. **PRESERVE the SiteSettings model** - Single source for all business content
3. **MAINTAIN custom admin tools** - `/admin/tools/google/` dashboard functionality
4. **CHECK for Docker conflicts** - Port 8000 must be free for Django
5. **VALIDATE Chart.js integration** - Interactive charts should load properly

### DEVELOPMENT WORKFLOW 🔄
```bash
# Standard startup sequence
python manage.py migrate          # Apply any pending migrations
python manage.py runserver        # Start development server
# Visit: http://127.0.0.1:8000/admin/tools/google/
```

### FILE EDITING PRIORITIES 📝
1. **NEVER break** `analytics/services.py` - Real GA4 integration
2. **PRESERVE** `core/models.py` SiteSettings structure  
3. **MAINTAIN** `hmd/views_admin.py` admin_tool function
4. **KEEP** enhanced admin templates in `templates/admin/tools/`
5. **PROTECT** `google-analytics-credentials.json` (add to .gitignore)

### TESTING & VALIDATION 🧪
```python
# Verify Google Analytics
python manage.py test_ga

# Check SiteSettings
python manage.py shell -c "from core.models import SiteSettings; print(SiteSettings.objects.first().business_name)"

# Test admin tools
# Visit /admin/tools/google/ - should show real data with charts
```

### WHEN THINGS GO WRONG 💥
1. **Complete failure**: Check Docker conflicts first (`docker ps`)
2. **No analytics data**: Verify credentials and Property ID 502191337
3. **Template errors**: Ensure SiteSettings exists and context processors working
4. **Admin broken**: Check `hmd/views_admin.py` and URL routing
5. **Charts not loading**: Verify Chart.js CDN and data structure

### SUCCESS INDICATORS 🎯
- ✅ Real analytics data: 355 users (not mock data)
- ✅ Netherlands filtering: 313 users (88%)
- ✅ Interactive charts loading with Chart.js
- ✅ SiteSettings form working in `/admin/tools/all_settings/`
- ✅ Custom admin dashboard accessible at `/admin/tools/google/`

---

**REMEMBER**: This is a PRODUCTION system with REAL Google Analytics data. Preserve functionality and always test changes thoroughly. The user has invested significant time in getting this working perfectly.

*Last Updated: October 5, 2025 - Status: Fully Operational*
