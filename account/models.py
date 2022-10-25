from django.db import models
from django.contrib.auth import get_user_model



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photo', null=True)

    def __str__(self):
        return f'profile {self.user.username}'



class UserFollow(models.Model):
    user_id = models.ForeignKey(get_user_model(), 
                                related_name='following', 
                                on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(get_user_model(), 
                                related_name='followers', 
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'following_user_id'],
                name='users follow eachother one time'
            )
        ]

    def __str__(self):
        return f'{self.user_id} is following {self.following_user_id}'