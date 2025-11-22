from django.conf.urls import handler404, handler500, handler403
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/', include('report.urls', namespace='report')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('donation/', include('donation.urls', namespace='donation')),
    path('notification/', include('notification.urls', namespace='notification')),
    path('search/<slug:clean_query>/', include('search.urls', namespace='search')),
    path('', include('main.urls', namespace='main')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
handler403 = 'main.views.error_403'
