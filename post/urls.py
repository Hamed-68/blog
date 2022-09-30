from django.urls import path, include, re_path
from post import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'post', views.PostView, basename='post')
router.register(r'comment', views.CommentView, basename='comment')


urlpatterns = [
    re_path(
        r'post/(?P<pk>[\d]+)/(?P<slug>[-\w]+)/',
        views.PostView.as_view({'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }),
        name='post-detail'),
    path('', include(router.urls)),
]