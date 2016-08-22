from django.core.management.base import BaseCommand
from base.models import User
import stored_messages

class Command(BaseCommand):
    help = 'Send notifications to users'

    def add_arguments(self, parser):
        parser.add_argument('message', type=str)
        parser.add_argument('users', nargs='+', type=str)

    def handle(self, *args, **options):
        users = User.objects.all().filter(username__in=options['users'])
        stored_messages.api.add_message_for(users, stored_messages.STORED_INFO, options['message'])
