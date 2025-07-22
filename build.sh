#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print each command as it runs
set -x

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
echo "==> Running Django migrations..."
python manage.py migrate
echo "==> Django migrations complete."