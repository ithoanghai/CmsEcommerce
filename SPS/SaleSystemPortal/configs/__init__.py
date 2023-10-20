from . import (
    dua,
    general,
    announcements,
    blog,
    calendars,
    #cohorts,
    #documents,
    invitations,
    likes,
    #message,
    notifications,
    stripe,
    waitinglist,
)

CONFIG_MAP = {
    dua.label: dua,
    general.label: general,
    announcements.label: announcements,
    blog.label: blog,
    calendars.label: calendars,
    #cohorts.label: cohorts,
    #documents.label: documents,
    invitations.label: invitations,
    likes.label: likes,
    #message.label: message,
    notifications.label: notifications,
    stripe.label: stripe,
    waitinglist.label: waitinglist,
}