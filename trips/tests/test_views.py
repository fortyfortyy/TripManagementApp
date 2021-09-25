from django.urls import reverse
from django.test import TestCase
from django.test import Client

from trips.forms import TripPlanCreateEditForm
from trips.models import Profile


class TripPlansViewTest(TestCase):
    def setUp(self):
        test_user1 = Profile.objects.create_user(email='fake@fake.com', username='testuser1', password='Fakepassoword1')
        test_user1.save()

    def test_for_login_redirect_and_template(self):
        # Create Client
        self.c = Client()
        # Try to call the Restricted View as Anonymous
        response = self.c.get(reverse('trip-plans'))
        # Check for Login Promt Redirection
        self.assertRedirects(response, '/accounts/login/?next=/')

        # Get Userobject
        self.user = Profile.objects.get(username="testuser1")
        # Login with the Client
        login = self.c.login(username='testuser1', password='Fakepassoword1')
        # Check our user is logged in
        self.assertTrue(login)
        # Check for our username
        self.assertEqual(self.user.username, 'testuser1')

        # Try to call the View as logged in User again
        response = self.c.get(reverse('trip-plans'))
        # Check for HTTPResponse 200
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'trips/trip-plans.html')


class TripPlanCreateViewTest(TestCase):
    def setUp(self):
        test_user1 = Profile.objects.create_user(email='fake@fake.com', username='testuser1', password='Fakepassoword1')
        test_user1.save()

    def test_for_login_redirect_forms_and_template(self):
        # Create Client
        self.c = Client()
        # Try to call the Restricted View as Anonymous
        response = self.c.get(reverse('trip-plans'))
        # Check for Login Promt Redirection
        self.assertRedirects(response, '/accounts/login/?next=/')

        # Get Userobject
        self.user = Profile.objects.get(username="testuser1")
        # Login with the Client
        login = self.c.login(username='testuser1', password='Fakepassoword1')
        # Check our user is logged in
        self.assertTrue(login)
        # Check for our username
        self.assertEqual(self.user.username, 'testuser1')

        # Try to call the View as logged in User again
        response = self.c.get(reverse('create-trip-plan'))
        # Check for HTTPResponse 200
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'trips/trip-plan-create-form.html')

        # Check its used correct form
        self.assertEqual(response.context['form'], TripPlanCreateEditForm())
