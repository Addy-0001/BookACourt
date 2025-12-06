#!/bin/bash

# BookACourt Authentication Setup Script
# This script helps set up the authentication system

echo "🚀 BookACourt Authentication Setup"
echo "===================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not detected!"
    echo "Please activate your virtual environment first:"
    echo "source env/bin/activate"
    exit 1
fi

echo "✓ Virtual environment detected"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python -c "import allauth" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✓ Dependencies already installed"
fi
echo ""

# Remove old migrations if requested
read -p "Do you want to remove old migrations? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing old migrations..."
    find . -path "*/migrations/*.py" -not -name "__init__.py" -type f -delete
    find . -path "*/migrations/*.pyc" -type f -delete
    echo "✓ Old migrations removed"
fi
echo ""

# Check database connection
echo "🔍 Checking database connection..."
if python manage.py check --database default 2>/dev/null; then
    echo "✓ Database connection successful"
else
    echo "❌ Database connection failed!"
    echo "Please check your database settings in .env file"
    exit 1
fi
echo ""

# Run makemigrations
echo "📝 Creating migrations..."
if python manage.py makemigrations; then
    echo "✓ Migrations created successfully"
else
    echo "❌ Failed to create migrations"
    exit 1
fi
echo ""

# Run migrate
echo "📊 Applying migrations..."
if python manage.py migrate; then
    echo "✓ Migrations applied successfully"
else
    echo "❌ Failed to apply migrations"
    exit 1
fi
echo ""

# Create superuser
read -p "Do you want to create a superuser? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "👤 Creating superuser..."
    echo "Please provide the following information:"
    python manage.py createsuperuser
fi
echo ""

echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Run the server: python manage.py runserver"
echo "2. Visit API docs: http://localhost:8000/api/docs/"
echo "3. Visit Admin panel: http://localhost:8000/admin/"
echo ""