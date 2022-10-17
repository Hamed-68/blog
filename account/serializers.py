from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import UserFollow
from post.serializers import PostSerializer
from django.core.paginator import Paginator



class UserFollowersSerializer(serializers.ModelSerializer):
    """USER FOLLOWERS SERIALIZER """
    following_user_id = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        many=False
    )
    user = serializers.ReadOnlyField(source='user_id.username')

    class Meta:
        model = UserFollow
        fields = ['id', 'user', 'following_user_id', 'created']


class UserFollowingSerializer(serializers.ModelSerializer):
    """USER FOLLOWING SERIALIZER"""
    following_user_id = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all(),
        many=False
    )
    user = serializers.ReadOnlyField(source='user_id.username')

    class Meta:
        model = UserFollow
        fields = ['id', 'user', 'following_user_id', 'created']



class UserSerializer(serializers.ModelSerializer):
    """USER SERIALIZER"""
    confirm_password = serializers.CharField(write_only=True)
    post_set = serializers.SerializerMethodField('paginated_posts')
    following = serializers.SerializerMethodField('paginated_following')
    followers = serializers.SerializerMethodField('paginated_followers')

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'post_set', 'followers', 'following',
                  'password', 'confirm_password']
        lookup_field = 'username'
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': lookup_field}
        }

    def paginated_posts(self, obj):     # paginate users posts
        limit = self.context['request'].query_params.get('limit') or 1
        paginate = Paginator(obj.post_set.all(), limit)
        offset = self.context['request'].query_params.get('offset') or 1
        posts = paginate.page(offset)
        serializer = PostSerializer(posts, many=True)
        return serializer.data

    def paginated_following(self, obj):     # paginate users following
        limit = self.context['request'].query_params.get('limit') or 1
        paginate = Paginator(obj.following.all(), limit)
        offset = self.context['request'].query_params.get('offset') or 1
        following = paginate.page(offset)
        serializer = UserFollowingSerializer(following, many=True)
        return serializer.data

    def paginated_followers(self, obj):     # paginate users followers
        limit = self.context['request'].query_params.get('limit') or 1
        paginate = Paginator(obj.followers.all(), limit)
        offset = self.context['request'].query_params.get('offset') or 1
        followers = paginate.page(offset)
        serializer = UserFollowingSerializer(followers, many=True)
        return serializer.data

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                                    "password and confirm_password didn't match!")
        return super(UserSerializer, self).validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)