from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from posts.api import PostViewSet, LikeViewSet

router_post = routers.DefaultRouter()
router_post.register(r'posts', PostViewSet)

router_like = routers.DefaultRouter()
router_like.register(r'likes', LikeViewSet)

urlpatterns = [
    url(r'^', include(router_post.urls)),
    url(r'^', include(router_like.urls)),
]
