from post.serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from post.models import Post, Comment
from django.utils.text import slugify
from rest_framework.permissions import IsAuthenticated
from post.permissions import IsAuthorOrReadonly, IsOwnerOrAuthorPost


# =========================== POST VIEW ===============================
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='PU')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        auto_slug = slugify(serializer.validated_data['title'])
        serializer.save(slug=auto_slug, author=self.request.user)

    def perform_destroy(self, instance):
        if instance.picture and instance.picture.url:
            instance.picture.delete()
        return super().perform_destroy(instance)

# ======================== COMMENT VIEW ===============================
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAuthorPost]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)