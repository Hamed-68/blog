from rest_framework import serializers
from post.models import Post, Comment, Images



class CommentSerializer(serializers.ModelSerializer):
    """ COMMENT SERIALIZER """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only = ['post']



class ImagesSerializer(serializers.ModelSerializer):
    """ IMAGES SERIALIZER """
    class Meta:
        model = Images
        fields = ['id', 'image']



class PostSerializer(serializers.ModelSerializer):
    """ POST SERIALIZER WITHOUT COMMENTS."""
    author = serializers.ReadOnlyField(source='author.username')
    profile = serializers.ImageField(read_only=True, source='author.profile.photo')
    images = ImagesSerializer(many=True, read_only=True)
    uplouded_images = serializers.ListField(
        child=serializers.FileField(max_length=1000,
                                    allow_empty_file=True,
                                    use_url=True),
        write_only=True,
        required=False
    )
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'profile', 'title', 'slug', 'body','images',
            'uplouded_images', 'created', 'updated', 'status'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        images = None
        if validated_data.get('uplouded_images'):   # images are optional in post
            images = validated_data.pop('uplouded_images')
        post = Post.objects.create(**validated_data)
        if images:
            for img in images:  # to save multiple images
                Images.objects.create(post=post, image=img)
        return post

    def update(self, instance, validated_data):
        images = None
        if validated_data.get('uplouded_images'):
            images = validated_data.pop('uplouded_images')
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if images:
            instance.images.all().delete()  # delete old images
            for img in images:
                Images.objects.create(post=instance, image=img)
        return instance