# Cleans Database details
#!/bin/bash

echo "🔍 Searching for Django migration files..."

# Find all migration files except __init__.py and delete them
find . -path "*/migrations/*.py" ! -name "__init__.py" -type f -print -delete

# Delete compiled Python files (.pyc)
find . -path "*/migrations/*.pyc" -type f -print -delete

echo "✅ All migration files deleted (except __init__.py)."
