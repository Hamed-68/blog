from django.db import models
from django.conf import settings


# ================================ POST MODEL ===============================
class Post(models.Model):
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
    slug = models.SlugField(unique=True)
    body = models.TextField()
    picture = models.ImageField(blank=True, null=True, upload_to="post_pics")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=PUBLISH_CHOICES, default=DRAFT)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique post title for user')
        ]
        ordering = ['-created']

# ================================ COMMENT MODEL ===============================
class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='owner')
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:15]

    class Meta:
        ordering = ('-created',)