from django.db.models.signals import post_save
from django.dispatch import receiver

from creme.blogs.conf import settings
from .models import Blog


@receiver(post_save, sender=settings.BLOG_SCOPING_MODEL)
def handle_scoper_save(sender, created, instance, **kwargs):
    if created and settings.BLOG_SCOPING_MODEL is not None:
        Blog.objects.get_or_create(scoper=instance)
