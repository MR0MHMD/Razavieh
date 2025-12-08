from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from notification.models import Notification, Tag
from main.utils import clean_filename
from django.db.models import Count, Q, Value, IntegerField
from django.http import JsonResponse
from .forms import NotificationForm


def notification_list(request, id=None, slug=None):
    tag = None
    if slug:
        tag = get_object_or_404(Tag, id=id, slug=slug)
        notifications = Notification.objects.filter(tags=tag).order_by('-date')
    else:
        notifications = Notification.objects.all().order_by('-date')

    paginator = Paginator(notifications, 12)
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

    tags = notification.tags.all()

    related_qs = Notification.objects.filter(is_active=True).exclude(id=notification.id)

    if tags.exists():
        related_qs = related_qs.annotate(
            same_tags=Count('tags', filter=Q(tags__in=tags))
        )
    else:
        related_qs = related_qs.annotate(
            same_tags=Value(0, output_field=IntegerField())
        )

    def relevance_score(item):
        score = 0
        q_title = notification.title.lower()
        q_desc = notification.content.lower()

        if q_title in item.title.lower():
            score += 3

        if q_title in item.content.lower():
            score += 1

        if q_desc[:40] in item.content.lower():
            score += 1

        return score

    related_list = sorted(
        related_qs,
        key=lambda x: (x.same_tags, relevance_score(x)),
        reverse=True
    )

    related_notifications = related_list[:3]

    context = {
        "notification": notification,
        "related_notifications": related_notifications
    }

    return render(request, "notification/notification/notification_detail.html", context)


def create_notification(request):
    if request.method == "POST":
        form = NotificationForm(request.POST, request.FILES)

        if form.is_valid():
            notification = form.save(commit=False)

            # ✔ تغییر نام فایل قبل از ذخیره
            if "image" in request.FILES:
                notification.image = clean_filename(request.FILES["image"])

            notification.save()
            form.save_m2m()

            # ✔ ذخیره تگ‌ها
            tag_ids_str = request.POST.get("selected_tags", "")
            if tag_ids_str.strip():
                tag_ids = [int(t) for t in tag_ids_str.split(",") if t.strip().isdigit()]
                tags = Tag.objects.filter(id__in=tag_ids)
                notification.tags.set(tags)

            return redirect("notification:notification_list")

    else:
        form = NotificationForm()

    return render(request, "notification/forms/create_notification.html", {
        "form": form,
        "existing_tags": Tag.objects.all(),
    })


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
