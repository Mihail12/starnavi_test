from django.contrib import admin
from django.db.models import Prefetch

from posts.models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('guid', 'posted_by', 'text', 'likes')

    def likes(self, obj):
        return obj.likes.count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related(
            Prefetch('likes', queryset=Like.objects.filter(is_active=True))
        )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'post', 'user')
    list_filter = ('is_active', )
    list_editable = ('is_active', )
