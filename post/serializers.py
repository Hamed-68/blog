from rest_framework import serializers
from post.models import Post, Comment


# ====================== COMMENT SERIALIZER ======================
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only = ['post']


# ====================== POST SERIALIZER =======================
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(
        read_only = True,
        many=True
    )
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['slug']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }