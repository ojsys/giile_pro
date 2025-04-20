from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('events/', include('events.urls', namespace='events')),
    path('talent/', include('talent.urls', namespace='talent')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
