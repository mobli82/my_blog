from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase

from blog.models import Post

import mock

class TestBlogPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Cris')
        Post.objects.create(title='First Post',
                            content='dummy',
                            author=self.user,
                            date_posted='2020-09-05T08:24:42.067Z'
        )
        Post.objects.create(title='Second Post',
                            content='dummy2',
                            author=self.user,
                            date_posted='2020-09-04T08:24:42.067Z'
        )
        Post.objects.create(title='Third Post',
                            content='dummy3',
                            author=self.user,
                            date_posted='2020-09-03T08:24:42.067Z'
        )
    
    def test_isinstance_Post(self):
        post = Post.objects.get(title='Third Post')

        self.assertTrue(isinstance(post, Post))
    
    def test_return_string_from__str__method(self):
        post = Post.objects.get(title='First Post')
        self.assertEqual(str(post), post.title)
        self.assertIsInstance(post.title, str)
    
    def test_str_method(self):
        post = Post.objects.get(title='Second Post')
        self.assertEqual(post.__str__(), post.title)
    
    def test_title_label(self):
        post = Post.objects.get(title='First Post')
        title_label = post._meta.get_field('title').verbose_name

        self.assertEqual(title_label, 'title')
    
    def test_post_author(self):
        user = User.objects.get(username='Cris')
        post = Post.objects.get(title='First Post')

        self.assertEqual(post.author, user)

    def test_max_length_title(self):
        post = Post.objects.get(title='First Post')
        length = 100

        max_length = post._meta.get_field('title').max_length

        self.assertEqual(length, max_length)
    
    @mock.patch('blog.models.reverse')
    def test_return_absolute_url(self,reverse):
        post = Post.objects.get(title='First Post')
        reverse.return_value = 'post-detail/1'
        
        self.assertEqual('post-detail/1', post.get_absolute_url())
    
    def test_should_raise_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Post.objects.create(title=122)