from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from .api import UserViewSet, AnalyticsAPI, UserActivityAPI

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    path('analytics/', AnalyticsAPI.as_view(), name='analytics'),
    path('user-activity/', UserActivityAPI.as_view(), name='user_activity'),
    path('user-activity/<str:pk>/', UserActivityAPI.as_view(), name='user_activity'),
]
