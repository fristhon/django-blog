from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = settings.SUPERUSER_USERNAME
        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD

        if not User.objects.filter(username=username).exists():
            admin = User.objects.create_superuser(
                email=email, username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Super User {admin = } Created'))
        else:
            self.stdout.write('There is an Admin account already.')