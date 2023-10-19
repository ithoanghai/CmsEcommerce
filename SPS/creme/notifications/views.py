from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from ..friends.models import CustomNotification
from django.views.generic import TemplateView


class UserAllNotificationListView(LoginRequiredMixin, ListView):
    model = CustomNotification  # Thay thế bằng mô hình thông báo của bạn
    template_name = 'app_list/notifications/notification_list.html'  # Thay thế 'your_template_name.html' bằng tên template của bạn
    context_object_name = 'notifications'  # Tên biến context cho danh sách thông báo

    def get_queryset(self):
        # Trả về danh sách toàn bộ thông báo cho người dùng hiện tại
        return CustomNotification.objects.filter(recipient=self.request.user)
    # Các tùy chọn khác của ListView (nếu cần)


def mark_like_comment_notifications_as_read(request):
    CustomNotification.objects.filter(recipient=request.user, type="comment").update(is_read=False)
    return JsonResponse({
        'status': True,
        'message': "Marked all notifications as read"
    })

