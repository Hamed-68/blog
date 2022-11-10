from account.serializers import(UserSerializer,
                            UserFollowingSerializer,
                            RawUserSerializer)
from account.models import UserFollow
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from account.permissions import CreateOrNeedAuthenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response



class UserViewset(ModelViewSet):
    """USER VIEW"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [CreateOrNeedAuthenticate]
    lookup_field = 'username'

    def get_serializer_class(self):  
        # use different serializer for list and update action
        if hasattr(self, 'action') and (
            self.action == 'list' or self.action == 'update'):
            return RawUserSerializer
        return self.serializer_class



class UserFollowingViewset(ModelViewSet):
    """USER FOLLOWING VIEW"""
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def following(self, request, pk):    # retrieve following 
        following = UserFollow.objects.filter(user_id=pk)
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk):    # retrieve followers
        followers = UserFollow.objects.filter(following_user_id=pk)
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        follower = self.request.user
        serializer.save(user_id=follower)
