from rest_framework.viewsets import ModelViewSet
from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q



class ChatMessageViewset(ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(sender=self.request.user)