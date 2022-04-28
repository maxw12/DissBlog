from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse


class TestCallsCore(TestCase):
    """
    Tests for login/register/logout
    """
    def setUp(self):
        """
        Setting up a test user.
        """
        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='hw578', first_name='haoyu', last_name='wang', date_of_birth='2000-05-12',
                                        email='hw578@exeter.ac.uk', password='ExeterUni19', type='2')
        self.client = Client()

    def test_call_login(self):
        """
        If post request has correct info then redirect to home page otherwise checks if renders login template.
        """
        # checking for get
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '#core/login.html')
        # checking for post request
        response_post = self.client.post(reverse('login'), {'username': 'test', 'password': 'test'})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, '/')
        # checking for post request with invalid info
        response_post_invalid = self.client.post(reverse('login'), {'username': 'test', 'password': 'invalid'})
        self.assertEqual(response_post_invalid.status_code, 302)
        self.assertRedirects(response_post_invalid, '/')

    def test_call_register(self):
        """
        If post request then tests for redirect to login page or register page depending on whether info is correct
        and filled otherwise checks if renders register page.
        """
        # checking for get
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')
        # checking for post
        response_post = self.client.post(reverse('register'), {'username': 'test', 'password': 'test'})
        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'core/register.html')
