from django.urls import path
from . import views

urlpatterns = [
    path('chat_room/<str:student_id>', views.chat_room, name='chat_room'),
    path('', views.chat_home, name='chat_home')
]
