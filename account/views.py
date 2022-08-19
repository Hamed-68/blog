from account.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from account.permissions import CreateOrNeedAuthenticate



class UserViewset(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [CreateOrNeedAuthenticate]