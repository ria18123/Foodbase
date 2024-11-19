from datetime import timedelta
import csv
from django.core.management.base import BaseCommand
from recipes.models import Recipe, Category
from taggit.models import Tag

class Command(BaseCommand):
    help = 'Import recipes from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv_file']

        # Clear previous data if needed (optional step to avoid duplicates)
        Recipe.objects.all().delete()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse or create category
                category_name = row.get('category', 'Uncategorized')
                category, _ = Category.objects.get_or_create(name=category_name)

                # Parse cook_time to timedelta if it's available and valid
                cook_time_str = row.get('cook_time')
                if cook_time_str:
                    try:
                        hours, minutes, seconds = map(int, cook_time_str.split(':'))
                        cook_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    except ValueError:
                        cook_time = timedelta(minutes=30)  # Default if parsing fails
                else:
                    cook_time = timedelta(minutes=30)  # Default if missing

                # Parse ratings (use 'rating' from the CSV and map to the 'ratings' field in the model)
                ratings = float(row.get('rating', 0)) if row.get('rating') else None

                # Create Recipe object
                recipe = Recipe(
                    title=row['title'],
                    description=row.get('description', ''),
                    ingredients=row.get('ingredients', ''),
                    instructions=row.get('instructions', ''),
                    cook_time=cook_time,
                    difficulty=row.get('difficulty', 'Medium'),
                    category=category,
                    cuisine=row.get('cuisine', 'Unknown'),
                    calories=float(row.get('calories', 0)) if row.get('calories') else None,
                    protein=float(row.get('protein', 0)) if row.get('protein') else None,
                    fat=float(row.get('fat', 0)) if row.get('fat') else None,
                    sodium=float(row.get('sodium', 0)) if row.get('sodium') else None,
                    ratings=ratings,  # Set ratings here
                )

                # Save the recipe instance
                recipe.save()

                # Add tags to the recipe
                tags_str = row.get('tags')
                if tags_str:
                    tags = [tag.strip() for tag in tags_str.split(',')]  # Split tags by comma
                    recipe.tags.add(*tags)  # Use Taggit to add tags

        self.stdout.write(self.style.SUCCESS('Recipes imported successfully!'))
