from rest_framework import serializers
from post.models import Post


# ====================== POST SERIALIZER =======================
class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source = 'author.username',
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['slug']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }