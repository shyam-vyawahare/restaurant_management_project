#!/usr/bin/env python
"""Create admin superuser if it doesn't exist"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_management.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
email = 'admin@restaurant.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f'User "{username}" already exists. Updating password...')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f'✓ Password updated for user "{username}"')
else:
    User.objects.create_superuser(username, email, password)
    print(f'✓ Superuser "{username}" created successfully!')

print(f'\nAdmin Login Credentials:')
print(f'  Username: {username}')
print(f'  Password: {password}')
print(f'  URL: http://127.0.0.1:8000/admin/')

