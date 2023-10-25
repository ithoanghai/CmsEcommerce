from celery import Celery
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Teams, Profile, Contact

app = Celery("redis://")


@app.task
def remove_users(removed_users_list, team_id):
    removed_users_list = [i for i in removed_users_list if i.isdigit()]
    users_list = Profile.objects.filter(id__in=removed_users_list)
    if users_list.exists():
        team = Teams.objects.filter(id=team_id).first()
        if team:
            accounts = team.account_teams.all()
            for account in accounts:
                for user in users_list:
                    account.assigned_to.remove(user)

            # for contacts
            contacts = team.contact_teams.all()
            for contact in contacts:
                for user in users_list:
                    contact.assigned_to.remove(user)

            # for leads
            leads = team.lead_teams.all()
            for lead in leads:
                for user in users_list:
                    lead.assigned_to.remove(user)

            # for opportunities
            opportunities = team.oppurtunity_teams.all()
            for opportunity in opportunities:
                for user in users_list:
                    opportunity.assigned_to.remove(user)

            # for cases
            cases = team.cases_teams.all()
            for case in cases:
                for user in users_list:
                    case.assigned_to.remove(user)

            # for documents
            docs = team.document_teams.all()
            for doc in docs:
                for user in users_list:
                    doc.shared_to.remove(user)

            # for tasks
            tasks = team.tasks_teams.all()
            for task in tasks:
                for user in users_list:
                    task.assigned_to.remove(user)

            # for invoices
            invoices = team.invoices_teams.all()
            for invoice in invoices:
                for user in users_list:
                    invoice.assigned_to.remove(user)

            # for events
            events = team.event_teams.all()
            for event in events:
                for user in users_list:
                    event.assigned_to.remove(user)


@app.task
def update_team_users(team_id):
    """this function updates assigned_to field on all models when a team is updated"""
    team = Teams.objects.filter(id=team_id).first()
    if team:
        teams_members = team.users.all()
        # for accounts
        accounts = team.account_teams.all()
        for account in accounts:
            account_assigned_to_users = account.assigned_to.all()
            for team_member in teams_members:
                if team_member not in account_assigned_to_users:
                    account.assigned_to.add(team_member)

        # for contacts
        contacts = team.contact_teams.all()
        for contact in contacts:
            contact_assigned_to_users = contact.assigned_to.all()
            for team_member in teams_members:
                if team_member not in contact_assigned_to_users:
                    contact.assigned_to.add(team_member)

        # for leads
        leads = team.lead_teams.all()
        for lead in leads:
            lead_assigned_to_users = lead.assigned_to.all()
            for team_member in teams_members:
                if team_member not in lead_assigned_to_users:
                    lead.assigned_to.add(team_member)

        # for opportunities
        opportunities = team.oppurtunity_teams.all()
        for opportunity in opportunities:
            opportunity_assigned_to_users = opportunity.assigned_to.all()
            for team_member in teams_members:
                if team_member not in opportunity_assigned_to_users:
                    opportunity.assigned_to.add(team_member)

        # for cases
        cases = team.cases_teams.all()
        for case in cases:
            case_assigned_to_users = case.assigned_to.all()
            for team_member in teams_members:
                if team_member not in case_assigned_to_users:
                    case.assigned_to.add(team_member)

        # for documents
        docs = team.document_teams.all()
        for doc in docs:
            doc_assigned_to_users = doc.shared_to.all()
            for team_member in teams_members:
                if team_member not in doc_assigned_to_users:
                    doc.shared_to.add(team_member)

        # for tasks
        tasks = team.tasks_teams.all()
        for task in tasks:
            task_assigned_to_users = task.assigned_to.all()
            for team_member in teams_members:
                if team_member not in task_assigned_to_users:
                    task.assigned_to.add(team_member)

        # for invoices
        invoices = team.invoices_teams.all()
        for invoice in invoices:
            invoice_assigned_to_users = invoice.assigned_to.all()
            for team_member in teams_members:
                if team_member not in invoice_assigned_to_users:
                    invoice.assigned_to.add(team_member)

        # for events
        events = team.event_teams.all()
        for event in events:
            event_assigned_to_users = event.assigned_to.all()
            for team_member in teams_members:
                if team_member not in event_assigned_to_users:
                    event.assigned_to.add(team_member)


@app.task
def send_email_to_assigned_user(recipients, contact_id):
    """Send Mail To Users When they are assigned to a contact"""
    contact = Contact.objects.get(id=contact_id)
    created_by = contact.created_by
    for profile_id in recipients:
        recipients_list = []
        profile = Profile.objects.filter(id=profile_id, is_active=True).first()
        if profile:
            recipients_list.append(profile.user.email)
            context = {}
            context["url"] = settings.DOMAIN_NAME
            context["user"] = profile.user
            context["contact"] = contact
            context["created_by"] = created_by
            subject = "Assigned a contact for you."
            html_content = render_to_string(
                "assigned_to/contact_assigned.html", context=context
            )

            msg = EmailMessage(subject, html_content, to=recipients_list)
            msg.content_subtype = "html"
            msg.send()

