from django.test import TestCase, RequestFactory
from blogtest.models import User, Submission, Course
from django.utils import timezone
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='hw578', first_name='haoyu', last_name='wang', date_of_birth='2000-05-12',
                                        email='hw578@exeter.ac.uk', password='ExeterUni19', type='2')
        self.assertEqual(user.email, 'hw578@exeter.ac.uk')
        self.assertEqual(user.username, 'hw578')
        self.assertEqual(user.first_name, 'haoyu')
        self.assertEqual(user.last_name, 'wang')
        self.assertEqual(user.date_of_birth, '2000-05-12')
        self.assertEqual(user.type, '2')


class SubmissionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        course = Course.objects.create(name='History')
        user = User.objects.create_user(username='hw578', first_name='haoyu', last_name='wang',
                                        date_of_birth='2000-05-12',
                                        email='hw578@exeter.ac.uk', password='ExeterUni19', type='2')
        submission = Submission.objects.create(title='testSubmission', tag=course,
                                               file='media/max_generated_resume.pdf',
                                               content='modeltest', author=user, pub_date='2022-04-12')

    def test_absolute_url(self):
        submission = Submission.objects.get(id=1)
        self.assertEqual(submission.get_absolute_url(), '/')

    def test_object_name_is_title_plus_author(self):
        submission = Submission.objects.get(id=1)
        expected = str(submission.title) + ' | ' + str(submission.author)
        self.assertEqual(str(submission.title) + str(' | ') + str(submission.author), expected)