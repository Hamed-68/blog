from post.serializers import (
    CommentSerializer,
    PostSerializer,
    PostLikeSerializer)
from rest_framework import viewsets
from post.models import Post, Comment, PostLike
from django.utils.text import slugify
from post.permissions import (IsAuthorOrReadonly,
                              IsOwnerOrAuthorPost,
                              IsLikerOrReadonly)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response



class PostView(viewsets.ModelViewSet):
    """ 
    POST VIEW, DISPLAYS USER POSTS AND FOLLOWINGS.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly]
    lookup_fields = ['pk', 'slug']

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.all()
        if user.is_authenticated:
            posts = Post.objects.filter(
                Q(author__followers__user_id=user.id) | Q(author=user)).distinct()
        return posts.filter(status='PU')

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        auto_slug = slugify(serializer.validated_data['title'], allow_unicode=True)
        serializer.save(slug=auto_slug, author=self.request.user)



class ExplorePost(PostView):
    """
    EXPLORE POST VIEW, DISPLAY ALL POSTS.
    """
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Post.objects.filter(status='PU').exclude(
                Q(author__followers__user_id=user.id) | Q(author=user))
        return Post.objects.all()



class CommentView(viewsets.ModelViewSet):
    """ COMMENT VIEW """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAuthorPost]

    @action(detail=True, methods=['get'])
    def post_id(self, request, pk):
        comments = Comment.objects.filter(post=pk).order_by('-created')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PostLikeView(viewsets.ModelViewSet):
    """ POST LIKE VIEW """
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()
    permission_classes = [IsLikerOrReadonly]