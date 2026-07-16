from django.test import TestCase , override_settings
from CMS.utils import create_test_image , create_test_rgba_image
import os
import shutil
from PIL import Image
import tempfile
from CMS.models import GalleryImage  , Notification
from django.contrib.auth import get_user_model





User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class GalleryImageModelTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_str_returns_title(self):
        obj = GalleryImage.objects.create(
            title="Nature",
            image=create_test_image()
        )

        self.assertEqual(str(obj), "Nature")

    def test_str_returns_default_when_title_is_empty(self):
        obj = GalleryImage.objects.create(
            image=create_test_image()
        )

        self.assertEqual(str(obj), f"عکس شماره {obj.id}")

    def test_save_converts_image_to_webp(self):
        obj = GalleryImage.objects.create(
            title="Test",
            image=create_test_image("photo.jpg")
        )

        self.assertTrue(obj.image.name.endswith(".webp"))
        self.assertEqual(Image.open(obj.image.path).format, "WEBP")

    def test_delete_removes_image_file(self):
        obj = GalleryImage.objects.create(
            image=create_test_image()
        )

        image_path = obj.image.path

        self.assertTrue(os.path.exists(image_path))

        obj.delete()

        self.assertFalse(os.path.exists(image_path))


class NotificationModelTests(TestCase):

    def test_str_returns_title(self):
        notification = Notification.objects.create(
            title="Test",
            message="Hello"
        )

        self.assertEqual(str(notification), "Test")

    def test_default_ordering(self):
        old = Notification.objects.create(
            title="Old",
            message="1"
        )

        new = Notification.objects.create(
            title="New",
            message="2"
        )

        notifications = Notification.objects.all()

        self.assertEqual(notifications[0], new)
        self.assertEqual(notifications[1], old)
