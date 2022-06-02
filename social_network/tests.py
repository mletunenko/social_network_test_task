from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .factorys import UserFactory, PostFactory
from .models import Post


class RegistrationTest(APITestCase):
    def test_user_registration(self):
        user = UserFactory()

        data = {
            "username": user.username + '_test',
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
        response = self.client.post('/registration/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_registration_no_password(self):
        user = UserFactory()
        data = {
            "username": user.username + '_test',
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        response = self.client.post('/registration/', data=data)
        self.assertEqual(response.status_code, 400)


class AuthenticationTests(APITestCase):
    def test_post_get_token(self):
        user = UserFactory()
        data = {
            "username": user.username,
            "password": user.username
        }
        response = self.client.post('/token/', data=data)
        self.assertEqual(bool(response.data['access']), True)
        self.assertEqual(bool(response.data['refresh']), True)


class PostTest(APITestCase):
    def test_post_new_post(self):
        user = UserFactory()
        self.client.force_login(user)
        post = PostFactory()
        data = {
            "title": post.title,
            "content": post.content
        }
        response = self.client.post('/post/', data=data)
        self.assertEqual(response.status_code, 201)
        post = Post.objects.get(id=response.data['id'])
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.content, data['content'])
        self.assertEqual(post.author_id, user.id)

    def test_put_post(self):
        post = PostFactory()
        user = post.author
        self.client.force_login(user)
        data = {
            "title": f'New {post.title}',
            "content": f'New {post.content}'
        }
        response = self.client.put(reverse('post-detail', args=(post.id,)), data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_post(self):
        post = PostFactory()
        user = post.author
        self.client.force_login(user)
        data = {
            "title": f'New {post.title}'
        }
        response = self.client.patch(reverse('post-detail', args=(post.id,)), data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_like(self):
        post = PostFactory()
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('post-like', args=(post.id,)))
        self.assertEqual(response.status_code, 200)

    def test_post_unlike(self):
        post = PostFactory()
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(reverse('post-like', args=(post.id,)))
        response = self.client.post(reverse('post-unlike', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
