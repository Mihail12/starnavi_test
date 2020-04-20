import factory

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from users.models import User


class PostAndLikeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.user2 = User.objects.create(username='test2')
        cls.posts_view_name = 'post-list'
        cls.post_view_name = 'post-detail'
        cls.likes_view_name = 'like-list'
        cls.like_view_name = 'like-detail'
        cls.post = Post.objects.create(posted_by=cls.user, text=factory.Faker('text').generate())

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        post_data = {
            'text': factory.Faker('text').generate()
        }
        response = self.client.post(reverse(self.posts_view_name), data=post_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(post_data['text'], response.json()['text'])
        self.assertEqual(str(self.user.guid), response.json()['posted_by'])

    def test_like_and_unlike_post(self):
        like_data = {
            'post': self.post.guid,
            'is_active': True,
        }
        like_response = self.client.post(reverse(self.likes_view_name), data=like_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, like_response.status_code)
        liked_post_response = self.client.get(reverse(self.post_view_name, args=[self.post.guid]), format='json')
        self.assertEqual(1, liked_post_response.json()['likes'])

        unlike_data = {
            'post': self.post.guid,
            'is_active': False,
        }
        resp = self.client.put(reverse(self.like_view_name, args=[like_response.json()['id']]), data=unlike_data, format='json')
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        unliked_post_response = self.client.get(reverse(self.post_view_name, args=[self.post.guid]), format='json')
        self.assertEqual(0, unliked_post_response.json()['likes'])

    def test_likes_from_different_users(self):
        like_data = {
            'post': self.post.guid,
            'is_active': True,
        }
        like_response = self.client.post(reverse(self.likes_view_name), data=like_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, like_response.status_code)

        self.client.force_authenticate(user=self.user2)
        like_data = {
            'post': self.post.guid,
            'is_active': True,
        }
        like_response = self.client.post(reverse(self.likes_view_name), data=like_data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, like_response.status_code)

        liked_post_response = self.client.get(reverse(self.post_view_name, args=[self.post.guid]), format='json')
        self.assertEqual(2, liked_post_response.json()['likes'])
