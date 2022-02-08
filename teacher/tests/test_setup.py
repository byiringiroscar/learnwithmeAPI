from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetup(APITestCase):
    def setUp(self):
        self.register_teacher_url = reverse('registerteacher')
        self.login_teacher_url = reverse('login-teacher')
        self.fake = Faker()
        self.user_data = {
            'first_name': self.fake.email().split('@')[0],
            'last_name': self.fake.email().split('@')[0],
            'email': self.fake.email(),
            'phone_number': '+250786405253',
            'password': 'password1234',
            'password2': 'password1234',
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
