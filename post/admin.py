from django.contrib import admin
from post.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    list_editable = ['author', 'status']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
