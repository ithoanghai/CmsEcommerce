from django.urls import re_path

from .views import (
    review_section,
    review_status,
    review_list,
    review_admin,
    review_bulk_accept,
    result_notification,
    result_notification_prepare,
    result_notification_send,
    review_detail,
    review_delete,
    review_assignments,
    review_assignment_opt_out,

    proposal_submit,
    proposal_submit_kind,
    proposal_detail,
    proposal_edit,
    proposal_speaker_manage,
    proposal_cancel,
    proposal_leave,
    proposal_pending_join,
    proposal_pending_decline,
    document_create,
    document_delete,
    document_download,
)
from . import views


app_name = "reviews"


urlpatterns = [
    re_path(r"^section/(?P<section_slug>[\w\-]+)/all/", review_section, {"reviewed": "all"}, name="review_section"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/reviewed/", review_section, {"reviewed": "reviewed"}, name="user_reviewed"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/not_reviewed/", review_section, {"reviewed": "not_reviewed"}, name="user_not_reviewed"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/assignments/", review_section, {"assigned": True}, name="review_section_assignments"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/status/", review_status, name="review_status"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/status/(?P<key>\w+)/", review_status, name="review_status"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/list/(?P<user_pk>\d+)/", review_list, name="review_list_user"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/admin/", review_admin, name="review_admin"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/admin/accept/", review_bulk_accept, name="review_bulk_accept"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/notification/(?P<status>\w+)/", result_notification, name="result_notification"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/notification/(?P<status>\w+)/prepare/", result_notification_prepare, name="result_notification_prepare"),
    re_path(r"^section/(?P<section_slug>[\w\-]+)/notification/(?P<status>\w+)/send/", result_notification_send, name="result_notification_send"),

    re_path(r"^review/<int:pk>/", review_detail, name="review_detail"),

    re_path(r"^<int:pk>/delete/", review_delete, name="review_delete"),
    re_path(r"^assignments/", review_assignments, name="review_assignments"),
    re_path(r"^assignment/<int:pk>/opt-out/", review_assignment_opt_out, name="review_assignment_opt_out")
]

urlpatterns = urlpatterns + [
    re_path(r"^submit/", views.ProposalKindList.as_view(), name="submission_submit"),
    re_path(r"^submit/(?P<kind_slug>[\w-]+)/", views.SubmissionAdd.as_view(), name="submission_submit_kind"),
    re_path(r"^<int:pk>/", views.SubmissionDetail.as_view(), name="submission_detail"),
    re_path(r"^<int:pk>/edit/", views.SubmissionEdit.as_view(), name="submission_edit"),
    re_path(r"^<int:pk>/cancel/", views.SubmissionCancel.as_view(), name="submission_cancel"),
    re_path(r"^(\d+)/document/create/", views.document_create, name="submission_document_create"),
    re_path(r"^document/(\d+)/delete/", views.document_delete, name="submission_document_delete"),
    re_path(r"^document/(\d+)/([^/]+)$", views.document_download, name="submission_document_download"),

    re_path(r"^all/", views.Reviews.as_view(), {"reviewed": "all"}, name="review_section"),
    re_path(r"^reviewed/", views.Reviews.as_view(), {"reviewed": "reviewed"}, name="user_reviewed"),
    re_path(r"^not-reviewed/", views.Reviews.as_view(), {"reviewed": "not_reviewed"}, name="user_not_reviewed"),
    re_path(r"^assignments/", views.Reviews.as_view(), {"assigned": True}, name="review_section_assignments"),
    re_path(r"^list/(?P<user_pk>\d+)/", views.ReviewList.as_view(), name="review_list_user"),
    re_path(r"^admin/", views.ReviewAdmin.as_view(), name="review_admin"),
    re_path(r"^notification/(?P<status>\w+)/", views.result_notification, name="result_notification"),
    re_path(r"^notification/(?P<status>\w+)/prepare/", views.result_notification_prepare, name="result_notification_prepare"),
    re_path(r"^notification/(?P<status>\w+)/send/", views.result_notification_send, name="result_notification_send"),
    re_path(r"^reviews/<int:pk>/", views.ReviewDetail.as_view(), name="review_detail"),

    re_path(r"^reviews/<int:pk>/delete/", views.ReviewDelete.as_view(), name="review_delete"),

    re_path(r"^submit/", proposal_submit, name="proposal_submit"),
    re_path(r"^submit/([\w\-]+)/", proposal_submit_kind, name="proposal_submit_kind"),
    re_path(r"^(\d+)/", proposal_detail, name="proposal_detail"),
    re_path(r"^(\d+)/edit/", proposal_edit, name="proposal_edit"),
    re_path(r"^(\d+)/speakers/", proposal_speaker_manage, name="proposal_speaker_manage"),
    re_path(r"^(\d+)/cancel/", proposal_cancel, name="proposal_cancel"),
    re_path(r"^(\d+)/leave/", proposal_leave, name="proposal_leave"),
    re_path(r"^(\d+)/join/", proposal_pending_join, name="proposal_pending_join"),
    re_path(r"^(\d+)/decline/", proposal_pending_decline, name="proposal_pending_decline"),

    re_path(r"^(\d+)/document/create/", document_create, name="proposal_document_create"),
    re_path(r"^document/(\d+)/delete/", document_delete, name="proposal_document_delete"),
    re_path(r"^document/(\d+)/([^/]+)$", document_download, name="proposal_document_download"),

]