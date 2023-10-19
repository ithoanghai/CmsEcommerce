from django.urls import include, re_path

from .views import action, alert, memo, todo, user_message

app_name = "assistants"


urlpatterns = [
    re_path(
        r'^memo/',
        include([
            re_path(
                r'^add/(?P<entity_id>\d+)[/]?$',
                memo.MemoCreation.as_view(),
                name='create_memo',
            ),
            re_path(
                r'^edit/(?P<memo_id>\d+)[/]?$',
                memo.MemoEdition.as_view(),
                name='edit_memo',
            ),
        ]),
    ),
    re_path(
        r'^alert/',
        include([
            re_path(
                r'^add/(?P<entity_id>\d+)[/]?$',
                alert.AlertCreation.as_view(),
                name='create_alert',
            ),
            re_path(
                r'^edit/(?P<alert_id>\d+)[/]?$',
                alert.AlertEdition.as_view(),
                name='edit_alert',
            ),
            re_path(
                r'^validate/(?P<alert_id>\d+)[/]?$',
                alert.validate,
                name='validate_alert',
            ),
            re_path(
                r'^bricks/hide_validated[/]?$',
                alert.HideValidatedAlerts.as_view(),
                name='hide_validated_alerts',
            ),
        ]),
    ),
    re_path(
        r'^todo/', include([
            re_path(
                r'^add/(?P<entity_id>\d+)[/]?$',
                todo.ToDoCreation.as_view(),
                name='create_todo',
            ),
            re_path(
                r'^edit/(?P<todo_id>\d+)[/]?$',
                todo.ToDoEdition.as_view(),
                name='edit_todo',
            ),
            re_path(
                r'^validate/(?P<todo_id>\d+)[/]?$',
                todo.validate,
                name='validate_todo',
            ),
            re_path(
                r'^bricks/hide_validated[/]?$',
                todo.HideValidatedToDos.as_view(),
                name='hide_validated_todos',
            ),
        ]),
    ),
    re_path(
        r'^action/', include([
            re_path(
                r'^add/(?P<entity_id>\d+)[/]?$',
                action.ActionCreation.as_view(),
                name='create_action',
            ),
            re_path(
                r'^edit/(?P<action_id>\d+)[/]?$',
                action.ActionEdition.as_view(),
                name='edit_action',
            ),
            re_path(
                r'^validate/(?P<action_id>\d+)[/]?$',
                action.validate,
                name='validate_action',
            ),
        ]),
    ),
    re_path(
        r'^message/', include([
            re_path(
                r'^add[/]?$',
                user_message.UserMessageCreation.as_view(),
                name='create_message',
            ),
            re_path(
                r'^add/(?P<entity_id>\d+)[/]?$',
                user_message.RelatedUserMessageCreation.as_view(),
                name='create_related_message',
            ),
            re_path(
                r'^delete[/]?$',
                user_message.UserMessageDeletion.as_view(),
                name='delete_message',
            ),
        ]),
    ),
]
