# Import the admin module from Django for creating admin interfaces
from django.contrib import admin
# Import path and include for URL routing
from django.urls import path, include
# Import settings for configuration
from django.conf import settings
# Import static for serving media files in development
from django.conf.urls.static import static
# Import Wagtail admin URLs for the CMS
from wagtail.admin import urls as wagtailadmin_urls
# Import Wagtail URLs for handling pages
from wagtail import urls as wagtail_urls
# Import Wagtail documents URLs for document management
from wagtail.documents import urls as wagtaildocs_urls

# Define the URL patterns for the project
urlpatterns = [
    path('cms/', include(wagtailadmin_urls)),  # Include Wagtail admin URLs under the 'cms/' path
    path('documents/', include(wagtaildocs_urls)),  # Include Wagtail document management URLs
    path('pages/', include(wagtail_urls)),  # Include Wagtail page URLs if you use them
    path('admin/', admin.site.urls),  # Include Django admin URLs under the 'admin/' path
    path('', include('recipes.urls', namespace='recipes')),  # Include all recipes URLs here
    path('accounts/', include('django.contrib.auth.urls')),  # Adds built-in authentication URLs (login, logout, etc.)
    path('social-auth/', include('social_django.urls', namespace='social')),  # Include social authentication URLs
]

# Serve media files during development if DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Append static URL patterns for media files