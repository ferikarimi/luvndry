from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678"
        )

        cls.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678"
        )








