from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        user =User.objects.create(
            email=f'uwaga2',
            first_name='test_user1',
            last_name='tested1',
            is_superuser=True,
            is_staff=True
        )

        user.set_password('5772')
        user.save()