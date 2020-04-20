from django.core.management import BaseCommand
from django.db import IntegrityError

from users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--username',  type=str)
        parser.add_argument('--password',  type=str)

    def handle(self, *args, **options):
        if options.get('username') or options.get('password'):
            try:
                User.objects.create_superuser(username=options['username'], password=options['password'])
                self.stdout.write(self.style.SUCCESS('Admin user was created'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING('The admin user have already been created'))
        else:
            self.stdout.write(self.style.WARNING('Please provide username and password'))
