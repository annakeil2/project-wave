import os
from wave_app.models import WaveUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not WaveUser.objects.filter(username='anna').exists():
            WaveUser.objects.create_superuser(
                username='anna',
                email=os.environ.get('SU_EMAIL'),
                password=os.environ.get('SU_PASSWORD')
            )
            print('Superuser has been created.')
        else:
            print('Superuser already exists.')