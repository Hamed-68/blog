from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import UserFollow
from post.serializers import PostSerializer



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
    post_set = PostSerializer(many=True, read_only=True)
    followers = UserFollowersSerializer(many=True, read_only=True)
    following = UserFollowingSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'post_set', 'followers', 'following',
                  'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

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