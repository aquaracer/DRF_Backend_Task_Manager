from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views
from core.api import api_view

router = DefaultRouter()
router.register('task', api_view.TaskViewSet, basename='Task')
router.register('subtask', api_view.SubtaskViewSet, basename='Subtask')


urlpatterns = router.urls

urlpatterns += [
    path('google_auth/', api_view.google_auth),
]
