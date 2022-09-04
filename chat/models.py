from django.db import models
from django.conf import settings



class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='sender',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='receiver',
                                 on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:10]