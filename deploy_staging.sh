#!/bin/bash
# deployment_staging.sh - Deploy to staging subdomain

set -e  # Exit on any error

echo "🚀 Deploying HMD to Staging Environment..."

# Configuration
STAGING_HOST="test3.hmdklusbedrijf.nl"
PROJECT_DIR="/path/to/hmd"  # Update this path
PYTHON_PATH="python3"       # or full path to Python

echo "📦 Installing dependencies..."
$PYTHON_PATH -m pip install -r requirements.txt

echo "🗃️  Running database migrations..."
$PYTHON_PATH manage.py migrate

echo "📁 Collecting static files..."
$PYTHON_PATH manage.py collectstatic --noinput

echo "🔍 Running deployment checks..."
$PYTHON_PATH manage.py check --deploy

echo "✅ Staging deployment complete!"
echo "🌐 Site should be available at: https://$STAGING_HOST"
echo ""
echo "🧪 Test the following before moving to production:"
echo "  - Admin interface: https://$STAGING_HOST/admin/"
echo "  - Homepage and all pages load correctly"
echo "  - Static files (CSS/JS/images) load properly"
echo "  - Contact forms work"
echo "  - All admin tools function correctly"