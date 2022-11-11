from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import UserFollow, Profile
from post.serializers import PostSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q



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
    profile_photo = serializers.ImageField(source='profile.photo', required=False)
    remove_profile_photo = serializers.BooleanField(
        required=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'profile_photo', 'remove_profile_photo']
        lookup_field = 'username'

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile', None)
        remove_profile_photo = validated_data.pop('remove_profile_photo', None)
        if profile:  # change profile photo
            instance.profile.delete()
            Profile.objects.create(user=instance, photo=profile['photo'])
        elif remove_profile_photo: # remove profile photo
            instance.profile.photo.delete()
        instance.save()
        return super(RawUserSerializer, self).update(instance, validated_data)



class UserSerializer(serializers.ModelSerializer):
    """USER SERIALIZER"""
    confirm_password = serializers.CharField(write_only=True)
    profile_photo = serializers.ImageField(source='profile.photo', required=False)
    followers = serializers.SerializerMethodField('count_followers')
    following = serializers.SerializerMethodField('count_following')
    # indicate request.user is in followers of this user.
    status_follow = serializers.SerializerMethodField()
    post_set = serializers.SerializerMethodField('paginated_posts')

    def get_status_follow(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                return UserFollow.objects.get(
                    Q(user_id=user) & Q(following_user_id=obj)
                ).id
            except UserFollow.DoesNotExist:
                return None
        return None

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'profile_photo', 'followers', 'following', 'status_follow',
                  'post_set', 'password', 'confirm_password']
        lookup_field = 'username'
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': lookup_field}
        }
    
    def count_followers(self, obj):
        return obj.followers.count()

    def count_following(self, obj):
        return obj.following.count()

    def paginated_posts(self, obj):     # paginate users posts
        size = self.context['request'].query_params.get('size') or 5
        page = self.context['request'].query_params.get('page') or 1
        paginate = Paginator(obj.post_set.all(), size)
        try:
            posts = paginate.page(page)
        except PageNotAnInteger:
            posts = paginate.page(1)
        except EmptyPage:
            posts = None
        serializer = PostSerializer(posts, many=True, context=self.context)
        return serializer.data

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                                    "password and confirm_password didn't match!")
        return super(UserSerializer, self).validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        profile = validated_data.pop('profile', None)
        user = get_user_model().objects.create_user(**validated_data)
        if profile:  # add profile photo
            Profile.objects.create(user=user, photo=profile['photo'])
        else:
            Profile.objects.create(user=user, photo=None)
        return user