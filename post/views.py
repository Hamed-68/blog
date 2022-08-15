from post.serializers import PostSerializer
from rest_framework import viewsets
from post.models import Post
from django.utils.text import slugify
from rest_framework.permissions import IsAuthenticated


# =========================== POST VIEW ===============================
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='PU')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        auto_slug = slugify(serializer.validated_data['title'])
        serializer.save(slug=auto_slug, author=self.request.user)

    def perform_destroy(self, instance):
        if instance.picture and instance.picture.url:
            instance.picture.delete()
        return super().perform_destroy(instance)