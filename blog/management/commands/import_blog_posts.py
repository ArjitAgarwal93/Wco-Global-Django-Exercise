import csv
import os
from django.core.management.base import BaseCommand, CommandError
from blog.models import BlogPost
from django.utils.termcolors import make_style

# Define custom terminal styles
error_style = make_style(fg="red", opts=("bold",))
success_style = make_style(fg="green", opts=("bold",))

class Command(BaseCommand):
    help = "Import blog posts from a CSV file"

    def add_arguments(self, parser):
        """
        Adds argument for passing the CSV file path.
        """
        parser.add_argument(
            "file_path", type=str, help="Path to the CSV file containing blog posts"
        )

    def handle(self, *args, **kwargs):
        """
        Populates the database with data from the specified CSV file.
        Handles basic error checks and logs output.
        """
        file_path = kwargs["file_path"]

        # Check if file exists
        if not os.path.exists(file_path):
            raise CommandError(error_style(f"File '{file_path}' does not exist."))

        try:
            with open(file_path, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                # Ensure required fields are present in the CSV
                required_fields = ["title", "content"]
                for field in required_fields:
                    if field not in reader.fieldnames:
                        raise CommandError(error_style(f"Missing required field: {field}"))

                # Process each row in the CSV
                imported_count = 0
                for row in reader:
                    title = row.get("title", "").strip()
                    content = row.get("content", "").strip()
                    country = row.get("country", "").strip() or None

                    if not title or not content:
                        self.stdout.write(error_style(f"Skipping invalid row: {row}"))
                        continue

                    # Create or update blog post
                    BlogPost.objects.update_or_create(
                        title=title, defaults={"content": content, "country": country}
                    )
                    imported_count += 1

                # Log success
                self.stdout.write(success_style(f"Successfully imported {imported_count} blog posts."))

        except Exception as e:
            raise CommandError(error_style(f"Error importing blog posts: {e}"))
