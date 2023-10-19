from django.core.management.base import BaseCommand

from ...models import ProposalResult


class Command(BaseCommand):

    def handle(self, *args, **options):
        ProposalResult.full_calculate()
