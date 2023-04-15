from rest_framework.routers import DefaultRouter

from core.api import api_views

router = DefaultRouter()
router.register('', api_views.NotificationViewSet, basename='Notification')

urlpatterns = router.urls
