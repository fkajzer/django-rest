from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from postings.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


# automated
# blank db
User = get_user_model()

class BlogPostAPITestCare(APITestCase):
    def setUp(self):
        user_obj = User(username='testcase', email='test@case.com')
        user_obj.set_password('fuff')
        user_obj.save()

        blog_post = BlogPost.objects.create(
                        user=user_obj,
                        title='test title',
                        content='test content')

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        count = BlogPost.objects.count()
        self.assertEqual(count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse('api-postings:post-create')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item(self):
        post = BlogPost.objects.first()
        url = post.get_api_url()
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        post = BlogPost.objects.first()
        url = post.get_api_url()
        data = {'title': 'test_post_item', 'content': 'test_post_item'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_item_authorized(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        data = {'title': 'test_post_item', 'content': 'test_post_item'}
        url = api_reverse('api-postings:post-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_item_authorized(self):
        post = BlogPost.objects.first()
        url = post.get_api_url()
        data = {'title': 'test_post_item', 'content': 'test_post_item'}

        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_ownership(self):
        owner = User(username='testcase2', email='test2@case.com')
        owner.save()
        blog_post = BlogPost.objects.create(
                        user=owner,
                        title='test title',
                        content='test content')

        url = blog_post.get_api_url()
        data = {'title': 'test_post_item', 'content': 'test_post_item'}

        user_obj = User.objects.first()
        self.assertNotEqual(owner, user_obj)

        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_login_and_update(self):
        data = {
            'username': 'testcase',
            'password': 'fuff'
        }
        url = api_reverse('api-login')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if response.data.get('token') is not None:
            post = BlogPost.objects.first()
            url = post.get_api_url()

            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data.get('token'))
            data = {'title': 'test_api_login_and_update', 'content': 'test_api_login_and_update'}
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
