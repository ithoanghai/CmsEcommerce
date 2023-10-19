from django.db import models
from django.contrib.humanize.templatetags import humanize
from ..creme_core.models.auth import User
from django.utils.timezone import now


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    created_at = models.DateTimeField(default=now)

    def get_date(self):
        return humanize.naturaltime(self.created_at)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsfeed_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def get_date(self):
        return humanize.naturaltime(self.created_at)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.content[:30]}..."
        )
