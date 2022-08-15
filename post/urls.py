from django.urls import path, include
from post import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'', views.PostView, basename='post')


urlpatterns = [
    path(r'', include(router.urls)),
]