import time
from datetime import datetime, timedelta

import factory
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from rest_framework.test import APITestCase

from posts.models import Post, Like
from users.models import User


class UserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.user2 = User.objects.create(username='test2')
        cls.user_activity_view_name = 'user_activity'
        cls.analytics_view_name = 'analytics'
        cls.rest_login_view_name = 'rest_login'
        cls.users_view_name = 'user-list'
        cls.post1 = Post.objects.create(posted_by=cls.user, text=factory.Faker('text').generate())
        cls.post2 = Post.objects.create(posted_by=cls.user2, text=factory.Faker('text').generate())
        cls.post3 = Post.objects.create(posted_by=cls.user, text=factory.Faker('text').generate())

        Like.objects.bulk_create([
            Like(is_active=True, post=cls.post1, user=cls.user),
            Like(is_active=True, post=cls.post2, user=cls.user),
            Like(is_active=True, post=cls.post3, user=cls.user),
            Like(is_active=True, post=cls.post1, user=cls.user2),
            Like(is_active=True, post=cls.post2, user=cls.user2),
            Like(is_active=True, post=cls.post3, user=cls.user2),
        ])
        Like.objects.filter(user=cls.user).update(created=timezone.now() - timedelta(days=4))

    def test_analytics(self):
        self.client.force_authenticate(user=self.user)
        date_from = (timezone.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        date_to = (timezone.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.get(reverse(self.analytics_view_name), {'date_from': date_from, 'date_to': date_to})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.json()['likes_count'])

        response = self.client.get(reverse(self.analytics_view_name), {'user': self.user.guid})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.json()['likes_count'])

    def test_user_signup_and_analytics(self):
        # Anonymous
        user_data = {
            "email": factory.Faker('email').generate(),
            "first_name": factory.Faker('first_name').generate(),
            "last_name": factory.Faker('last_name').generate(),
            "password": factory.Faker('password').generate(),
            "username": factory.Faker('word').generate()
        }
        response = self.client.post(reverse(self.users_view_name), data=user_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        time_before_login = timezone.now().replace(tzinfo=None)
        login_data = {
            'username': user_data['username'],
            'password': user_data['password'],
        }
        time.sleep(1)
        login = self.client.post(reverse(self.rest_login_view_name), data=login_data, format='json')
        self.assertEqual(status.HTTP_200_OK, login.status_code)
        time.sleep(1)
        time_after_login = timezone.now().replace(tzinfo=None)

        # Logged in
        self.client.force_authenticate(user=self.user)
        user_activity = self.client.get(reverse(self.user_activity_view_name, args=[login.json()['user']['pk']]))
        last_login = datetime.strptime(user_activity.json()['last_login'], '%Y-%m-%d %H:%M:%S')

        self.assertTrue(time_before_login < last_login < time_after_login)
