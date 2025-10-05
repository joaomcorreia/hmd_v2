# analytics/management/commands/test_ga.py
from django.core.management.base import BaseCommand
from analytics.services import ga_service


class Command(BaseCommand):
    help = 'Test Google Analytics connection and display sample data'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Testing Google Analytics connection...")
        
        try:
            data = ga_service.get_overview_data(days=7)
            
            if "Mock Data" in data.get('period', ''):
                self.stdout.write(
                    self.style.WARNING("⚠️  Using mock data - Google Analytics not configured")
                )
                self.stdout.write("📋 To set up real analytics, see: GOOGLE_ANALYTICS_SETUP.md")
            else:
                self.stdout.write(
                    self.style.SUCCESS("✅ Google Analytics connected successfully!")
                )
                
            self.stdout.write(f"\n📊 Analytics Summary ({data['period']}):")
            self.stdout.write(f"   👥 Users: {data['overview']['total_users']:,}")
            self.stdout.write(f"   📈 Sessions: {data['overview']['total_sessions']:,}")
            self.stdout.write(f"   📄 Page Views: {data['overview']['total_pageviews']:,}")
            self.stdout.write(f"   ⚡ Bounce Rate: {data['overview']['bounce_rate']}%")
            
            if data.get('top_pages'):
                self.stdout.write(f"\n🏆 Top Pages:")
                for page in data['top_pages'][:3]:
                    self.stdout.write(f"   • {page['page']} - {page['views']:,} views")
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error connecting to Google Analytics: {e}")
            )
            self.stdout.write("📋 Check your configuration in GOOGLE_ANALYTICS_SETUP.md")