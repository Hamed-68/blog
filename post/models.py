from django.db import models
from django.conf import settings



class PostLike(models.Model):
    """ LIKE MODEL"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                            related_name='likes')
    date_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post}."



class Post(models.Model):
    """ POST MODEL """
    PUBLISH = "PU"
    DRAFT = "DR"
    ARCHIVE = "AR"
    PUBLISH_CHOICES = [
        (PUBLISH, "Publish"),
        (DRAFT, "Draft"),
        (ARCHIVE, "Archive"),
    ]
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(allow_unicode=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=PUBLISH_CHOICES, default=PUBLISH)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique post title for user')
        ]
        ordering = ['-created']
    
    @property
    def get_likes(self):
        return PostLike.objects.filter(post=self).count()



class Images(models.Model):
    """
    IMAGES CLASS.
    by this model, posts could have multi images.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images')
    image = models.FileField(upload_to='post_medias',
                              null=True)
    def __str__(self):
        return f'{self.post.title} images'



class Comment(models.Model):
    """ COMMENT MODEL """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='owner')
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15]

    class Meta:
        ordering = ('-created',)