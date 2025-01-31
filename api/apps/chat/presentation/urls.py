from django.urls import path
from apps.chat.presentation.views.room_view import RoomViewSet
from apps.chat.presentation.views.message_view import MessageViewSet


urlpatterns = [
    path('rooms/', RoomViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('rooms/<int:pk>/', RoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
