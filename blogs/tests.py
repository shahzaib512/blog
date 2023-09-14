from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User

class BlogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post = Post.objects.create(
            title='Test Title',
            author=self.user,
            body='Test Body Content'
        )

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        expected_author = f'{self.user}'
        expected_title = 'Test Title'
        expected_body = 'Test Body Content'
        self.assertEqual(expected_author, str(post.author))
        self.assertEqual(expected_title, post.title)
        self.assertEqual(expected_body, post.body)

    def test_blog_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')
        self.assertTemplateUsed(response, 'home.html')

    def test_blog_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Title')
        self.assertTemplateUsed(response, 'post_detail.html')
