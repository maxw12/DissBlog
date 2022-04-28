from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory


class TestLoggedOutURLS(TestCase):
    """
    Testing URLS for before loggin in
    """
    def setUp(self):
        self.factory = RequestFactory()
        # testUser = get_user_model()
        # self.user = testUser.objects.create_user(username='hw578', first_name='haoyu', last_name='wang', date_of_birth='2000-05-12',
        #                                 email='hw578@exeter.ac.uk', password='ExeterUni19', type='2')
        self.client = Client()

    # test when not logged in
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_submit_page(self):
        response = self.client.get('/submit/')
        self.assertEqual(response.status_code, 302)

    def test_my_submission_page(self):
        response = self.client.get('/mysubmission/')
        self.assertEqual(response.status_code, 302)


class TestLoggedInURLS(TestCase):
    """
    Testing URLS for after loggin in
    """
    def setUp(self):
        self.factory = RequestFactory()
        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='hw578', first_name='haoyu', last_name='wang', date_of_birth='2000-05-12',
                                        email='hw578@exeter.ac.uk', password='ExeterUni19', type='2')
        self.client = Client()
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

        # testing login
        response_login = self.client.post('/login/', {'username': 'hw578', 'password': 'ExeterUni19'})
        self.assertEqual(response_login.status_code, 302)

    # def test_login_page(self):
    #     response = self.client.get('/login/')
    #     self.assertEqual(response.status_code, 200)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_submit_page(self):
        response = self.client.get('/submit/')
        self.assertEqual(response.status_code, 200)

    def test_my_submission_page(self):
        response = self.client.get('/mysubmission/')
        self.assertEqual(response.status_code, 200)

    # def test_detail_submission_page(self):
    #     response = self.client.get('/submission/<int:pk>')
    #     self.assertEqual(response.status_code, 200)
