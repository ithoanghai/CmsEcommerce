import debug_toolbar
import logging
from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path as url
from django.shortcuts import render
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.views.generic import TemplateView
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.static import serve

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .configs import CONFIG_MAP
from .views import as_view
from .api import api_router

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap as WagtailSitemap
from wagtail.images.views.serve import ServeView

from creme.creme_core.apps import creme_app_configs
from creme.sitemaps import ActivitiesSitemap
from creme.views import dashboard
from creme.sitemaps import NewsSitemap
from creme.creme_core.views.exceptions import permission_denied
from app_CMS.search import views as search_views

logger = logging.getLogger(__name__)
handler403 = permission_denied

openapi_info = openapi.Info(
    title="CRM API",
    default_version="v1",
)


schema_view = get_schema_view(
    openapi_info,
    public=True,
    url=settings.SWAGGER_ROOT_URL,
    permission_classes=(permissions.AllowAny,),
)


# Định nghĩa các sitemaps cho trang web của bạn
sitemaps = {
    'pages': WagtailSitemap,
    'mysitemap': NewsSitemap,
    'activitiessitemap': ActivitiesSitemap
}

def __prepare_static_url():
    static_url = settings.PRODUCTION_MEDIA_URL

    if not isinstance(static_url, str):
        raise ImproperlyConfigured(
            f"settings.PRODUCTION_MEDIA_URL must be a string ; "
            f"it's currently a {type(static_url)}."
        )

    if not static_url.startswith('/') or not static_url.endswith('/'):
        raise ImproperlyConfigured(
            f'settings.PRODUCTION_MEDIA_URL must starts & end with "/" '
            f'(current value is "{static_url}").'
        )

    return static_url[1:]

url_main = [
    # ADMIN PAGE
    path('creme/', include('creme.creme_core.urls')),
    path("admin/", admin.site.urls),
    path("wagtailadmin/", include(wagtailadmin_urls)),

    # MAIN PAGE
    path("", as_view("home.html", config=None), name="homepage"),
    path('shop/', include(apps.get_app_config('creme_config').urls[0])),
    path('cms/', include(wagtail_urls)),


    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('sitemapsocial.xml', sitemap, {'sitemaps': {'socialpages': NewsSitemap}}),
    path('account/social/', include("social.apps.django_app.urls", namespace="social")),
    path('accounts/', include('creme.creme_core.accounts.urls')),

    path('search/', search_views.search, name="search"),

    path("logout/", auth_views.LogoutView.as_view(), {"next_page": "/creme_login/"}, name="logout"),
]

url_crm_cms_social_ecommerce = [
    path('markitup/', include("markitup.urls")),
    # adds internationalization URLs
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # CMS wagtail
    path('documents/', include('wagtail.documents.urls')),
    path('images/<parameter1>/<parameter2>/<parameter3>/', ServeView.as_view(), name='wagtailimages_serve'),
    path("api/v2/", api_router.urls),
    path("__debug__/", include(debug_toolbar.urls)),

    # crm and social and ecommerce Oscar
    path('', include("creme.pages.urls")),
    path('', include('creme.notifications.urls')),
    path('', include('creme.newsfeed.urls')),
    path('', include('creme.friends.urls')),
    path('', include('creme.userprofile.urls')),
    path('', include('creme.communications.urls')),
    path('', include("creme.chatgpt.urls")),
    path('', include("creme.speakers.urls")),
    path('', include("creme.sponsorship.urls")),
    path('', include("creme.boxes.urls")),
    path('', include("creme.teams.urls")),     # path('teams/', include("teams.urls", namespace="teams")),
    path('', include("creme.reviews.urls")),
    path('', include("creme.schedule.urls")),

    path('documents/', include("creme.documents.urls")), # for creme
    path("activities/", include("creme.activities.urls")),  # for creme, social
    path("assistants/", include("creme.assistants.urls")),  # for creme
    path("events/", include("creme.events.urls")),  # for creme
    path("opportunities/", include("creme.opportunity.urls")),  # for creme

    path('invitations/', include("creme.invitations.urls", namespace="invitations")),
    path('announcements/', include("creme.announcements.urls", namespace="announcements")),
    path("blogs", include("creme.blogs.urls", namespace="blogs")),
    path("users/<str:username>/", include("creme.blogs.urls", namespace="blog")),
    path('ajax/images/', include("creme.images.urls", namespace="images")),
    path('payments/', include("creme.stripe.urls", namespace="stripe")),
    path('calendars/', include("creme.calendars.urls", namespace="calendars")),
    path("likes/", include("creme.likes.urls", namespace="likes")),
    path("waitinglist/", include("creme.waitinglist.urls", namespace="waitinglist")),
    path("badges/", include("creme.badges.urls", namespace="badges")),
    path("comment/", include("creme.comments.urls", namespace="comments")),
    path("forums/", include("creme.forums.urls", namespace="forums")),
    path("ratings/", include("creme.ratings.urls", namespace="ratings")),
    path("referrals/", include("creme.referrals.urls", namespace="referrals")),
    path("wiki/", include("creme.wiki.urls", namespace="wiki")),
    path("bookmarks/", include("creme.bookmarks.urls", namespace="bookmarks")),
    path("flags/", include("creme.flag.urls", namespace="flags")),
    # path("phones/", include("creme.phoneconfirm.urls", namespace="phones")),
    # path("message/", include("creme.message.urls", namespace="message")),

    #crm api url
    path("contacts/", include("creme.contacts.urls", namespace="api_contacts")),
    path("leads/", include("creme.leads.urls", namespace="api_leads")),
    path("tasks/", include("creme.tasks.urls", namespace="api_tasks")),
    path("cases/", include("creme.cases.urls", namespace="api_cases")),
    path("teams/", include("creme.teams.urls", namespace="api_teams")),
    path("accounts/", include("creme.creme_core.accounts.urls", namespace="api_accounts")),

    #crm creme base
    url(
        r'^creme_login[/]?$', auth_views.LoginView.as_view(template_name='authent/creme_login.html'),
        name='creme_login',
    ),
    url(
        r'^creme_logout[/]?$', auth_views.logout_then_login, name='creme_logout',
    ),
    url(
        r'^creme_about[/]?$', render,
        {'template_name': 'about/about.html'},
        name='creme_about',
    ),

    # TODO: remove this line when the Rich Text Editor is generated like other static media
    url(
        r'^tiny_mce/(?P<path>.*)$', xframe_options_sameorigin(serve),
        {'document_root': Path(__file__).resolve().parent / 'media' / 'tiny_mce'},
    ),

    # NB: in production, you can configure your web server to statically serve
    #     the files in the directory 'media/static/' (and so the following line is never used).
    url(
        rf'^{__prepare_static_url()}(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT},
    ),
]

url_crm_api = [
    url(
        r"^healthz/$",
        TemplateView.as_view(template_name="healthz.html"),
        name="healthz",
    ),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

urlpatterns = url_main + url_crm_cms_social_ecommerce + url_crm_api

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView
    from django.views.generic.base import RedirectView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path( "favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "img/bread-favicon.ico"), )
    ]

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        path("test404/", TemplateView.as_view(template_name="404.html")),
        path("test500/", TemplateView.as_view(template_name="500.html")),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

for label in CONFIG_MAP:
    urlpatterns.append(CONFIG_MAP[label].url)

for app_config in creme_app_configs():
    app_name = app_config.name

    try:
        included = include(app_name + '.urls')
    except ImportError as e:
        if e.args and 'urls' in e.args[0]:
            logger.warning(f'The app "{app_name}" has no "urls" module.')
        else:  # It seems an annoying ImportError make the existing 'urls' module to be imported.
            raise
    else:
        urlpatterns.append(url(r'^' + app_config.url_root, included))