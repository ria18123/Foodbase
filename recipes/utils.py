# Import Q for complex queries and the Recipe and Blog models
from django.db.models import Q
from .models import Recipe, Blog

# Function to get recipe suggestions for a user
def get_recipe_suggestions(user, limit=5):
    """
    Fetch recipe suggestions based on user preferences, favorites, or recent activity.
    """
    # Return the most recently created recipes, limited to the specified number
    return Recipe.objects.order_by('-created_at')[:limit]

# Function to get blog suggestions based on a given blog
def get_blog_suggestions(blog, limit=5):
    """
    Fetch similar blogs based on the tags or related attributes.
    """
    # Check if the Blog object has tags and handle the case if tags are missing or empty
    if not hasattr(blog, 'tags') or not blog.tags.exists():
        # If no tags exist, return blogs excluding the current blog, ordered by creation date
        return Blog.objects.exclude(id=blog.id).order_by('-created_at')[:limit]

    # Fetch blogs with similar tags, excluding the current blog
    return Blog.objects.filter(
        Q(tags__in=blog.tags.all())  # Filter blogs that have any of the current blog's tags
    ).exclude(id=blog.id).distinct()[:limit]  # Exclude the current blog and ensure distinct results