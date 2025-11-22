from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import NotificationForm
from notification.models import Notification, Tag


def notification_list(request, id=None, slug=None):
    tag = None
    if slug:
        tag = get_object_or_404(Tag, id=id, slug=slug)
        notifications = Notification.objects.filter(tags=tag).order_by('-date')
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


def notification_detail(request, id, slug):
    notification = get_object_or_404(Notification, id=id, slug=slug)
    return render(request, 'notification/notification/notification_detail.html', {'notification': notification})


class create_notification(CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notification/forms/create_notification.html'
    success_url = reverse_lazy('notification:notification_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['existing_tags'] = Tag.objects.all()
        return ctx

    def form_valid(self, form):
        notification = form.save(commit=False)
        notification.save()
        form.save_m2m()

        # ذخیره تگ‌ها
        tag_ids_str = self.request.POST.get("selected_tags", "")
        if tag_ids_str.strip():
            tag_ids = [int(t) for t in tag_ids_str.split(",") if t.strip().isdigit()]
            tags = Tag.objects.filter(id__in=tag_ids)
            notification.tags.set(tags)

        return super().form_valid(form)


@csrf_exempt
def create_tag_ajax(request):
    name = request.POST.get("name", "").strip()
    if not name:
        return JsonResponse({"error": "نام تگ خالی است"}, status=400)

    tag, created = Tag.objects.get_or_create(name=name)

    return JsonResponse({
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug
    })
