from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TasksViewSet, TaskChangesView

router = DefaultRouter()
router.register('tasks', TasksViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('task_changes/<int:task_id>/', TaskChangesView.as_view(), name='task_changes'),
]
