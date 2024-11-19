# Import TestCase for creating test cases
from django.test import TestCase
# Import User model for creating test users
from django.contrib.auth.models import User
# Import reverse for URL resolution
from django.urls import reverse
# Import Recipe model from recipes app
from recipes.models import Recipe
# Import IntegrityError for handling database integrity issues
from django.db.utils import IntegrityError

# Test case for the profile view
class ProfileViewTestCase(TestCase):
    # Set up method to create a test user and profile URL
    def setUp(self):
        # Create a test user with username and password
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Resolve the URL for the profile view
        self.profile_url = reverse('recipes:profile')

    # Test case for authenticated users accessing the profile view
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated users."""
        # Log in the test user
        self.client.login(username='testuser', password='testpass')
        # Make a GET request to the profile URL
        response = self.client.get(self.profile_url)
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the username
        self.assertContains(response, 'testuser')

    # Test case for unauthenticated users accessing the profile view
    def test_profile_view_unauthenticated(self):
        """Test profile view redirects unauthenticated users."""
        # Make a GET request to the profile URL without logging in
        response = self.client.get(self.profile_url)
        # Check that the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the response redirects to the login page
        self.assertRedirects(response, f'/accounts/login/?next={self.profile_url}')

# Test case for the search view
class SearchViewTestCase(TestCase):
    # Set up method to create the search URL
    def setUp(self):
        # Resolve the URL for the search results view
        self.search_url = reverse('recipes:search_results')

    # Test case for a valid search query
    def test_valid_search_query(self):
        """Test search results for a valid query."""
        # Make a GET request with a valid search query
        response = self.client.get(f'{self.search_url}?query=chicken')
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the expected search result message
        self.assertContains(response, 'Search Results for "chicken"')

    # Test case for an invalid search query
    def test_invalid_search_query(self):
        """Test search results for a malicious query."""
        # Make a GET request with a malicious search query
        response = self.client.get(f'{self.search_url}?query=<script>alert("test")</script>')
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response does not contain the malicious script
        self.assertNotContains(response, '<script>')
        # Check that the response contains a generic search result message
        self.assertContains(response, 'Search Results for')

    # Test case for an empty search query
    def test_empty_search_query(self):
        """Test search results for an empty query."""
        # Make a GET request with an empty search query
        response = self.client.get(f'{self.search_url}?query=')
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains a message indicating no results found
        self.assertContains(response, 'No results found.')

# Test case for the Recipe model
class RecipeModelTestCase(TestCase):
    # Test case for the string representation of the Recipe model
    def test_recipe_str(self):
        """Test string representation of the Recipe model."""
        # Create a test recipe
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='A delicious test recipe.',
            ingredients='1 cup flour, 2 eggs',
            instructions='Mix and bake.',
        )
        # Check that the string representation of the recipe is correct
        self.assertEqual(str(recipe), 'Test Recipe')

    # Test case for creating a recipe with all fields filled
    def test_create_recipe_with_all_fields(self):
        """Test creating a recipe with all fields filled."""
        # Create a recipe with all fields
        recipe = Recipe.objects.create(
            title='Complete Recipe',
            description='A recipe with all fields.',
            ingredients='1 cup flour, 2 eggs',
            instructions='Mix and bake.',
            calories=500,
            protein=10.5,
            fat=20.3,
            sodium=0.5,
            diet='vegetarian',
            spice_level='mild',
        )
        # Check that the recipe title is correct
        self.assertEqual(recipe.title, 'Complete Recipe')
        # Check that the recipe calories are correct
        self.assertEqual(recipe.calories, 500)

    # Test case for creating a recipe with missing required fields
    def test_invalid_recipe_missing_fields(self):
        """Test creating a recipe with missing required fields."""
        # Check that creating a recipe without a title raises an IntegrityError
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(title=None)

# Test case for the Recipe views
class RecipeViewsTestCase(TestCase):
    # Set up method to create a test recipe
    def setUp(self):
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test description",
            ingredients="Test ingredients",
            instructions="Test instructions"
        )

    # Test case for the recipe detail view
    def test_recipe_detail_view(self):
        """Test the detail view for a specific recipe."""
        # Make a GET request to the recipe detail view
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the recipe title
        self.assertContains(response, self.recipe.title)

    # Test case for the index view
    def test_index_view(self):
        """Test the index view displays recipes."""
        # Make a GET request to the index view
        response = self.client.get(reverse('recipes:index'))
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the test recipe title
        self.assertContains(response, "Test Recipe")