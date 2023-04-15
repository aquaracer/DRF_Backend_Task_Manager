from rest_framework.routers import DefaultRouter
from django.urls import path

from core.api import api_views

router = DefaultRouter()
router.register('task', api_views.TaskViewSet, basename='Task')
router.register('subtask', api_views.SubtaskViewSet, basename='Subtask')


urlpatterns = router.urls

urlpatterns += [
    path('google_auth/', api_views.google_auth),
]
