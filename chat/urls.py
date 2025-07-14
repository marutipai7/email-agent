from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('new_chat/', views.new_chat_view, name='new_chat'),
    path('stream/', views.stream_chat_response, name='stream_chat_response'),
]
