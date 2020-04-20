from django.urls import reverse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TrackRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.path != reverse('user_activity'):
            request.user.last_request_at = timezone.now()
            request.user.save()
