#!/bin/bash
# deploy_production.sh - Deploy to main production domain

set -e  # Exit on any error

echo "🚀 Deploying HMD to Production Environment..."

# Configuration
PRODUCTION_HOST="hmdklusbedrijf.nl"
PROJECT_DIR="/path/to/hmd"  # Update this path
PYTHON_PATH="python3"       # or full path to Python

# Safety check
echo "⚠️  WARNING: This will deploy to PRODUCTION!"
echo "🌐 Domain: $PRODUCTION_HOST"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled."
    exit 1
fi

echo "📦 Installing dependencies..."
$PYTHON_PATH -m pip install -r requirements.txt

echo "🗃️  Running database migrations..."
$PYTHON_PATH manage.py migrate

echo "📁 Collecting static files..."
$PYTHON_PATH manage.py collectstatic --noinput

echo "🔍 Running deployment checks..."
$PYTHON_PATH manage.py check --deploy

echo "🔄 Restarting web server (if applicable)..."
# Uncomment and modify based on your server setup:
# sudo systemctl restart apache2
# sudo systemctl restart nginx
# sudo systemctl restart gunicorn

echo "✅ Production deployment complete!"
echo "🌐 Site should be available at: https://$PRODUCTION_HOST"
echo ""
echo "🎉 Your HMD website is now live in production!"
echo "📊 Monitor the following:"
echo "  - Server logs for any errors"
echo "  - Site performance and loading times"
echo "  - All functionality works as expected"