from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TasksViewSet, FilteredTasksView, TaskChangesView

router = DefaultRouter()
router.register('tasks', TasksViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('task_changes/<int:task_id>/', TaskChangesView.as_view(), name='task_changes'),
    path('filtered_tasks/<str:status>/<str:planned_finish>/', FilteredTasksView.as_view(),
         name='filtered_tasks'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]