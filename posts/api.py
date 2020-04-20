from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Like
from posts.serializers import LikeSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().prefetch_related(
            Prefetch('likes', queryset=Like.objects.filter(is_active=True))
        )

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
