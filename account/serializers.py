from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import UserFollow, Profile
from post.serializers import PostWithoutCommentsSerializer
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



class ProfileSerializer(serializers.ModelSerializer):
    """
    PROFILE SERIALIZER FOR USER 
    """
    class Meta:
        model = Profile
        fields = ['photo',]



class RawUserSerializer(serializers.ModelSerializer):
    """ USER SERIALIZER WITHOUT NESTED SERIALIZERS. """
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'profile']
        lookup_field = 'username'



class UserSerializer(serializers.ModelSerializer):
    """USER SERIALIZER"""
    confirm_password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()
    post_set = serializers.SerializerMethodField('paginated_posts')
    following = serializers.SerializerMethodField('paginated_following')
    followers = serializers.SerializerMethodField('paginated_followers')

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'profile', 'post_set', 'followers', 'following',
                  'password', 'confirm_password']
        lookup_field = 'username'
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': lookup_field}
        }

    def paginated_posts(self, obj):     # paginate users posts
        size = self.context['request'].query_params.get('size') or 5
        page = self.context['request'].query_params.get('page') or 1
        paginate = Paginator(obj.post_set.all(), size)
        try:
            posts = paginate.page(page)
        except:
            posts = paginate.page(1)
        serializer = PostWithoutCommentsSerializer(posts, many=True)
        return serializer.data

    def paginated_following(self, obj):     # paginate users following
        following_size = self.context['request'].query_params.get('following_size') or 5
        following_page = self.context['request'].query_params.get('following_page') or 1
        paginate = Paginator(obj.following.all(), following_size)
        try:
            following = paginate.page(following_page)
        except:
            following = paginate.page(1)
        serializer = UserFollowingSerializer(following, many=True)
        return serializer.data

    def paginated_followers(self, obj):     # paginate users followers
        follower_size = self.context['request'].query_params.get('follower_size') or 5
        follower_page = self.context['request'].query_params.get('follower_page') or 1
        paginate = Paginator(obj.followers.all(), follower_size)
        try:
            followers = paginate.page(follower_page)
        except:
            followers = paginate.page(1)
        serializer = UserFollowingSerializer(followers, many=True)
        return serializer.data

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                                    "password and confirm_password didn't match!")
        return super(UserSerializer, self).validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        profile = validated_data.pop('profile')
        user = get_user_model().objects.create_user(**validated_data)
        if profile['photo']:  # add profile photo
            Profile.objects.create(user=user, photo=profile['photo'])
        else:
            Profile.objects.create(user=user, photo=None)
        return user

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        if profile['photo']:  # change profile photo
            instance.profile.delete()
            Profile.objects.create(user=instance, photo=profile['photo'])
        instance.save()
        return super(UserSerializer, self).update(instance, validated_data)