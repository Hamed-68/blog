from account.serializers import(UserSerializer,
                            UserFollowingSerializer,
                            RawUserSerializer)
from account.models import UserFollow
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from account.permissions import CreateOrNeedAuthenticate
from rest_framework.permissions import IsAuthenticated


class UserViewset(ModelViewSet):
    """USER VIEW"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [CreateOrNeedAuthenticate]
    lookup_field = 'username'

    def get_serializer_class(self):  # users list without extra info
        if hasattr(self, 'action') and self.action == 'list':
            return RawUserSerializer
        return self.serializer_class



class UserFollowingViewset(ModelViewSet):
    """USER FOLLOWING VIEW"""
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follower = self.request.user
        serializer.save(user_id=follower)
