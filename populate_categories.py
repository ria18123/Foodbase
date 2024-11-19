import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodbites.settings')
django.setup()

from recipes.models import Category

categories = ['Appetizers', 'Main Courses', 'Desserts', 'Drinks']
for category_name in categories:
    Category.objects.get_or_create(name=category_name)
