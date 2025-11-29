# env.py
# This file is used to store sensitive information like secrets and environment variables.

import os

# Example: Replace these with your actual secrets

# Django Secret Key
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-#dw6p-_(fs%5$84ps8xeulipjtgb141aij3pk1&a@4@de+8m$d")

# Database password
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "your-default-db-password")

# Add other secrets or environment variables as needed