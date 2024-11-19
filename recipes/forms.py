# Import forms module from Django for creating forms
from django import forms
# Import timedelta for handling time durations
from datetime import timedelta
# Import Recipe, UserProfile, and Blog models from the current app's models
from .models import Recipe, UserProfile, Blog  # Import Blog directly from models
# Import Review model from the current app's models
from .models import Review

# Define a form for creating and editing Blog instances
class BlogForm(forms.ModelForm):
    # Meta class to specify model and fields for the form
    class Meta:
        model = Blog  # Specify the model to use
        fields = ['title', 'content', 'image']  # Specify the fields to include in the form

# Define a form for filtering recipes
class RecipeFilterForm(forms.Form):
    # Create a choice field for selecting spice level
    spice_level = forms.ChoiceField(
        choices=[  # Define the choices for spice level
            ('mild', 'Mild'),
            ('medium', 'Medium'),
            ('hot', 'Hot')
        ],
        required=False,  # This field is not required
        widget=forms.Select(attrs={'class': 'form-control'})  # Use a select widget with Bootstrap class
    )

# Define a form for creating and editing Recipe instances
class RecipeForm(forms.ModelForm):
    # Create an integer field for cook time in hours
    cook_time_hours = forms.IntegerField(
        required=False,  # This field is not required
        min_value=0,  # Minimum value is 0
        label="Cook Time (Hours)",  # Label for the field
        widget=forms.NumberInput(attrs={'placeholder': 'Hours'})  # Use a number input widget with placeholder
    )

    # Create an integer field for cook time in minutes
    cook_time_minutes = forms.IntegerField(
        required=False,  # This field is not required
        min_value=0,  # Minimum value is 0
        max_value=59,  # Maximum value is 59
        label="Cook Time (Minutes)",  # Label for the field
        widget=forms.NumberInput(attrs={'placeholder': 'Minutes'})  # Use a number input widget with placeholder
    )

    # Meta class to specify model and fields for the form
    class Meta:
        model = Recipe  # Specify the model to use
        fields = [  # Specify the fields to include in the form
            'title', 'description', 'ingredients', 'instructions',
            'difficulty', 'category', 'cuisine', 'calories', 'protein',
            'fat', 'sodium', 'image', 'tags'  # Include tags field here
        ]

    # Clean method to validate and process form data
    def clean(self):
        cleaned_data = super().clean()  # Call the parent clean method
        hours = cleaned_data.get('cook_time_hours') or 0  # Get hours or default to 0
        minutes = cleaned_data.get('cook_time_minutes') or 0  # Get minutes or default to 0

        # Ensure minutes is valid
        if minutes < 0 or minutes > 59:
            self.add_error('cook_time_minutes', "Minutes should be between 0 and 59.")  # Add error if invalid

        # Set the `cook_time` field as a timedelta
        cleaned_data['cook_time'] = timedelta(hours=hours, minutes=minutes)  # Create timedelta object
        return cleaned_data  # Return cleaned data

    # Save method to handle saving the form data
    def save(self, commit=True):
        instance = super().save(commit=False)  # Create an instance without saving yet
        # Update the cook_time field on the model instance
        cook_time = self.cleaned_data.get('cook_time', timedelta())  # Get cook_time or default to timedelta()
        instance.cook_time = cook_time  # Set the cook_time on the instance
        if commit:
            instance.save()  # Save the instance if commit is True
            self.save_m2m()  # Save many-to-many fields (e.g., tags)
        return instance  # Return the saved instance

# Define a form for creating and editing UserProfile instances
class UserProfileForm(forms.ModelForm):
    # Meta class to specify model and fields for the form
    class Meta:
        model = UserProfile  # Specify the model to use
        fields = [  # Specify the fields to include in the form
            'profile_image', 'phone_number', 'address',
            'city', 'state', 'zip_code', 'country'
        ]
        # Define custom widgets for specific fields
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),  # Placeholder for phone number
            'address': forms.TextInput(attrs={'placeholder': 'Street Address'}),  # Placeholder for address
            'city': forms.TextInput(attrs={'placeholder': 'City'}),  # Placeholder for city
            'state': forms.TextInput(attrs={'placeholder': 'State'}),  # Placeholder for state
            'zip_code': forms.TextInput(attrs={'placeholder': 'ZIP Code'}),  # Placeholder for ZIP code
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),  # Placeholder for country
        }

# Define a form for creating and editing Review instances
class ReviewForm(forms.ModelForm):
    # Meta class to specify model and fields for the form
    class Meta:
        model = Review  # Specify the model to use
        fields = ['rating', 'comment']  # Specify the fields to include in the form
        # Define custom widgets for specific fields
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1, 'class': 'form-control'}),  # Rating input with constraints
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # Textarea for comment with Bootstrap class
        }