from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # defining the special method used to call string
    def __str__(self):
        return self.name
#     Returning the name atribute of the category

# Defining model recipe that will be maped to a database table
class Recipe(models.Model):
    # Class level diet choice defined.
    DIET_CHOICES = [
        # list containing dietary options
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
        ('gluten-free', 'Gluten-Free'),
        ('none', 'No Restrictions'),
    ]
    # defining the title field
    title = models.CharField(max_length=200)
    # defining the field description
    description = models.TextField()
    # defining the field ingredients
    ingredients = models.TextField()
    # defining the field instructions
    instructions = models.TextField()
    # defining a fielsd called cook_time
    cook_time = models.DurationField(default=timedelta(minutes=30))
    # defining a field called difficulty
    difficulty = models.CharField(max_length=50)
    # defining a foreign key called category
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="recipes", null=True, blank=True
    )
    # defining a field called cuisine
    cuisine = models.CharField(max_length=50, blank=True, null=True)
    # defines a field called created_at
    created_at = models.DateTimeField(auto_now_add=True)
    # defines a field called calories
    calories = models.FloatField(null=True, blank=True)
    # defines a field called protein
    protein = models.FloatField(null=True, blank=True)
    # defines a field called fat
    fat = models.FloatField(null=True, blank=True)
    # defines a field called sodium
    sodium = models.FloatField(null=True, blank=True)
    # line defines a field called image
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    # defines a field called tags
    tags = TaggableManager()
    # defines a field called ratings
    # validators parameter ensures that the rating must be between 0.0 and 5.0
    ratings = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    # defines a field called diet
    diet = models.CharField(
        max_length=50,
        choices=DIET_CHOICES,
        default='none',
        help_text='Dietary preference for this recipe',
    )
    # choices parameter restricts the values to those defined in DIET_CHOICES
    #  defines a field called spice_level
    spice_level = models.CharField(max_length=50, choices=[
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('hot', 'Hot')
    ], default='mild')  # Add this field if it doesn't exist

    # defining a special method called __str__, which is used to return a string representing the Recipe instance
    def __str__(self):
        return self.title

# This line defines a new model class called UserProfile, which inherits from models.Model.
class UserProfile(models.Model):
    # This means UserProfile is a Django model that will be mapped to a database table.

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # This line defines a one-to-one relationship with the User model.
    # If the associated User is deleted, the UserProfile will also be deleted (on_delete=models.CASCADE).

    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # This line defines a field for storing the user's profile image.
    # The image will be uploaded to the 'profile_images/' directory.
    # The field is optional (blank=True, null=True).

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # This line defines a field for storing the user's phone number.
    # It is a CharField with a maximum length of 15 characters and is optional.

    address = models.CharField(max_length=255, blank=True, null=True)
    # This line defines a field for storing the user's address.
    # It is a CharField with a maximum length of 255 characters and is optional.

    city = models.CharField(max_length=100, blank=True, null=True)
    # This line defines a field for storing the user's city.
    # It is a CharField with a maximum length of 100 characters and is optional.

    state = models.CharField(max_length=100, blank=True, null=True)
    # This line defines a field for storing the user's state.
    # It is a CharField with a maximum length of 100 characters and is optional.

    zip_code = models.CharField(max_length=10, blank=True, null=True)
    # This line defines a field for storing the user's zip code.
    # It is a CharField with a maximum length of 10 characters and is optional.

    country = models.CharField(max_length=100, blank=True, null=True)
    # This line defines a field for storing the user's country.
    # It is a CharField with a maximum length of 100 characters and is optional.

    @property
    # This decorator indicates that the following method is a property of the UserProfile class.
    def timestamp(self):
        # This method returns the current timestamp using timezone.now().
        return timezone.now().timestamp()

    def __str__(self):
        # This method defines a string representation of the UserProfile instance.
        # It returns a formatted string that includes the username of the associated User.
        return f'{self.user.username} Profile'


# This line defines a new model class called Blog, which inherits from models.Model.
class Blog(models.Model):
    # This means Blog is a Django model that will be mapped to a database table.

    title = models.CharField(max_length=255)
    # This line defines a field for storing the title of the blog post.
    # It is a CharField with a maximum length of 255 characters.

    content = models.TextField()
    # This line defines a field for storing the content of the blog post.
    # It is a TextField, which is suitable for longer text.

    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    # This line defines a field for storing an image associated with the blog post.
    # The image will be uploaded to the 'blog_images/' directory.
    # The field is optional (null=True, blank=True).

    created_at = models.DateTimeField(auto_now_add=True)
    # This line defines a field for storing the date and time when the blog post was created.
    # It automatically sets the field to the current date and time when a new Blog instance is created.

    updated_at = models.DateTimeField(auto_now=True)
    # This line defines a field for storing the date and time when the blog post was last updated.
    # It automatically updates the field to the current date and time whenever the Blog instance is saved.

    tags = TaggableManager()  # Add this field
    # This line defines a field for tagging the blog post using TaggableManager from the taggit package.
    # This allows for easy association of tags with the blog post.

    def __str__(self):
        # This method defines a string representation of the Blog instance.
        # It returns the title of the blog post when the instance is converted to a string.
        return self.title


# This line defines a new model class called Review, which inherits from models.Model.
class Review(models.Model):
    # This means Review is a Django model that will be mapped to a database table.

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    # This line defines a foreign key field called recipe, creating a relationship with the Recipe model.
    # If the associated Recipe is deleted, all related Review instances will also be deleted (on_delete=models.CASCADE).
    # The related_name allows reverse access to the reviews from the recipe.

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # This line defines a foreign key field called user, creating a relationship with the User model.
    # If the associated User is deleted, all related Review instances will also be deleted (on_delete=models.CASCADE).

    rating = models.PositiveIntegerField(
        # This line defines a field called rating, which stores a positive integer value.
        validators=[MinValueValidator(1), MaxValueValidator(5)]
        # The validators ensure that the rating must be between 1 and 5 (inclusive).
    )

    comment = models.TextField(blank=True, null=True)
    # This line defines a field called comment for storing user comments on the review.
    # It is a TextField that is optional (blank=True, null=True).

    created_at = models.DateTimeField(auto_now_add=True)
    # This line defines a field called created_at, which stores the date and time when the review was created.
    # It automatically sets the field to the current date and time when a new Review instance is created.

    def __str__(self):
        # This method defines a string representation of the Review instance.
        # It returns a formatted string that includes the username of the user, the title of the recipe, and the rating.
        return f"{self.user.username} - {self.recipe.title} ({self.rating}/5)"