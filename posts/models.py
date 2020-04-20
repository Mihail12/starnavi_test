import uuid

from django.conf import settings
from django.db import models


class BaseCreatedModifiedModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseCreatedModifiedModel):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like')


class Like(BaseCreatedModifiedModel):
    is_active = models.BooleanField(default=True)  # if True like is posted, if False unliked
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post', 'is_active')
