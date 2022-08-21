from account.serializers import(UserSerializer, 
                            UserFollowersSerializer,
                            UserFollowingSerializer)
from account.models import UserFollow
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from account.permissions import CreateOrNeedAuthenticate



class UserViewset(ModelViewSet):
    """USER VIEW"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [CreateOrNeedAuthenticate]



class UserFollowersViewset(ModelViewSet):
    """USER FOLLOWERS VIEW"""
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowersSerializer

    def perform_create(self, serializer):
        follower = self.request.user
        serializer.save(user_id=follower)



class UserFollowingViewset(ModelViewSet):
    """USER FOLLOWING VIEW"""
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowingSerializer

    def perform_create(self, serializer):
        follower = self.request.user
        serializer.save(user_id=follower)
        