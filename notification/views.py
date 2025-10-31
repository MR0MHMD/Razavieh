from django.shortcuts import render, get_object_or_404
from .models import Notification


def notification_list(request, tag=None):
    if tag:
        notifications = Notification.objects.filter(tags__slug=tag)
    else:
        notifications = Notification.objects.all()
    context = {
        'notifications': notifications,
        'tag': tag,
    }
    return render(request, 'notification/notification/notification_list.html', context)


def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    return render(request, 'notification/notification/notification_detail.html', {'notification': notification})
