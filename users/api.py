from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Like
from users.models import User
from users.permissions import IsLoggedInUserOrAdmin
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AnalyticsAPI(APIView):
    def get(self, request, *args, **kwargs):
        likes = Like.objects.all()
        if request.query_params.get('post'):
            likes = likes.filter(post=request.query_params['post'])
        if request.query_params.get('user'):
            likes = likes.filter(user=request.query_params['user'])
        if request.query_params.get('date_from'):
            date_from = datetime.strptime(request.query_params['date_from'], '%Y-%m-%d')
            likes = likes.filter(created__gt=date_from)
        if request.query_params.get('date_to'):
            date_to = datetime.strptime(request.query_params['date_to'], '%Y-%m-%d')
            likes = likes.filter(created__lt=date_to)
        data = {'likes_count': likes.count()}
        return Response(data, status=status.HTTP_200_OK)


class UserActivityAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if kwargs.get('pk'):
            user = get_object_or_404(User, pk=kwargs['pk'])
        data = {
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'never',
            'last_request_at': user.last_request_at.strftime('%Y-%m-%d %H:%M') if user.last_request_at else 'never'
        }
        return Response(data, status=status.HTTP_200_OK)
