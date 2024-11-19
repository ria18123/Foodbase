# Consolidate repetitive imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Category, Blog, Review, UserProfile
from .forms import RecipeForm, BlogForm, ReviewForm, UserProfileForm
from .utils import get_recipe_suggestions, get_blog_suggestions
from django.db.models import Avg, FloatField
from django.contrib.auth import get_backends
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import Coalesce
from django.db.models import Q


def recipe_modifications(request):
    # This function handles the request for the recipe modifications page.

    return render(request, "recipes/recipe_modifications.html")
    # This line renders the 'recipe_modifications.html' template and returns the response.


def personalized_recommendations(request):
    # This function handles personalized recipe recommendations based on user input.

    if request.method == 'POST':
        # Check if the request method is POST, indicating form submission.

        filters = Q()
        # Initialize an empty Q object to build dynamic query filters.

        # Get form inputs
        diet = request.POST.get('diet')
        # Retrieve the 'diet' input from the submitted form data.

        cuisine = request.POST.get('cuisine')
        # Retrieve the 'cuisine' input from the submitted form data.

        spice_level = request.POST.get('spice_level')
        # Retrieve the 'spice_level' input from the submitted form data.

        ingredients = request.POST.get('ingredients')
        # Retrieve the 'ingredients' input from the submitted form data.

        allergies = request.POST.get('allergies')
        # Retrieve the 'allergies' input from the submitted form data.

        # Add filters dynamically
        if diet:
            filters &= Q(diet__iexact=diet)  # Match diet exactly (case-insensitive)

        if cuisine:
            filters &= Q(cuisine__icontains=cuisine)  # Partial match for cuisine

        if spice_level:
            filters &= Q(spice_level__iexact=spice_level)  # Exact match for spice level

        if ingredients:
            # Match any of the given ingredients
            included_ingredients = [ing.strip() for ing in ingredients.split(',') if ing.strip()]
            # Split the ingredients by comma, strip whitespace, and filter out empty strings.

            for ing in included_ingredients:
                filters &= Q(ingredients__icontains=ing)  # Partial match for each ingredient

        if allergies:
            # Exclude recipes containing allergens
            excluded_allergens = [allergen.strip() for allergen in allergies.split(',') if allergen.strip()]
            # Split the allergies by comma, strip whitespace, and filter out empty strings.

            for allergen in excluded_allergens:
                filters &= ~Q(ingredients__icontains=allergen)  # Exclude recipes with allergens

        # Get filtered recipes
        recipes = Recipe.objects.filter(filters).distinct()
        # Query the Recipe model using the constructed filters and get distinct results.

        return render(request, 'recipes/recommendations.html', {'recipes': recipes})
        # Render the 'recommendations.html' template with the filtered recipes.

    return render(request, 'recipes/personalized_form.html')
    # If the request method is not POST, render the 'personalized_form.html' template.


def register(request):
    # This function handles user registration.

    if request.method == 'POST':
        # Check if the request method is POST, indicating form submission.

        form = UserCreationForm(request.POST)
        # Create an instance of UserCreationForm with the submitted data.

        if form.is_valid():
            # Check if the form data is valid.

            user = form.save()
            # Save the new user to the database.

            # Attaching the backend manually here
            backend = get_backends()[0]  # Get the first authentication backend from the list.

            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            # Set the backend attribute of the user to the module and class name of the authentication backend.

            login(request, user)  # Log the user in directly after registration.

            messages.success(request, 'Registration successful!')
            # Add a success message to be displayed to the user.

            return redirect('login')
            # Redirect the user to the login page after successful registration.

        else:
            messages.error(request, 'Please correct the error below.')
            # If the form is not valid, add an error message to be displayed.

    else:
        form = UserCreationForm()
        # If the request method is not POST, create a new empty UserCreationForm.

    return render(request, 'registration/register.html', {'form': form})
    # Render the 'register.html' template with the form (either filled with errors or empty).


@login_required
# This decorator ensures that only authenticated users can access the profile_view function.

def profile_view(request):
    # This function handles the display and update of the user's profile.

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Retrieve the UserProfile for the currently logged-in user, creating one if it doesn't exist.

    # Handle POST request for profile updates
    if request.method == 'POST':
        # Check if the request method is POST, indicating a form submission for profile updates.

        user_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        # Create an instance of UserProfileForm with the submitted data and the existing profile instance.

        request.user.first_name = request.POST.get('first_name')
        # Update the user's first name with the submitted data.

        request.user.last_name = request.POST.get('last_name')
        # Update the user's last name with the submitted data.

        request.user.email = request.POST.get('email')
        # Update the user's email with the submitted data.

        request.user.save()
        # Save the updated user information to the database.

        if user_form.is_valid():
            # Check if the user_form data is valid.

            user_form.save()
            # Save the updated UserProfile information to the database.

            messages.success(request, 'Profile updated successfully.')
            # Add a success message to be displayed to the user.

            return redirect('recipes:profile')
            # Redirect the user to the profile page after successful update.

    else:
        user_form = UserProfileForm(instance=profile)
        # If the request method is not POST, create a UserProfileForm instance with the existing profile data.

    # Fetch recipe suggestions
    suggestions = get_recipe_suggestions(user=request.user)
    # Call a function to get recipe suggestions based on the current user.

    return render(request, 'recipes/profile_view.html', {
        # Render the 'profile_view.html' template with the context data.
        'form': user_form,  # Pass the user form to the template.
        'profile': profile,  # Pass the user profile to the template.
        'suggestions': suggestions,  # Pass the recipe suggestions to the template.
    })

# Profile Edit View
# This comment indicates that the following function is responsible for editing user profiles.

@login_required
# This decorator ensures that only authenticated users can access the profile_edit function.

def profile_edit(request):
    # This function handles the editing of the user's profile.

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Retrieve the UserProfile for the currently logged-in user, creating one if it doesn't exist.

    if request.method == 'POST':
        # Check if the request method is POST, indicating a form submission for profile updates.

        user_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        # Create an instance of UserProfileForm with the submitted data and the existing profile instance.

        request.user.first_name = request.POST.get('first_name')
        # Update the user's first name with the submitted data.

        request.user.last_name = request.POST.get('last_name')
        # Update the user's last name with the submitted data.

        request.user.email = request.POST.get('email')
        # Update the user's email with the submitted data.

        request.user.save()
        # Save the updated user information to the database.

        if user_form.is_valid():
            # Check if the user_form data is valid.

            user_form.save()
            # Save the updated UserProfile information to the database.

            messages.success(request, 'Profile updated successfully.')
            # Add a success message to be displayed to the user.

            return redirect('recipes:profile')
            # Redirect the user to the profile page after successful update.

    else:
        user_form = UserProfileForm(instance=profile)
        # If the request method is not POST, create a UserProfileForm instance with the existing profile data.

    return render(request, 'recipes/profile_edit.html', {
        # Render the 'profile_edit.html' template with the context data.
        'form': user_form,  # Pass the user form to the template.
        'profile': profile,  # Pass the user profile to the template.
    })


# Index
# This comment indicates that the following function is responsible for the index page of the application.

def index(request):
    # This function handles the request for the index page.

    recipes = Recipe.objects.order_by('-created_at')[:5]  # Fetch the latest 5 recipes
    # Query the Recipe model to get the latest 5 recipes, ordered by creation date in descending order.

    return render(request, 'recipes/index.html', {'recipes': recipes})
    # Render the 'index.html' template and pass the fetched recipes to the template context.

# Category List
# This comment indicates that the following function is responsible for displaying the list of categories.

def category_list(request):
    # This function handles the request for the category list page.

    categories = Category.objects.all()
    # Query the Category model to retrieve all categories.

    return render(request, 'recipes/category_list.html', {'categories': categories})
    # Render the 'category_list.html' template and pass the fetched categories to the template context.



def category_detail(request, category_id):
    # This function handles the request for the details of a specific category, identified by category_id.

    category = get_object_or_404(Category, id=category_id)
    # Retrieve the Category object with the given category_id, or return a 404 error if not found.

    recipes = Recipe.objects.filter(category=category)
    # Query the Recipe model to get all recipes that belong to the specified category.

    # Tag filtering
    tag = request.GET.get('tag')
    # Retrieve the 'tag' parameter from the GET request, if provided.

    if tag:
        # If a tag is specified, filter the recipes by the tag name.
        recipes = recipes.filter(tags__name__icontains=tag)

    # Tags list for filtering options
    tags = [
        "breakfast", "lunch", "dinner", "appetizer", "salad",
        "main-course", "side-dish", "baked-goods", "dessert",
        "snack", "soup", "holiday", "vegetarian"
    ]
    # Define a list of tags that can be used as filtering options for recipes.

    # Pagination logic
    paginator = Paginator(recipes, 10)  # 10 recipes per page
    # Create a Paginator object to paginate the recipes, with 10 recipes per page.

    page = request.GET.get('page')
    # Retrieve the 'page' parameter from the GET request to determine which page of results to display.

    try:
        paginated_recipes = paginator.page(page)
        # Attempt to get the recipes for the specified page.
    except PageNotAnInteger:
        paginated_recipes = paginator.page(1)
        # If the page parameter is not an integer, default to the first page.
    except EmptyPage:
        paginated_recipes = paginator.page(paginator.num_pages)
        # If the page parameter is out of range, return the last page of results.

    return render(request, 'recipes/category_detail.html', {
        # Render the 'category_detail.html' template with the context data.
        'category': category,  # Pass the category object to the template.
        'recipes': paginated_recipes,  # Pass the paginated recipes to the template.
        'tags': tags,  # Pass the list of tags to the template for filtering options.
    })


def search_results(request):
    # This function handles the search results for recipes based on a query parameter.

    query = request.GET.get('query', '')
    # Retrieve the 'query' parameter from the GET request; default to an empty string if not provided.

    results = Recipe.objects.filter(title__icontains=query)
    # Search for recipes in the Recipe model where the title contains the query string (case-insensitive).

    return render(request, 'recipes/search_results.html', {
        # Render the 'search_results.html' template with the context data.
        'query': query,  # Pass the search query to the template.
        'results': results,  # Pass the search results to the template.
    })


def recipe_detail(request, recipe_id):
    # This function handles the request for the details of a specific recipe, identified by recipe_id.

    recipe = get_object_or_404(Recipe, id=recipe_id)
    # Retrieve the Recipe object with the given recipe_id, or return a 404 error if not found.

    # Tracking viewed recipes in session
    viewed_recipes = request.session.get('viewed_recipes', [])
    # Get the list of viewed recipes from the session, defaulting to an empty list if not present.

    if recipe.id not in viewed_recipes:
        # Check if the current recipe has not been viewed yet.
        viewed_recipes.append(recipe.id)
        # Add the current recipe's ID to the list of viewed recipes.

    request.session['viewed_recipes'] = viewed_recipes
    # Update the session with the new list of viewed recipes.

    # Fetching suggestions excluding recently viewed
    suggestions = Recipe.objects.filter(~Q(id__in=viewed_recipes)).distinct()[:5]
    # Query the Recipe model to get distinct recipes that are not in the viewed_recipes list, limiting to 5 suggestions.

    # Handle review submission
    if request.method == 'POST':
        # Check if the request method is POST, indicating a form submission for a review.

        review_form = ReviewForm(request.POST)
        # Create an instance of ReviewForm with the submitted data.

        if review_form.is_valid():
            # Check if the review form data is valid.

            review = review_form.save(commit=False)
            # Create a review instance but do not save it to the database yet.

            review.recipe = recipe
            # Associate the review with the current recipe.

            review.user = request.user
            # Associate the review with the currently logged-in user.

            review.save()
            # Save the review to the database.

            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
            # Redirect the user to the recipe detail page after successfully submitting the review.

    else:
        review_form = ReviewForm()
        # If the request method is not POST, create a new instance of ReviewForm for displaying the form.

    # Fetching the existing reviews for the recipe
    reviews = recipe.reviews.all()
    # Retrieve all reviews associated with the current recipe.

    # calculating the time
    total_seconds = recipe.cook_time.total_seconds()
    # Get the total cook time in seconds.

    hours = total_seconds // 3600
    # Calculate the number of hours from the total seconds.

    minutes = (total_seconds % 3600) // 60
    # Calculate the remaining minutes from the total seconds.

    return render(request, 'recipes/recipe_detail.html', {
        # Render the 'recipe_detail.html' template with the context data.
        'recipe': recipe,  # Pass the recipe object to the template.
        'hours': hours,  # Pass the calculated hours to the template.
        'minutes': minutes,  # Pass the calculated minutes to the template.
        'suggestions': suggestions,  # Pass the recipe suggestions to the template.
        'review_form': review_form,  # Pass the review form to the template.
        'reviews': reviews,  # Pass the existing reviews to the template.
    })


def blog_home(request):
    # This function handles the request for the blog home page.

    # Fetch all blogs from the database
    blogs = Blog.objects.all().order_by('-created_at')  # Latest blogs first
    # Query the Blog model to retrieve all blog entries, ordering them by creation date in descending order (latest first).

    return render(request, 'recipes/blog_home.html', {'blogs': blogs})
    # Render the response using the specified template (the template name is missing in the provided code).


def blog_detail(request, blog_id):
    # This function handles the request for the details of a specific blog post, identified by blog_id.

    blog = get_object_or_404(Blog, id=blog_id)
    # Retrieve the Blog object with the given blog_id, or return a 404 error if not found.

    # Fetch suggestions
    suggestions = get_blog_suggestions(blog)
    # Call the function to get blog suggestions related to the current blog post.

    return render(request, 'recipes/blog_detail.html', {
        # Render the 'blog_detail.html' template with the context data.
        'blog': blog,  # Pass the blog object to the template.
        'suggestions': suggestions,  # Pass the suggestions to the template.
    })

@login_required
# This decorator ensures that only authenticated users can access the create_blog view.

def create_blog(request):
    # This function handles the creation of a new blog post.

    if request.method == "POST":
        # Check if the request method is POST, indicating that the form has been submitted.

        form = BlogForm(request.POST, request.FILES)
        # Create an instance of BlogForm with the submitted data and any uploaded files.

        if form.is_valid():
            # Check if the form data is valid.

            blog = form.save(commit=False)
            # Create a blog instance but do not save it to the database yet.

            blog.author = request.user
            # Set the author of the blog post to the currently logged-in user.

            blog.save()
            # Save the blog post to the database.

            return redirect("recipes:blog_home")
            # Redirect the user to the blog home page after successfully creating the blog post.

    else:
        form = BlogForm()
        # If the request method is not POST, create a new instance of BlogForm for displaying the form.

    return render(request, "recipes/create_blog.html", {"form": form})
    # Render the 'create_blog.html' template with the context data, passing the form to the template.



# Submit Recipe
# This comment indicates that the following function is responsible for submitting a new recipe.

def submit_recipe(request):
    # This function handles the submission of a new recipe.

    if request.method == 'POST':
        # Check if the request method is POST, indicating that the form has been submitted.

        form = RecipeForm(request.POST, request.FILES)
        # Create an instance of RecipeForm with the submitted data and any uploaded files.

        if form.is_valid():
            # Check if the form data is valid.

            form.save()
            # Save the new recipe to the database.

            return redirect('recipes:index')
            # Redirect the user to the index page of recipes after successfully submitting the recipe.

    else:
        form = RecipeForm()
        # If the request method is not POST, create a new instance of RecipeForm for displaying the form.

    return render(request, 'recipes/submit_recipe.html', {'form': form})
    # Render the 'submit_recipe.html' template with the context data, passing the form to the template.


# Service Detail
# This comment indicates that the following function is responsible for displaying the details of a specific service.

def service_detail(request, service_name):
    # This function handles the request for the details of a specific service, identified by service_name.

    context = {
        # Create a context dictionary to pass data to the template.

        'service_name': service_name,
        # Include the service_name in the context to be used in the template.

        'services': {
            # Define a dictionary of services, where each service has its own details.

            'meal-prep-assistance': {
                # Define the details for the 'meal-prep-assistance' service.

                'title': 'Meal prep assistance',
                # Set the title of the service.

                'description': 'Streamline your meal prep routine with expert advice...',
                # Provide a description of the service.

                'image_url': 'images/meal_prep.jpg',
                # Specify the URL of the image associated with the service.

                'button_text': 'Schedule appointment'
                # Set the text for the button that users will click to schedule an appointment.
            },

            # Add other services as needed
            # Placeholder comment indicating where additional services can be added to the dictionary.
        }
    }

    return render(request, 'recipes/service_detail.html', context)
    # Render the 'service_detail.html' template with the context data, passing the service details to the template.


# Latest Recipes
# This comment indicates that the following function is responsible for retrieving and displaying the latest recipes.

def latest_recipes(request):
    # This function handles the request for the latest recipes.

    recipes = Recipe.objects.order_by('-created_at')[:10]
    # Query the Recipe model to retrieve the latest 10 recipes, ordered by creation date in descending order.

    return render(request, 'recipes/latest_recipes.html', {'recipes': recipes})
    # Render the 'latest_recipes.html' template with the context data, passing the latest recipes to the template.





@login_required
# This decorator ensures that only authenticated users can access the user_dashboard view.

def user_dashboard(request):
    # This function handles the request for the user dashboard.

    suggestions = get_recipe_suggestions(user=request.user)
    # Retrieve recipe suggestions for the currently logged-in user.

    # Specify `output_field` to handle mixed types (FloatField and IntegerField)
    # This comment explains that the output_field is specified to manage different data types in the annotation.

    trending_recipes = Recipe.objects.annotate(
        # Annotate the Recipe queryset to include an average rating for each recipe.

        avg_rating=Coalesce(Avg('ratings'), 0, output_field=FloatField())
        # Calculate the average rating of the recipe ratings, using Coalesce to return 0 if there are no ratings.
    ).order_by('-avg_rating')[:5]
    # Order the recipes by average rating in descending order and limit the results to the top 5.

    return render(request, 'profile.html', {
        # Render the 'profile.html' template with the context data.

        'suggestions': suggestions,
        # Pass the recipe suggestions to the template.

        'trending_recipes': trending_recipes,
        # Pass the trending recipes to the template.
    })


# User Login
# This comment indicates that the following function is responsible for handling user login.

def user_login(request):
    # This function processes the login request for users.

    if request.method == 'POST':
        # Check if the request method is POST, indicating that the login form has been submitted.

        form = AuthenticationForm(request, data=request.POST)
        # Create an instance of AuthenticationForm with the submitted data.

        if form.is_valid():
            # Check if the form data is valid.

            username = form.cleaned_data.get('username')
            # Retrieve the cleaned username from the form data.

            password = form.cleaned_data.get('password')
            # Retrieve the cleaned password from the form data.

            user = authenticate(username=username, password=password)
            # Authenticate the user with the provided username and password.

            if user is not None:
                # Check if the user was successfully authenticated.

                login(request, user)
                # Log the user in by creating a session.

                return redirect('recipes:user_dashboard' if not user.is_superuser else '/admin/')
                # Redirect the user to their dashboard if they are not a superuser, otherwise redirect to the admin page.

            else:
                messages.error(request, 'Invalid username or password.')
                # If authentication fails, display an error message for invalid credentials.

        else:
            messages.error(request, 'Invalid username or password.')
            # If the form is not valid, display an error message for invalid credentials.

    else:
        form = AuthenticationForm()
        # If the request method is not POST, create a new instance of AuthenticationForm for displaying the login form.

    return render(request, 'registration/login.html', {'form': form})
    # Render the 'login.html' template with the context data, passing the form to the template.



# defining Chat Room
def chat_room(request, room_name):
    # Render the 'chat_room.html' template with the room name passed as context
    return render(request, 'recipes/chat_room.html', {'room_name': room_name})


# Function to create a new blog post
def create_blog(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Create a form instance with the submitted data and files
        form = BlogForm(request.POST, request.FILES)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to the blog home page after saving
            return redirect("recipes:blog_home")  # Redirect to the blog home
    else:
        # If the request method is not POST, create an empty form
        form = BlogForm()

    # Render the 'create_blog.html' template with the form context
    return render(request, "recipes/create_blog.html", {"form": form})