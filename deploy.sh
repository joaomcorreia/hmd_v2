#!/bin/bash
echo "🚀 Starting Django deployment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run Django management commands
echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Set permissions
chmod +x manage.py
find . -type f -name "*.py" -exec chmod +x {} \;
chmod -R 755 staticfiles/ 2>/dev/null || true
chmod -R 755 media/ 2>/dev/null || true

echo "✅ Django deployment completed successfully!"
echo "🌐 Your site should be available at: https://test3.hmdklusbedrijf.nl"