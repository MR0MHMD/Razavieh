from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from .forms import NotificationForm


def notification_list(request, tag=None):
    if tag:
        notifications = Notification.objects.filter(tags__slug=tag).order_by('-date')
    else:
        notifications = Notification.objects.all().order_by('-date')

    paginator = Paginator(notifications, 9)
    page_number = request.GET.get('page', 1)
    try:
        notifications = paginator.page(page_number)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    context = {
        'notifications': notifications,
        'tag': tag,
    }
    return render(request, 'notification/notification/notification_list.html', context)


def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    return render(request, 'notification/notification/notification_detail.html', {'notification': notification})


def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('notification:notification_list')
    else:
        form = NotificationForm()
    return render(request, 'notification/forms/create_notification.html', {'form': form})
