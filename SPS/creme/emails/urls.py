from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static

from .. import emails
from ..creme_core.conf.urls import Swappable, swap_manager
from .views import (
    campaign,
    mail,
    mailing_list,
    recipient,
    sending,
    signature,
    synchronization,
    template,
)

app_name = "emails"

urlpatterns = [
    # Campaign: mailing_list brick
    re_path(
        r'^campaign/(?P<campaign_id>\d+)/mailing_list/add[/]?$',
        campaign.MailingListsAdding.as_view(),
        name='add_mlists_to_campaign'
    ),
    re_path(
        r'^campaign/(?P<campaign_id>\d+)/mailing_list/delete[/]?$',
        campaign.MailingListRemoving.as_view(),
        name='remove_mlist_from_campaign'
    ),

    # Campaign: sending configuration
    re_path(
        r'^sending/config/add[/]?$',
        sending.SendingConfigItemCreation.as_view(),
        name='create_sending_config_item',
    ),
    re_path(
        r'^sending/config/edit/(?P<item_id>\d+)[/]?$',
        sending.SendingConfigItemEdition.as_view(),
        name='edit_sending_config_item',
    ),
    re_path(
        r'^sending/config/set_password/(?P<item_id>\d+)[/]?$',
        sending.SendingConfigItemPasswordEdition.as_view(),
        name='set_sending_config_item_password',
    ),
    re_path(
        r'^sending/config/delete[/]?$',
        sending.SendingConfigItemDeletion.as_view(),
        name='delete_sending_config_item',
    ),

    # Campaign: sending brick
    re_path(
        r'^campaign/(?P<campaign_id>\d+)/sending/add[/]?$',
        sending.SendingCreation.as_view(),
        name='create_sending',
    ),
    re_path(
        r'^sending/(?P<sending_id>\d+)/edit[/]?$',
        sending.SendingEdition.as_view(),
        name='edit_sending',
    ),

    # Campaign: sending details brick
    re_path(
        r'^sending/(?P<sending_id>\d+)[/]?$',
        sending.SendingDetail.as_view(),
        name='view_sending',
    ),
    re_path(
        r'^sending/(?P<sending_id>\d+)/get_body[/]?$',
        sending.SendingBody.as_view(),
        name='sending_body',
    ),
    re_path(
        r'^sending/(?P<sending_id>\d+)/reload[/]?$',
        sending.SendingBricksReloading.as_view(),
        name='reload_sending_bricks',
    ),

    # Mailing list: recipients brick
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/recipient/add[/]?$',
        recipient.RecipientsAdding.as_view(),
        name='add_recipients',
    ),
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/recipient/add_csv[/]?$',
        recipient.RecipientsAddingFromCSV.as_view(),
        name='add_recipients_from_csv',
    ),

    # Mailing list: contacts brick
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/contact/add[/]?$',
        mailing_list.ContactsAdding.as_view(),
        name='add_contacts_to_mlist',
    ),
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/contact/add_from_filter[/]?$',
        mailing_list.ContactsAddingFromFilter.as_view(),
        name='add_contacts_to_mlist_from_filter',
    ),
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/contact/delete[/]?$',
        mailing_list.ContactRemoving.as_view(),
        name='remove_contact_from_mlist',
    ),

    # Mailing list: organisations brick
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/organisation/add[/]?$',
        mailing_list.OrganisationsAdding.as_view(),
        name='add_orgas_to_mlist',
    ),
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/organisation/add_from_filter[/]?$',
        mailing_list.OrganisationsAddingFromFilter.as_view(),
        name='add_orgas_to_mlist_from_filter',
    ),
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/organisation/delete[/]?$',
        mailing_list.OrganisationRemoving.as_view(),
        name='remove_orga_from_mlist',
    ),

    # Mailing list: child lists brick
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/child/add[/]?$',
        mailing_list.ChildrenAdding.as_view(),
        name='add_child_mlists',
    ),
    re_path(
        r'^mailing_list/(?P<ml_id>\d+)/child/delete[/]?$',
        mailing_list.ChildRemoving.as_view(),
        name='remove_child_mlist',
    ),

    # Template: attachment brick
    re_path(
        r'^template/(?P<template_id>\d+)/attachment/add[/]?$',
        template.AttachmentsAdding.as_view(),
        name='add_attachments_to_template',
    ),
    re_path(
        r'^template/(?P<template_id>\d+)/attachment/delete[/]?$',
        template.AttachmentRemoving.as_view(),
        name='remove_attachment_from_template',
    ),

    # Mails history bricks
    re_path(
        r'^mails_history/(?P<mail_id>\w+)[/]?$',
        mail.LightWeightEmailPopup.as_view(),
        name='view_lw_mail'
    ),  # TODO: improve URL (lw_mail...)
    re_path(
        r'^mail/get_body/(?P<mail_id>\w+)[/]?$',
        mail.LightWeightEmailBody.as_view(),
        name='lw_mail_body',
    ),  # TODO: idem
    re_path(
        r'^mail/resend[/]?$',
        mail.EntityEmailsResending.as_view(),
        name='resend_emails',
    ),
    re_path(
        r'^mail/link/(?P<subject_id>\w+)[/]?$',
        mail.EntityEmailLinking.as_view(),
        name='link_emails',
    ),

    # Signature
    re_path(
        r'^signature/',
        include([
            re_path(
                r'^add[/]?$',
                signature.SignatureCreation.as_view(),
                name='create_signature',
            ),
            re_path(
                r'^edit/(?P<signature_id>\d+)[/]?$',
                signature.SignatureEdition.as_view(),
                name='edit_signature',
            ),
            re_path(
                r'^delete[/]?$',
                signature.SignatureDeletion.as_view(),
                name='delete_signature',
            ),
        ]),
    ),

    # Synchronization
    re_path(
        r'^synchronization/',
        include([
            re_path(
                r'^portal[/]?$',
                synchronization.SynchronizationPortal.as_view(),
                name='sync_portal',
            ),
            re_path(
                r'^email_to_sync/accept[/]?$',
                synchronization.EmailToSyncAcceptation.as_view(),
                name='accept_email_to_sync',
            ),
            re_path(
                r'^email_to_sync/delete[/]?$',
                synchronization.EmailToSyncDeletion.as_view(),
                name='delete_email_to_sync',
            ),

            re_path(
                r'^email_to_sync/person/edit/(?P<person_id>\d+)[/]?$',
                synchronization.EmailToSyncPersonEdition.as_view(),
                name='edit_email_to_sync_person',
            ),
            re_path(
                r'^email_to_sync/(?P<mail_id>\d+)/fix[/]?$',
                synchronization.EmailToSyncCorrection.as_view(),
                name='fix_email_to_sync',
            ),
            re_path(
                r'^email_to_sync/(?P<mail_id>\d+)/recipient/mark[/]?$',
                synchronization.EmailToSyncRecipientMarking.as_view(),
                name='mark_email_to_sync_recipient',
            ),
            re_path(
                r'^email_to_sync/(?P<mail_id>\d+)/recipient/delete[/]?$',
                synchronization.EmailToSyncRecipientDeletion.as_view(),
                name='delete_email_to_sync_recipient',
            ),

            re_path(
                r'^email_to_sync/(?P<mail_id>\d+)/attachment/delete[/]?$',
                synchronization.EmailToSyncAttachmentDeletion.as_view(),
                name='delete_email_to_sync_attachment',
            ),

            # Configuration
            re_path(
                r'^config/add[/]?$',
                synchronization.SynchronizationConfigItemCreation.as_view(),
                name='create_sync_config_item',
            ),
            re_path(
                r'^config/edit/(?P<item_id>\d+)[/]?$',
                synchronization.SynchronizationConfigItemEdition.as_view(),
                name='edit_sync_config_item',
            ),
            re_path(
                r'^config/delete[/]?$',
                synchronization.SynchronizationConfigItemDeletion.as_view(),
                name='delete_sync_config_item',
            ),
        ]),
    ),

    re_path(r"^list/", mail.emails_list, name="list"),
    re_path(r"^compose/", mail.email, name="compose"),
    re_path(r"^email_sent/", mail.email_sent, name="email_sent"),
    re_path(
        r"^email_move_to_trash/(?P<pk>\d+)/$",
        mail.email_move_to_trash,
        name="email_move_to_trash",
    ),
    re_path(r"^email_delete/(?P<pk>\d+)/$", mail.email_delete, name="email_delete"),
    re_path(r"^email_trash/", mail.email_trash, name="email_trash"),
    re_path(
        r"^email_trash_delete/(?P<pk>\d+)/$",
        mail.email_trash_delete,
        name="email_trash_delete",
    ),
    re_path(r"^email_draft/", mail.email_draft, name="email_draft"),
    re_path(
        r"^email_draft_delete/(?P<pk>\d+)/$",
        mail.email_draft_delete,
        name="email_draft_delete",
    ),
    re_path(r"^email_imp/(?P<pk>\d+)/$", mail.email_imp, name="email_imp"),
    re_path(r"^email_imp_list/", mail.email_imp_list, name="email_imp_list"),
    re_path(
        r"^email_sent_edit/(?P<pk>\d+)/$", mail.email_sent_edit, name="email_sent_edit"
    ),
    re_path(r"^email_unimp/(?P<pk>\d+)/$", mail.email_unimp, name="email_unimp"),
    re_path(r"^email_view/(?P<pk>\d+)/$", mail.email_view, name="email_view"),

    *swap_manager.add_group(
        emails.emailcampaign_model_is_custom,
        Swappable(
            re_path(
                r'^campaigns[/]?$',
                campaign.EmailCampaignsList.as_view(),
                name='list_campaigns',
            ),
        ),
        Swappable(
            re_path(
                r'^campaign/add[/]?$',
                campaign.EmailCampaignCreation.as_view(),
                name='create_campaign',
            ),
        ),
        Swappable(
            re_path(
                r'^campaign/edit/(?P<campaign_id>\d+)[/]?$',
                campaign.EmailCampaignEdition.as_view(),
                name='edit_campaign',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^campaign/(?P<campaign_id>\d+)[/]?$',
                campaign.EmailCampaignDetail.as_view(),
                name='view_campaign',
            ),
            check_args=Swappable.INT_ID,
        ),
        app_name='emails',
    ).kept_patterns(),

    *swap_manager.add_group(
        emails.emailtemplate_model_is_custom,
        Swappable(
            re_path(
                r'^templates[/]?$',
                template.EmailTemplatesList.as_view(),
                name='list_templates',
            ),
        ),
        Swappable(
            re_path(
                r'^template/add[/]?$',
                template.EmailTemplateCreation.as_view(),
                name='create_template',
            ),
        ),
        Swappable(
            re_path(
                r'^template/edit/(?P<template_id>\d+)[/]?$',
                template.EmailTemplateEdition.as_view(),
                name='edit_template',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^template/(?P<template_id>\d+)[/]?$',
                template.EmailTemplateDetail.as_view(),
                name='view_template',
            ),
            check_args=Swappable.INT_ID,
        ),
        app_name='emails',
    ).kept_patterns(),

    *swap_manager.add_group(
        emails.entityemail_model_is_custom,
        Swappable(
            re_path(
                r'^mails[/]?$',
                mail.EntityEmailsList.as_view(),
                name='list_emails',
            ),
        ),
        Swappable(
            re_path(
                r'^mail/add/(?P<entity_id>\d+)[/]?$',
                mail.EntityEmailCreation.as_view(),
                name='create_email',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^mail/add_from_template/(?P<entity_id>\d+)[/]?$',
                mail.EntityEmailWizard.as_view(),
                name='create_email_from_template',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^mail/(?P<mail_id>\d+)[/]?$',
                mail.EntityEmailDetail.as_view(),
                name='view_email',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^mail/(?P<mail_id>\d+)/popup[/]?$',
                mail.EntityEmailPopup.as_view(),
                name='view_email_popup',
            ),
            check_args=Swappable.INT_ID,
        ),
        app_name='emails',
    ).kept_patterns(),

    *swap_manager.add_group(
        emails.mailinglist_model_is_custom,
        Swappable(
            re_path(
                r'^mailing_lists[/]?$',
                mailing_list.MailingListsList.as_view(),
                name='list_mlists',
            ),
        ),
        Swappable(
            re_path(
                r'^mailing_list/add[/]?$',
                mailing_list.MailingListCreation.as_view(),
                name='create_mlist',
            ),
        ),
        Swappable(
            re_path(
                r'^mailing_list/edit/(?P<ml_id>\d+)[/]?$',
                mailing_list.MailingListEdition.as_view(),
                name='edit_mlist',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^mailing_list/(?P<ml_id>\d+)[/]?$',
                mailing_list.MailingListDetail.as_view(),
                name='view_mlist',
            ),
            check_args=Swappable.INT_ID,
        ),
        app_name='emails',
    ).kept_patterns(),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
