from django.urls import include, re_path
from ..creme_core.conf.urls import Swappable, swap_manager

from . import activity_model_is_custom
from .views import activity, bricks, calendar, views

app_name = "activities"

calendar_patterns = [
    re_path(
        r'^user[/]?$',
        calendar.CalendarView.as_view(),
        name='calendar',
    ),
    re_path(
        r'^activities[/]?$',
        calendar.ActivitiesData.as_view(),
        name='calendars_activities',
    ),
    re_path(
        r'^select[/]?$',
        calendar.CalendarsSelection.as_view(),
        name='select_calendars',
    ),
    re_path(
        r'^activity/update[/]?$',
        calendar.ActivityDatesSetting.as_view(),
        name='set_activity_dates',
    ),
    re_path(
        r'^add[/]?$',
        calendar.CalendarCreation.as_view(),
        name='create_calendar',
    ),
    re_path(
        r'^(?P<calendar_id>\d+)/edit[/]?$',
        calendar.CalendarEdition.as_view(),
        name='edit_calendar',
    ),
    re_path(
        r'^delete/(?P<calendar_id>\d+)[/]?$',
        calendar.CalendarDeletion.as_view(),
        name='delete_calendar',
    ),
    re_path(
        r'^link/(?P<activity_id>\d+)[/]?$',
        calendar.CalendarLinking.as_view(),
        name='link_calendar',
    ),
]


urlpatterns = calendar_patterns + [
    # re_path(r"(?P<key>[\w\-]+)/start/", views.activity_start, name="activity_start"),
    # re_path(r"(?P<key>[\w\-]+)/play/", views.activity_play, name="activity_play"),
    # re_path(r"(?P<key>[\w\-]+)/completed/", views.activity_completed, name="activity_completed"),

    re_path(r"^staff/", views.staff_dashboard, name="staff_dashboard"),
    re_path(r"^staff/activity/([^/]+)/", views.staff_activity_detail, name="staff_activity_detail"),

    re_path(
        r'^activities/ical[/]?$',
        activity.ICalExport.as_view(),
        name='dl_ical',
    ),

    # Bricks
    re_path(
        r'^activity/(?P<activity_id>\d+)/participant/add[/]?$',
        bricks.ParticipantsAdding.as_view(),
        name='add_participants',
    ),
    re_path(
        r'^activity/participant/delete[/]?$',
        bricks.ParticipantRemoving.as_view(),
        name='remove_participant',
    ),
    re_path(
        r'^activity/(?P<activity_id>\d+)/subject/add[/]?$',
        bricks.SubjectsAdding.as_view(),
        name='add_subjects',
    ),
    re_path(
        r'^activity/subject/delete[/]?$',
        bricks.SubjectRemoving.as_view(),
        name='remove_subject',
    ),
    re_path(
        r'^linked_activity/unlink[/]?$',
        bricks.ActivityUnlinking.as_view(),
        name='unlink_activity',
    ),

    re_path(r'^calendar/', include(calendar_patterns)),

    *swap_manager.add_group(
        activity_model_is_custom,
        Swappable(
            re_path(
                r'^activities[/]?$',
                activity.ActivitiesList.as_view(),
                name='list_activities',
            ),
        ),
        Swappable(
            re_path(
                r'^phone_calls[/]?$',
                activity.PhoneCallsList.as_view(),
                name='list_phone_calls',
            ),
        ),
        Swappable(
            re_path(
                r'^meetings[/]?$',
                activity.MeetingsList.as_view(),
                name='list_meetings',
            ),
        ),
    #
        Swappable(
            re_path(
                r'^activity/add[/]?$',
                activity.ActivityCreation.as_view(),
                name='create_activity',
            ),
        ),
        Swappable(
            re_path(
                r'^activity/add/(?P<act_type>\w+)[/]?$',
                activity.ActivityCreation.as_view(),
                name='create_activity',
            ),
            check_args=('idxxx',),
        ),
        Swappable(
            re_path(
                r'^activity/add_unavailability[/]?$',
                activity.UnavailabilityCreation.as_view(),
                name='create_unavailability',
            )
        ),
        Swappable(
            re_path(
                r'^activity/add_popup[/]?$',
                activity.ActivityCreationPopup.as_view(),
                name='create_activity_popup',
            ),
        ),
        Swappable(
            re_path(
                r'^activity/add_related/(?P<entity_id>\d+)[/]?$',
                activity.RelatedActivityCreation.as_view(),
                name='create_related_activity',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^activity/edit/(?P<activity_id>\d+)[/]?$',
                activity.ActivityEdition.as_view(),
                name='edit_activity',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^activity/(?P<activity_id>\d+)[/]?$',
                activity.ActivityDetail.as_view(),
                name='view_activity',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^activity/(?P<activity_id>\d+)/popup[/]?$',
                activity.ActivityPopup.as_view(),
                name='view_activity_popup',
            ),
            check_args=Swappable.INT_ID,
        ),
       app_name='activities',
    ).kept_patterns(),
]
