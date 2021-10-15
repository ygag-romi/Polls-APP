from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll


class Command(BaseCommand):
    help = 'Closes a specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        for poll_id in kwargs['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)

            except Poll.DoesNotExist:
                raise CommandError('poll "%s" does not exist' % poll_id)

            poll.closed = True
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed '
                                                 'poll "%s" ' % poll_id))
