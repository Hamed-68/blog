from django.contrib import admin
from post.models import Post, Comment, Images, PostLike


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    list_editable = ['author', 'status']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Images)
admin.site.register(PostLike)