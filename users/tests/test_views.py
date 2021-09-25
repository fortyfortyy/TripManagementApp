import pytest
from django.urls import reverse
from django.test import TestCase
from django.test import Client

from trips.models import Profile


@pytest.mark.django_db
def test_create_user(client, create_user):
    test_user = Profile.objects.create_user(email='fake@fake.com', password='Fake_password1', username='fake_username')
    test_user.save()
    assert test_user.is_authenticated is True
    profile = Profile.objects.get(email='fake@fake.com')
    assert test_user.email == profile.email


class LogoutViewTest(TestCase):
    def setUp(self):
        test_user1 = Profile.objects.create_user(email='fake@fake.com', username='testuser1', password='Fakepassoword1')
        test_user1.save()

    def test_for_login_logout_redirect_and_template(self):
        # Create Client
        self.c = Client()
        # Try to call the Restricted View as Anonymous
        response = self.c.get(reverse('logout'))
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
        response = self.c.get(reverse('logout'))
        # Check for HTTPResponse 200
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'trips/trip-plans.html')

        response = self.client.get('/accounts/logout/')
        self.assertEquals(response.status_code, 200)

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/accounts/logout/')
        self.assertEquals(response.status_code, 304)
