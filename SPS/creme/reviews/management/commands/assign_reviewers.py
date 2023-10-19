from django.core.management.base import BaseCommand

from ....proposals.models import ProposalBase
from ...models import ReviewAssignment


class Command(BaseCommand):

    def handle(self, *args, **options):
        for proposal in ProposalBase.objects.filter(cancelled=0):
            print ("Creating assignments for %s" % (proposal.title,))
            ReviewAssignment.create_assignments(proposal)
