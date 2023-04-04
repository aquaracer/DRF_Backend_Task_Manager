from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from core import views
from notifications import views as notifications_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/v1/', include('core.urls')),
    path('core/v1/notifications/', include('notifications.urls')),
    path('core/v1/chat/', include('chat.urls')),
    path('google_login/', views.google_login),
    path('main/', notifications_views.index),
    path('firebase-messaging-sw.js', notifications_views.showFirebaseJS, name="show_firebase_js"),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
