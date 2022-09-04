from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import UserViewset, UserFollowingViewset


router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')
router.register(r'following', UserFollowingViewset, basename='user-follow')


urlpatterns = [
    path('', include(router.urls)),
]