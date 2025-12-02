#!/usr/bin/env python
"""
Script to create a superuser for the Django admin panel.
Run this after migrations on deployment.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gitforchristmas.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment variables or use defaults
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme123')

# Check if superuser already exists
if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists. Skipping creation.")
else:
    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"   Email: {email}")
        print(f"   Password: {'*' * len(password)}")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

