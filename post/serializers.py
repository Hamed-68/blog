from rest_framework import serializers
from post.models import Post, Comment, Images, PostLike
from django.db.models import Q



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
    like = serializers.IntegerField(source='get_likes', read_only=True) # count likes
    # indicate current user liked this post
    status_like = serializers.SerializerMethodField()
    images = ImagesSerializer(many=True, read_only=True)
    image_option = serializers.CharField(write_only=True, required=False)
    uplouded_images = serializers.ListField(
        child=serializers.FileField(max_length=1000,
                                    allow_empty_file=True,
                                    use_url=True),
        write_only=True,
        required=False
    )

    def get_status_like(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                return PostLike.objects.get(
                    Q(user=user) & Q (post=obj)).id
            except PostLike.DoesNotExist:
                return 0
        return 0

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'profile', 'title', 'slug', 'body',
            'like', 'status_like', 'images', 'image_option',
            'uplouded_images', 'created', 'updated', 'status'
        ]
        read_only_fields = ['slug']

    def create(self, validated_data):
        uplouded_images = validated_data.pop('uplouded_images', None)
        post = Post.objects.create(**validated_data)
        if uplouded_images:
            for img in uplouded_images:  # to save multiple images
                Images.objects.create(post=post, image=img)
        return post

    def update(self, instance, validated_data):
        uplouded_images = validated_data.pop('uplouded_images', None) # new images
        image_option = validated_data.pop('image_option', None) # deleted images
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if uplouded_images: # add new images (optional)
            for img in uplouded_images:
                Images.objects.create(post=instance, image=img)
        if image_option:  # delete old images (optional)
            ids = image_option.strip('[]').split(',')
            for id in ids:
                try:
                    Images.objects.get(id=id).delete()
                except Images.DoesNotExist:
                    pass
        return instance



class PostLikeSerializer(serializers.ModelSerializer):
    """ POST LIKE SERIALIZER """
    user = serializers.CharField(read_only=True)

    class Meta:
        model = PostLike
        fields = '__all__'
        read_only = ['user']

    def create(self, validated_data):
        post = validated_data.get('post', None)
        user = self.context.get('request').user
        like, created = PostLike.objects.get_or_create(user=user, post=post)
        return like