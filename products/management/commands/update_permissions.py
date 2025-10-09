from django.core.management.base import BaseCommand
from products.permission_manager import update_permission

class Command(BaseCommand):
    help = 'update permissions '
    def handle(self, *args, **options):
        update_permission()

