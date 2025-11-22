from django.shortcuts import render, redirect
from main.utils import generate_english_slug
from notification.models import Notification
from django.core.paginator import Paginator
from report.models import Report
from django.http import Http404
from django.db.models import Q
from blog.models import Post


def score_result(item, query):
    """
    امتیازدهی به نتایج — هرچه ارتباط بیشتر، امتیاز بالاتر
    """
    query = query.lower()
    score = 0

    # Report
    if isinstance(item, Report):
        if query in item.title.lower():
            score += 3
        if query in item.description.lower():
            score += 2
        if any(query in t.name.lower() for t in item.tags.all()):
            score += 4
        return score

    # Notification
    if isinstance(item, Notification):
        if query in item.title.lower():
            score += 3
        if query in item.content.lower():
            score += 2
        if any(query in t.name.lower() for t in item.tags.all()):
            score += 4
        return score

    # Post
    if isinstance(item, Post):
        if query in item.title.lower():
            score += 3
        if query in item.description.lower():
            score += 2
        return score

    return 0


def search_view(request, clean_query):
    query = request.GET.get('q', '').strip()

    if not query:
        raise Http404("Query is empty.")

    # فقط برای زیبایی URL — تغییری روی دیتابیس نیست
    expected_slug = generate_english_slug(query)

    if clean_query != expected_slug:
        # ریدایرکت به URL صحیح
        return redirect(f"/search/{expected_slug}/?q={query}")

    # انتخاب تب
    tab = request.GET.get("tab", "reports")

    # ------------------------------
    #     جستجو در گزارشات
    # ------------------------------
    reports_qs = Report.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    reports = sorted(reports_qs, key=lambda r: -score_result(r, query))

    paginator_r = Paginator(reports, 6)
    page_r = request.GET.get("page_r", 1)
    reports_page = paginator_r.get_page(page_r)

    # ------------------------------
    #     جستجو در اطلاع‌رسانی
    # ------------------------------
    notif_qs = Notification.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    notifications = sorted(notif_qs, key=lambda r: -score_result(r, query))

    paginator_n = Paginator(notifications, 6)
    page_n = request.GET.get("page_n", 1)
    notifications_page = paginator_n.get_page(page_n)

    # ------------------------------
    #     جستجو در اخبار
    # ------------------------------
    post_qs = Post.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    ).distinct()

    posts = sorted(post_qs, key=lambda r: -score_result(r, query))

    paginator_p = Paginator(posts, 6)
    page_p = request.GET.get("page_p", 1)
    posts_page = paginator_p.get_page(page_p)

    context = {
        "query": query,
        "clean_query": clean_query,
        "tab": tab,
        "reports": reports_page,
        "notifications": notifications_page,
        "posts": posts_page,
        "count_reports": len(reports),
        "count_notifications": len(notifications),
        "count_posts": len(posts),
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        if tab == "reports":
            return render(request, "search/partials/reports_results.html", context)
        if tab == "notifications":
            return render(request, "search/partials/notifications_results.html", context)
        if tab == "posts":
            return render(request, "search/partials/posts_results.html", context)

    return render(request, "search/search/search_page.html", context)
