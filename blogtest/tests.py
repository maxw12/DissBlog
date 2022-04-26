from django.test import TestCase, RequestFactory
from .models import User

from blogtest.views import DetailView, HomeView


class UnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='hw578', email='hw578@exeter.ac.uk', password='ExeterUni19', type='2')

    def test_details(self):
        request = self.factory.get('')
        request.user = self.user
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class HomePageTest(TestCase):
    def test_environment_set_in_context(self):
        request = RequestFactory().get('submission/')
        view = DetailView()
        view.setup(request)

        context = view.get_context_data()
        self.assertIn('comment', context)
