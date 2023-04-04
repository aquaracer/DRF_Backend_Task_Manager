from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views
from chat.api import api_views

router = DefaultRouter()
router.register('room', api_views.CreateRoomViewSet, basename='Room')

urlpatterns = router.urls

urlpatterns += [
    path('room/<int:pk>/', views.room, name='room'),
]
