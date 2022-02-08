from .test_setup import TestSetup
from teacher.models import User


class TestViews(TestSetup):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_teacher_url)
        self.assertAlmostEqual(res.status_code, 400)

    def test_user_can_register_with_data(self):
        res = self.client.post(self.register_teacher_url, self.user_data, format="json")
        # import pdb
        # pdb.set_trace()
        self.assertAlmostEqual(res.data['email'], self.user_data[
            'email'])  # to ensure server can send us user email after register account
        self.assertAlmostEqual(res.data['first_name'], self.user_data['first_name'])
        # import pdb
        # pdb.set_trace()
        self.assertAlmostEqual(res.status_code, 201)

    def test_user_can_login_with_unverified_email(self):
        self.client.post(self.register_teacher_url, self.user_data, format="json")
        res = self.client.post(self.login_teacher_url, self.user_data, format="json")
        # import pdb
        # pdb.set_trace()
        self.assertAlmostEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        response = self.client.post(self.register_teacher_url, self.user_data, format="json")
        email = response.data['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_teacher_url, self.user_data, format="json")
        # import pdb
        # pdb.set_trace()
        self.assertAlmostEqual(res.status_code, 200)
