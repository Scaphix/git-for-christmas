#!/usr/bin/env bash
# Build script for Render deployment
# This script runs migrations, collects static files, and creates the admin user

set -o errexit  # Exit on error

echo "Starting build process..."

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create admin user if it doesn't exist
echo "Creating admin user..."
python create_admin.py

echo "Build completed successfully!"

