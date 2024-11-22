from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add users with specific passwords or update their password if they exist'

    def add_arguments(self, parser):
        parser.add_argument('--user-password', action='append', nargs=2, metavar=('USERNAME', 'PASSWORD'), help='Add a username and its password')

    def handle(self, *args, **kwargs):
        user_password_pairs = kwargs['user_password']

        for username, password in user_password_pairs:
            user, created = User.objects.get_or_create(username=username)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists. Updating password.'))
            user.set_password(password)
            user.save()
