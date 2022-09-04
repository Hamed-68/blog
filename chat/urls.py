from rest_framework import routers
from django.urls import path, include
from chat import views


router = routers.DefaultRouter()
router.register(r'message', views.ChatMessageViewset, basename='message')


urlpatterns = [
    path('', include(router.urls)),
]
