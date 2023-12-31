import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..creme_core.core.contants.common import COMMENT_VERB
from ..friends.models import CustomNotification
from ..friends.serializers import NotificationSerializer
from .forms import PostCreateForm
from .models import *


class PostCreateView(CreateView):
    model = Post
    http_method_names = ['post']
    form_class = PostCreateForm
    template_name = 'home.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print(form.errors)
        return redirect(reverse_lazy('homepage'))

    def post(self, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        # comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        notification = CustomNotification.objects.create(recipient=post.user, actor=request.user, verb=COMMENT_VERB,
                                                         description="commented on your post")
        channel_layer = get_channel_layer()
        channel = "comment_like_notifications_{}".format(post.user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",
                "command": "new_like_comment_notification",
                "notification": json.dumps(NotificationSerializer(notification).data),
                'unread_notifications': CustomNotification.objects.user_unread_notification_count(request.user)
            }
        )
        return redirect(reverse_lazy('homepage'))
    else:
        return redirect(reverse_lazy('homepage'))
