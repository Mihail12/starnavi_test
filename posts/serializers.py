from rest_framework import serializers

from posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('url', 'posted_by', 'text', 'guid', 'likes')
        extra_kwargs = {'posted_by': {'read_only': True}, 'guid': {'read_only': True}}

    @staticmethod
    def get_likes(obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('url', 'is_active', 'user', 'post')
        extra_kwargs = {'user': {'read_only': True},}
