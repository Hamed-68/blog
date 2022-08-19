from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import UserViewset


router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]