import csv
import os
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from contacts.models import Contact 


class Command(BaseCommand):
    help = "Import contacts from a CSV file into the Contact model"

    def add_arguments(self, parser):
        parser.add_argument("csv_filename", type=str, help="CSV file name (located in BASE_DIR)")

    def handle(self, *args, **kwargs):
        csv_filename = kwargs["csv_filename"]
        base_dir = getattr(settings, "BASE_DIR", None)

        if not base_dir:
            self.stderr.write(self.style.ERROR("BASE_DIR is not defined in settings."))
            return

        csv_file_path = os.path.join(base_dir, csv_filename)

        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file_path}"))
            return

        contacts = []

        try:
            with open(csv_file_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    contact_id = row.get("Contact Id", "").strip()
                    first_name = row.get("First Name", "").strip()
                    last_name = row.get("Last Name", "").strip()
                    email = row.get("Email", "").strip()
                    phone = row.get("Phone", "").strip()
                    created = row.get("Created", "").strip()
                    last_activity = row.get("Last Activity", "").strip()

                    # Convert dates to Python datetime
                    created_at = self.parse_date(created)
                    updated_at = self.parse_date(last_activity)

                    contacts.append(
                        Contact(
                            id=contact_id,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            date_added=created_at,
                            date_updated=updated_at,
                        )
                    )

            # Bulk create contacts
            Contact.objects.bulk_create(contacts, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(contacts)} contacts."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing contacts: {e}"))

    def parse_date(self, date_str):
        """Helper method to parse ISO date format"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None
