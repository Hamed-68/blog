from django.urls import path, include
from post import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'post', views.PostView, basename='post')
router.register(r'comment', views.CommentView, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
]