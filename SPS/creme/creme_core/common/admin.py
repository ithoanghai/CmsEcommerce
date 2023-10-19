from django.contrib import admin

from ...comments.models import Comment, Comment_Files
from ...userprofile.models import Address
from ..models.auth import User

# Register your models here.
admin.site.register(Address)
#admin.site.register(Comment)
admin.site.register(Comment_Files)
