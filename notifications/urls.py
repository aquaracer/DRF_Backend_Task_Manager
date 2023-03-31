from rest_framework.routers import DefaultRouter
from core.api import api_view

router = DefaultRouter()
router.register('notification', api_view.NotificationViewSet, basename='Task')

urlpatterns = router.urls