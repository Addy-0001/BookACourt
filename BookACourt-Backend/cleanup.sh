#!/bin/bash

# cleanup.sh
# Usage: ./cleanup.sh
# WARNING: This will delete your database and all migration history!

echo "⚠️  WARNING: This will delete your database and all migration history!"
read -p "Are you sure you want to continue? (y/n): " confirm

if [[ $confirm != "y" ]]; then
    echo "Aborting..."
    exit 0
fi

echo "🧹 Cleaning up old migrations and __pycache__..."

# Delete __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Delete old migrations (except __init__.py)
find . -path "*/migrations/*.py" ! -name "__init__.py" -delete

# Delete old migration folders' __pycache__
find . -path "*/migrations/__pycache__" -exec rm -rf {} +

# Remove SQLite database
if [ -f "db.sqlite3" ]; then
    echo "🗑 Deleting old database..."
    rm db.sqlite3
fi

# Make new migrations
echo "📦 Creating new initial migrations..."
python manage.py makemigrations

# Apply migrations
echo "🚀 Applying migrations..."
python manage.py migrate

# Optional: Create a superuser
echo "🧑 Creating superuser..."
python manage.py createsuperuser

echo "✅ Cleanup complete. Project database is now reset."
