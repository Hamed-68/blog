from django.urls import path, include, re_path
from post import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'post', views.PostView, basename='post')
router.register(r'explore', views.ExplorePost, basename='explore')
router.register(r'comment', views.CommentView, basename='comment')
router.register(r'like', views.PostLikeView, basename='like')


urlpatterns = [
    re_path(
        r'post/(?P<pk>[\d]+)/(?P<slug>[-\w]+)/',
        views.PostView.as_view({'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }),
        name='post-detail'),
    re_path(
        r'explore/(?P<pk>[\d]+)/(?P<slug>[-\w]+)/',
        views.ExplorePost.as_view({'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }),
        name='explore-detail'),
    path('', include(router.urls)),
]