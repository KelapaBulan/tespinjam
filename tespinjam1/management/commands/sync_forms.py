from django.core.management.base import BaseCommand
from tespinjam1.sheet_firebase_sync import sync_sheet_to_firebase


class Command(BaseCommand):
    help = "Sync Google Form responses to Firebase"

    def handle(self, *args, **options):
        sync_sheet_to_firebase()
        self.stdout.write(self.style.SUCCESS("Sync completed"))