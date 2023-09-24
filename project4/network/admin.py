from django.contrib import admin
from .models import User, Post, Like, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user')


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", )


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user',)


# Register your models here.
admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
