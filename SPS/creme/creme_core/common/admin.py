from django.contrib import admin

from ...comments.models import Comment, Comment_Files
from ...persons.models import Address

# Register your models here.
admin.site.register(Address)
admin.site.register(Comment_Files)
