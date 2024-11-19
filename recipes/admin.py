# Import the admin module from Django for creating admin interfaces
from django.contrib import admin
# Import Recipe, Blog, and Category models from the current app's models
from .models import Recipe, Blog, Category  # Import Category model

# Register the Recipe model with the admin site
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin
    list_display = ('title', 'category', 'created_at', 'ratings')  # Add 'ratings' here
    # Specify the fields to be searchable in the admin interface
    search_fields = ('title', 'description')
    # Specify the fields to filter by in the admin interface
    list_filter = ('category', 'ratings')  # Optional: Allow filtering by ratings

# Register the Blog model with the admin site
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin
    list_display = ('title', 'created_at', 'updated_at')  # Removed 'author'
    # Specify the fields to be searchable in the admin interface
    search_fields = ('title', 'content')
    # Specify the fields to filter by in the admin interface
    list_filter = ('created_at',)  # Removed 'author'
    # Specify the default ordering of the list view
    ordering = ('-created_at',)  # Order by created_at in descending order

# Register the Category model with the admin site
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of the admin
    list_display = ('name',)  # Display the category name
    # Specify the fields to be searchable in the admin interface
    search_fields = ('name',)  # Allow searching by category name