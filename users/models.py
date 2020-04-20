import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    last_request_at = models.DateTimeField(null=True, blank=True)
