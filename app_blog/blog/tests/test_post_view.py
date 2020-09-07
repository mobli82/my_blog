from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from blog.views import UserPostsListView, PostCreateView
from blog.models import Post

import json
import mock

class TestPostsListView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Mick',
                                            email='mick@company.com',
                                            password='123tester')
        self.user.save()
        self.login = self.client.login(username='Mick', password='123tester')
        self.post = Post.objects.create(
            title='First Post',
            content='Some content',
            author=self.user
        )
    
    def tearDown(self):
        self.post.delete()
        self.user.delete()

    def test_posts_list_GET(self):
        response = self.client.get('/blog/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts_blog.html')
    
    def test_post_detail_GET(self):
        response = self.client.get(f'/blog/post-detail/{self.post.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_add_new_user_post_success(self):
        data = {
            'title': 'New Post',
            'content': 'content new',
            'author': self.user
        }
        request = self.client.post(f'/blog/post-create/', data=data)

        response = self.client.get('/blog/posts/')

        # print(response.context)

        self.assertEqual(request.status_code, 302)
        self.assertEqual(Post.objects.all().last().title, 'New Post')
    
    def test_add_user_post_fail(self):
        data = {
            'title': '',
            'content': '',
            'author': ''
        }
        request = self.client.post(f'/blog/post-create/', data=data)

        response = self.client.get('/blog/posts/')
        
        # print(response.context)

        num_of_posts = list(response.context['posts'])
    
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Post.objects.all().count(), len(num_of_posts))
    
    def test_user_post_delete_success(self):
        # deletion post succes
        total_posts = Post.objects.all().count()

        post = Post.objects.first()
        request = self.client.delete(f'/blog/post-delete/{post.id}/')
        
        new_total_posts = Post.objects.all().count()

        self.assertEqual(request.status_code, 302)
        self.assertEqual(total_posts - 1, new_total_posts)

    def test_user_post_delete_no_pk(self):
        # deletion post fail
        # with self.assertRaises(TypeError):
        request =self.client.delete(f'/blog/post-delete/{None}/')

        self.assertEqual(request.status_code, 404)
    
    def test_user_post_list_view(self):
        user = User.objects.get(username='Mick')

        Post.objects.bulk_create([
            Post(
                title='Post nr 1',
                content='Some content 1',
                author=user,
            ),
            Post(
                title='Post nr 2',
                content='Some content 2',
                author=user,
            ),
            Post(
                title='Post nr 3',
                content='Some content 3',
                author=user,
            ),
            Post(
                title='Post nr 4',
                content='Some content 4',
                author=user,
            ),
        ])

        self.assertTrue(isinstance(user, User))
        response = self.client.get(reverse('posts-user', kwargs={'username': user.username}))

        qset = Post.objects.all().filter(author=user).order_by('-date_posted')
        # print(dir(qset))
        qset = list(qset)
        # print(response.context)
        self.assertEquals(response.status_code, 200)
        # self.assertEquals(qset, list(response.context['posts']))
    
    def test_update_user_post(self):
        post = Post.objects.get(title='First Post')
        # print(post)
        # response = self.client.post(reverse('post-update', kwargs={'pk': post.id}), 
        #                                     data={'title': 'First Post Updated'})
        
        response = self.client.post(f'/blog/post-update/{post.id}/', 
                                    data={'title': 'First Post Updated',
                                          'content':'some content',
                                          'author': post.author})
        
        request = self.client.get(f'/blog/post-detail/{ post.id}/')
        
        # print(request.context['post'])
        self.assertEqual(request.status_code, 200)
        self.assertEqual(response.status_code, 302)
        
        # print(Post.objects.all())
        print(request.content)
        self.assertEqual(request.context['post'].title, 'First Post Updated')
        self.assertFalse(post.id == request.context['user'].id)
        
        """" FIX THAT assert !!!"""
        # self.assertContains(request.content, f'{post.title} has been Updated')