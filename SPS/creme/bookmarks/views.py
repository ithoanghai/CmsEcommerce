import datetime

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import gettext as _

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from .forms import BookmarkInstanceForm
from .models import Bookmark, BookmarkInstance


def bookmarks(request):
    bookmarks = Bookmark.objects.all().order_by("-added")
    if request.user.is_authenticated:
        user_bookmarks = Bookmark.objects.filter(
            saved_instances__user=request.user
        )
    else:
        user_bookmarks = []

    context = {
        "bookmarks": bookmarks,
        "user_bookmarks": user_bookmarks,
    }
    return render(request, "bookmarks/bookmarks.html", context)


@login_required
def your_bookmarks(request):
    bookmark_instances = BookmarkInstance.objects.filter(
        user=request.user
    ).order_by("-saved")
    context = {
        "bookmarks": bookmarks,
        "bookmark_instances": bookmark_instances,
    }
    return render(request, "bookmarks/your_bookmarks.html", context)


@login_required
def add(request):
    if request.method == "POST":
        bookmark_form = BookmarkInstanceForm(request.user, request.POST)
        if bookmark_form.is_valid():
            bookmark_instance = bookmark_form.save(commit=False)
            bookmark_instance.user = request.user
            bookmark_instance.save()
            bookmark = bookmark_instance.bookmark

            bookmark.has_favicon = bookmark.favicon_available()
            bookmark.favicon_checked = datetime.datetime.now()
            bookmark.save()

            if bookmark_form.should_redirect():
                return HttpResponseRedirect(bookmark.url)
            else:
                request.user.message_set.create(
                    message=_("You have saved bookmark '%(description)s'") % {
                        "description": bookmark_instance.description
                    }
                )
                return HttpResponseRedirect(reverse("bookmarks:all_bookmarks"))
    else:
        initial = {}
        if "url" in request.GET:
            initial["url"] = request.GET["url"]
        if "description" in request.GET:
            initial["description"] = request.GET["description"].strip()
        if "redirect" in request.GET:
            initial["redirect"] = request.GET["redirect"]

        if initial:
            bookmark_form = BookmarkInstanceForm(initial=initial)
        else:
            bookmark_form = BookmarkInstanceForm()

    bookmarks_add_url = "http://" + Site.objects.get_current().domain + reverse("add_bookmark")
    bookmarklet = ("javascript:location.href='%s?url='+encodeURIComponent(location.href)+';"
                   "description='+encodeURIComponent(document.title)+';redirect=on'"
                   % bookmarks_add_url)

    context = {
        "bookmarklet": bookmarklet,
        "bookmark_form": bookmark_form,
    }
    return render(request, "bookmarks/add.html", context)


@login_required
def delete(request, bookmark_instance_id):
    bookmark_instance = get_object_or_404(
        BookmarkInstance,
        pk=bookmark_instance_id
    )
    if request.user == bookmark_instance.user:
        bookmark_instance.delete()
        request.user.message_set.create(message="Bookmark Deleted")

    if "next" in request.GET:
        next = request.GET["next"]
    else:
        next = reverse("all_bookmarks")

    return HttpResponseRedirect(next)
