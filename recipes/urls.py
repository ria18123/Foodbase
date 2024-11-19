from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Set the application namespace for URL namespacing
app_name = 'recipes'

# Define the URL patterns for the recipes app
urlpatterns = [
    path('', views.index, name='index'),  # Home page showing latest recipes
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Recipe detail page
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),  # Page to submit a new recipe
    path('service/<str:service_name>/', views.service_detail, name='service_detail'),  # Service detail page
    path('category/', views.category_list, name='category_list'),  # List of recipe categories
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # Category detail page
    path('register/', views.register, name='register'),  # User registration page
    path('login/', views.user_login, name='login'),  # User login page
    path('accounts/profile/', views.user_dashboard, name='user_dashboard'),  # User dashboard after login
    path('accounts/', include('django.contrib.auth.urls')),  # Includes built-in auth URLs for login/logout
    path('latest/', views.latest_recipes, name='latest_recipes'),  # Page showing the latest recipes
    path('search/', views.search_results, name='search_results'),  # Page for displaying search results
    path('profile/', views.profile_view, name='profile'),  # User profile page
    path('profile/edit/', views.profile_edit, name='edit_profile'),  # Page to edit user profile
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),  # Chat room page
    path('create-blog/', views.create_blog, name='create_blog'),  # Page to create a new blog post
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Blog detail page
    path('blog/', views.blog_home, name='blog_home'),  # Home page for blogs
    path("recipe-modifications/", views.recipe_modifications, name="recipe_modifications"),  # Page for recipe modifications
    path("personalized-recommendations/", views.personalized_recommendations, name="personalized_recommendations"),  # Page for personalized recommendations
]

# Serve media files during development
if settings.DEBUG:
    # Append static URL patterns for serving media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)