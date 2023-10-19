from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from ..creme_core.accounts.mixins import LoginRequiredMixin
from ..creme_core.models.auth import User
from ..userprofile.models import Profile


class TimelineView(DetailView):
    model = User
    template_name = "profile/user-profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"
    object = None

    def get_object(self, queryset=None):
        return self.model.objects.select_related('profile').prefetch_related("posts").get(username=self.kwargs.get(self.slug_url_kwarg))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ProfileEditView(LoginRequiredMixin,UpdateView):
    model = Profile
    template_name = "app_list/profile/edit-my-profile.html"
    context_object_name = "profile"
    object = None
    fields = "__all__"

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user.profile
        return redirect(reverse_lazy('accounts:login'))


    def post(self, request, *args, **kwargs):
        print(request.POST.get('first_name'))
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.about = request.POST.get('about')
        if request.POST.get('gender') == "male":
            user.gender = "male"
        else:
            user.gender = "female"
        user.save()
        profile = user.profile
        profile.country = request.POST.get('country')
        profile.city = request.POST.get('city')
        profile.phone = request.POST.get('phone')
        profile.save()
        return redirect(reverse_lazy('profile:edit-profile'))


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
    else:
        profiles = Profile.objects.exclude()

    return render(request, "profile/profile_list.html", {"profiles": profiles})


class FriendView(DetailView):
    model = User
    template_name = "profile/friend.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"
    object = None

    def get_object(self, queryset=None):
        return self.model.objects.select_related('profile').prefetch_related("posts").get(
            username=self.kwargs.get(self.slug_url_kwarg))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)