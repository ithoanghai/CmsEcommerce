import datetime
import urllib.request
import urllib.parse

from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from taggit.managers import TaggableManager

"""
A Bookmark is unique to a URL whereas a BookmarkInstance represents a
particular Bookmark saved by a particular person.

This not only enables more than one user to save the same URL as a
bookmark but allows for per-user tagging.
"""

# at the moment Bookmark has some fields that are determined by the
# first person to add the bookmark (the adder) but later we may add
# some notion of voting for the best description and note from
# amongst those in the instances.


class Bookmark(models.Model):

    url = models.URLField(unique=True)
    description = models.CharField(_("description"), max_length=100)
    note = models.TextField(_("note"), blank=True)

    has_favicon = models.BooleanField(_("has favicon"))
    favicon_checked = models.DateTimeField(_("favicon checked"), default=datetime.datetime.now)

    adder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="added_bookmarks", verbose_name=_("adder"), on_delete=models.CASCADE)
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)

    def get_favicon_url(self, force=False):
        """
        return the URL of the favicon (if it exists) for the site this
        bookmark is on other return None.

        If force=True, the URL will be calculated even if it does not
        exist.
        """
        if self.has_favicon or force:
            base_url = "%s://%s" % urllib.parse.urlparse(self.url)[:2]
            favicon_url = urllib.parse.urljoin(base_url, "favicon.ico")
            return favicon_url
        return None

    def favicon_available(self):
        try:
            headers = {
                "Accept": ("text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,"
                           "text/plain;q=0.8,image/png,*/*;q=0.5"),
                "Accept-Language": "en-us,en;q=0.5",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Connection": "close",
                # "User-Agent": settings.URL_VALIDATOR_USER_AGENT
                }
            req = urllib.request.Request(self.get_favicon_url(force=True), None, headers)
            urllib.request.urlopen(req)
            return True
        except:
            return False

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ["-added", ]


class BookmarkInstance(models.Model):

    bookmark = models.ForeignKey(Bookmark, related_name="saved_instances",
                                 verbose_name=_("bookmark"), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="saved_bookmarks", verbose_name=_("user"), on_delete=models.CASCADE)
    saved = models.DateTimeField(_("saved"), default=datetime.datetime.now)

    description = models.CharField(_("description"), max_length=100)
    note = models.TextField(_("note"), blank=True)

    tags = TaggableManager()

    def save(self, force_insert=False, force_update=False):
        if getattr(self, 'url', None):
            try:
                bookmark = Bookmark.objects.get(url=self.url)
            except Bookmark.DoesNotExist:
                # has_favicon=False is temporary as the view for adding bookmarks will change it
                bookmark = Bookmark(url=self.url, description=self.description, note=self.note,
                                    has_favicon=False, adder=self.user)
                bookmark.save()
            self.bookmark = bookmark
        super(BookmarkInstance, self).save(force_insert, force_update)

    def delete(self):
        bookmark = self.bookmark
        super(BookmarkInstance, self).delete()
        if bookmark.saved_instances.all().count() == 0:
            bookmark.delete()

    def __unicode__(self):
        return _("%(bookmark)s for %(user)s") % {"bookmark": self.bookmark, "user": self.user}
