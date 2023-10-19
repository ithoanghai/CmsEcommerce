from django.contrib.sites.models import Site
from django.conf import settings as django_settings
from .configs import CONFIG_MAP

def apps_filter(app):
    return app.startswith("app_list.") or app in ["accounts", "mailer"]


def package_names(names):
    apps = []
    for x in names:
        if x.startswith("app_list."):
            apps.append(x.replace(".", "-"))
        if x == "accounts":
            apps.append("django-user-accounts")
        if x == "mailer":
            apps.append("django-mailer")
    return apps


def settings(request):
    ctx = {
        "available_configs": CONFIG_MAP,

        "ADMIN_URL": django_settings.ADMIN_URL,
        "CONTACT_EMAIL": django_settings.CONTACT_EMAIL,

        "notifications_installed": "notifications" in django_settings.INSTALLED_APPS,
        "invitations_installed": "invitations" in django_settings.INSTALLED_APPS,
        "teams_installed": "teams" in django_settings.INSTALLED_APPS,
        "stripe_installed": "stripe" in django_settings.INSTALLED_APPS,
        "announcements_installed": "announcements" in django_settings.INSTALLED_APPS,
        "blog_installed": "blog" in django_settings.INSTALLED_APPS,
        "calendars_installed": "calendars" in django_settings.INSTALLED_APPS,
        "likes_installed": "likes" in django_settings.INSTALLED_APPS,
        "waitinglist_installed": "waitinglist" in django_settings.INSTALLED_APPS,
        "badges_installed": "badges" in django_settings.INSTALLED_APPS,
        "comments_installed": "comments" in django_settings.INSTALLED_APPS,
        "documents_installed": "documents" in django_settings.INSTALLED_APPS,
        "forums_installed": "forums" in django_settings.INSTALLED_APPS,
        "points_installed": "points" in django_settings.INSTALLED_APPS,
        "ratings_installed": "ratings" in django_settings.INSTALLED_APPS,
        "referrals_installed": "referrals" in django_settings.INSTALLED_APPS,
        "reviews_installed": "reviews" in django_settings.INSTALLED_APPS,
        "wiki_installed": "wiki" in django_settings.INSTALLED_APPS,
        "bookmarks_installed": "wiki" in django_settings.INSTALLED_APPS,
        "flags_installed": "flag" in django_settings.INSTALLED_APPS,
        "activities_installed": "activities" in django_settings.INSTALLED_APPS,

        "app_list": package_names(filter(apps_filter, django_settings.INSTALLED_APPS))
    }

    #if Site._meta.installed:
    if Site._meta:
        site = Site.objects.get_current(request)
        ctx.update({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain
        })

    return ctx
