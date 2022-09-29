import base64
import json

from django.conf import settings

from rest_framework.test import APITestCase


from mockfirestore import MockFirestore
from django.contrib.auth.models import User as A_User
from rest_framework import HTTP_HEADER_ENCODING

from .models import User
from datetime import datetime, timedelta


class UsersTest(APITestCase):
    def setUp(self):
        settings.DEFAULT_APP = MockFirestore()
        settings.IS_TESTING = True

        self.email_test = "test@test.test"
        self.pwd_test = "123456"
        self.user = A_User.objects.create_user(username=self.email_test, password=self.pwd_test)
        self.credentials = f"{self.email_test}:{self.pwd_test}"
        self.base64_credentials = base64.b64encode(
            self.credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)

    def test_create_user(self):
        email = "test42@test.test"
        pw = "123456"
        data = {"email": email, "password": pw}
        url = "/polls/create_user"
        response = self.client.post(url, data, format='json')

        print(response)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_user_field_missing(self):
        data = {"password": "no-email"}
        url = "/polls/create_user"
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_verify_user(self):
        code = 1234
        code_end_on = datetime.today() + timedelta(minutes=1)
        user = User().create(data={"email": self.email_test, "code": code,
                                   "code_end_on": code_end_on.timestamp()})

        data = {"digit_code": code}

        url = "/polls/verify_user"
        resp = self.client.post(url, data=data, HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}",
                                format="json")
        self.assertEqual(resp.status_code, 200)
        updated_user = json.loads(resp.content)
        self.assertEqual(updated_user["status"], "active")
        self.assertTrue(updated_user["is_verified"])

    def test_verify_user_timeout(self):
        code = 1234
        code_end_on = datetime.today() - timedelta(minutes=1)
        user = User().create(data={"email": self.email_test, "code": code,
                                   "code_end_on": code_end_on.timestamp()})

        data = {"digit_code": code}

        url = "/polls/verify_user"
        resp = self.client.post(url, data=data, HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}",
                                format="json")
        self.assertEqual(resp.status_code, 400)
        msg = resp.content.decode()
        self.assertEqual(msg, "Token timeout")

    def test_verify_user_missing_field(self):
        code = 1234
        code_end_on = datetime.today() - timedelta(minutes=1)
        user = User().create(data={"email": self.email_test, "code": code,
                                   "code_end_on": code_end_on.timestamp()})

        data = {"missing-field": code}

        url = "/polls/verify_user"
        resp = self.client.post(url, data=data, HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}",
                                format="json")
        self.assertEqual(resp.status_code, 400)
        msg = resp.content.decode()
        self.assertEqual(msg, "Digit code is missing")

    def test_verify_user_wrong_code_type(self):
        code = 1234.213
        code_end_on = datetime.today() - timedelta(minutes=1)
        user = User().create(data={"email": self.email_test, "code": code,
                                   "code_end_on": code_end_on.timestamp()})

        data = {"digit_code": code}

        url = "/polls/verify_user"
        resp = self.client.post(url, data=data, HTTP_AUTHORIZATION=f"Basic {self.base64_credentials}",
                                format="json")
        self.assertEqual(resp.status_code, 400)
        msg = resp.content.decode()
        self.assertEqual(msg, "Something is wrong with the token")
        pass
