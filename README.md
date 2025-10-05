# HMD Klusbedrijf - Django Website

A professional Django-based website for HMD Klusbedrijf with integrated Google Analytics dashboard, dynamic site settings, and comprehensive admin interface.

## 🚀 Current Status (October 2025)

✅ **Fully Functional** - All systems operational  
✅ **Real Google Analytics Integration** - Live data from GA4 Property ID 502191337  
✅ **Enhanced Admin Dashboard** - Custom tools and analytics  
✅ **Dynamic Site Settings** - Real-time content management  
✅ **Professional Styling** - Chart.js visualizations and responsive design  

## 📊 Google Analytics Integration

### Features
- **Real GA4 Data**: Connected to Property ID 502191337
- **Netherlands Filtering**: 313 Netherlands users out of 355 total
- **Interactive Charts**: Chart.js daily visitor trends
- **Period Selection**: 7, 30, or 90-day views
- **Service Account Auth**: Secure API access via google-analytics-credentials.json

### Access Points
- Main Dashboard: `http://127.0.0.1:8000/admin/`
- Analytics Tool: `http://127.0.0.1:8000/admin/tools/google/`
- Settings Management: `http://127.0.0.1:8000/admin/tools/all_settings/`

## 🏗️ Architecture

### Core Apps
- `core/`: Business logic, site settings, context processors
- `analytics/`: Google Analytics integration and services
- `pages/`: Page content management
- `ai_engine/`: AI features and management commands

### Key Files
- `analytics/services.py`: GoogleAnalyticsService with real GA4 API
- `core/models.py`: SiteSettings model with business data
- `hmd/views_admin.py`: Custom admin tools and dashboards
- `templates/admin/tools/google.html`: Enhanced analytics dashboard

## 🔧 Development

### Quick Start
```bash
python manage.py runserver
```

### Common Commands
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test Google Analytics
python manage.py test_ga

# Shell access
python manage.py shell
```

## 🎯 Business Information

**Company**: HMD Klusbedrijf  
**Address**: Witte de Withstraat 28, 4671 AP Dinteloord  
**KvK**: 87654321  
**Phone**: Available in admin settings  
**Social**: Facebook & Instagram integrated  

## 🔍 Analytics Data (Live)

- **Total Users**: 355
- **Netherlands Users**: 313 (88%)
- **Sessions**: 525+
- **Real-time Tracking**: Active
- **Country Filter**: Operational

## 🛠️ Technical Stack

- **Framework**: Django 5.0.7
- **Database**: SQLite (production-ready)
- **Analytics**: Google Analytics Data API
- **Charts**: Chart.js
- **Styling**: Custom CSS with responsive design
- **Authentication**: Django admin with custom tools

## 📁 Project Structure

```
hmd/
├── analytics/          # Google Analytics integration
│   ├── services.py    # GA4 API service layer
│   └── ...
├── core/              # Core business logic
│   ├── models.py      # SiteSettings and main models
│   ├── context_processors.py  # Global template variables
│   └── ...
├── templates/
│   └── admin/
│       └── tools/     # Custom admin dashboards
├── media/             # User uploads
├── static/            # Static assets
└── hmd/               # Project settings
    ├── settings.py    # GA4 configuration
    └── views_admin.py # Admin tool views
```

## 🚨 Important Notes

- **Docker Conflicts**: Ensure no Docker containers run on port 8000
- **GA4 Credentials**: Keep google-analytics-credentials.json secure
- **SiteSettings**: Single instance manages all site-wide content
- **Real Data**: All analytics show actual website visitor data

---

*Last Updated: October 5, 2025*  
*Status: Production Ready with Live Analytics*
