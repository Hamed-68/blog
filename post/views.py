from post.serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from post.models import Post, Comment
from django.utils.text import slugify
from rest_framework.permissions import IsAuthenticated
from post.permissions import IsAuthorOrReadonly, IsOwnerOrAuthorPost
from django.shortcuts import get_object_or_404
from django.db.models import Q



class PostView(viewsets.ModelViewSet):
    """ 
    POST VIEW, DISPLAYS USER POSTS AND FOLLOWINGS.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly]
    lookup_fields = ['pk', 'slug']

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(
            Q(author__followers__user_id=user.id) | Q(author=user))
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
            posts = Post.objects.exclude(
                Q(author__followers__user_id=user.id) | Q(author=user))
            return posts.filter(status='PU')
        return Post.objects.all()



class CommentView(viewsets.ModelViewSet):
    """ COMMENT VIEW """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAuthorPost]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)