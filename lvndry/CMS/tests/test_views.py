from django.test import override_settings
from .test_base import BaseAPITestCase
from CMS.utils import create_test_image , create_test_rgba_image
import tempfile
from CMS.models import GalleryImage , MagazineArticle , Notification
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase





User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp()



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class GalleryImageListCreateTests(BaseAPITestCase):

    def setUp(self):
        self.url = "/CMS/gallery/"


    def test_admin_can_get_gallery_images(self):
        GalleryImage.objects.create(
            title="Image 1",
            image=create_test_image()
        )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Image 1")

    def test_admin_can_create_gallery_image(self):
        self.client.force_authenticate(self.admin)

        data = {
            "title": "Nature",
            "image": create_test_image()
        }

        response = self.client.post(self.url, data, format="multipart")
        obj = GalleryImage.objects.get()

        self.assertEqual(obj.title, "Nature")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GalleryImage.objects.count(), 1)

    def test_invalid_create_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {"title": "Image"},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_cannot_create_gallery_image(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.url,
            {
                "title": "Nature",
                "image": create_test_image()
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class GalleryImageDetailTests(BaseAPITestCase):

    def setUp(self):
        uploaded = create_test_rgba_image()
        self.gallery = GalleryImage.objects.create(
            title="Old Title",
            image=uploaded
        )

        self.url = f"/CMS/gallery/{self.gallery.id}/"

    def test_admin_can_get_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Old Title")

    def test_get_non_existing_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get("/CMS/gallery/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_get_gallery_image(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_patch_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {"title": "New Title"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.gallery.refresh_from_db()

        self.assertEqual(self.gallery.title, "New Title")

    def test_patch_non_existing_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            "/CMS/gallery/9999/",
            {"title": "New"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_delete_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            GalleryImage.objects.filter(pk=self.gallery.pk).exists()
        )

    def test_delete_non_existing_gallery_image(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete("/CMS/gallery/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class AdminMagazineTests(BaseAPITestCase):

    def setUp(self):
        self.article = MagazineArticle.objects.create(
            title="Article 1",
            summary="summary",
            content="content",
            image=create_test_image(),
            is_active=True
        )

        self.url = "/CMS/admin_magazines/"


    def test_admin_can_get_all_articles(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_filter_active_articles(self):
        MagazineArticle.objects.create(
            title="Inactive",
            summary="summary",
            content="content",
            image=create_test_image(),
            is_active=False
        )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url, {"inactive": "false"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for article in response.data:
            self.assertTrue(article["is_active"])

    def test_admin_can_filter_inactive_articles(self):
        self.article.is_active = False
        self.article.save()

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url, {"inactive": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for article in response.data:
            self.assertFalse(article["is_active"])

    def test_normal_user_cannot_get_articles(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------- POST ----------------

    def test_admin_can_create_article(self):
        self.client.force_authenticate(self.admin)

        data = {
            "title": "New Article",
            "summary": "summary",
            "content": "content",
            "image": create_test_image(),
            "is_active": True
        }

        response = self.client.post(
            self.url,
            data,
            format="multipart"
        )
        article = MagazineArticle.objects.latest("id")

        self.assertEqual(article.title, "New Article")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MagazineArticle.objects.count(), 2)

    def test_normal_user_cannot_create_article(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.url,
            {},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_update_article(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "id": self.article.id,
                "title": "Updated"
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, "Updated")

    def test_patch_without_id(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {"title": "Updated"},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_article_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "id": 9999,
                "title": "Updated"
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_patch_article(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.url,
            {
                "id": self.article.id,
                "title": "Updated"
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_soft_delete_article(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            self.url,
            {
                "id": self.article.id
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()

        self.assertFalse(self.article.is_active)

    def test_delete_without_id(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            self.url,
            {},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_article_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(
            self.url,
            {
                "id": 9999
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_delete_article(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            self.url,
            {
                "id": self.article.id
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MagazineTests(APITestCase):

    def setUp(self):
        uploaded = create_test_rgba_image()

        MagazineArticle.objects.create(
            title="Active",
            summary="summary",
            content="content",
            image=uploaded,
            is_active=True
        )

        uploaded = create_test_rgba_image()

        MagazineArticle.objects.create(
            title="Inactive",
            summary="summary",
            content="content",
            image=uploaded,
            is_active=False
        )

        self.url = "/CMS/magazines/"

    def test_only_active_articles_are_returned(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Active")
        self.assertTrue(response.data[0]["is_active"])


class NotificationListCreateTests(BaseAPITestCase):

    def setUp(self):
        self.url = "/CMS/notifications/"


    def test_admin_can_get_notifications(self):
        Notification.objects.create(
            title="Test",
            message="Hello"
        )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_normal_user_cannot_get_notifications(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- POST ----------

    def test_admin_can_create_notification(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {
                "title": "Server",
                "message": "Maintenance",
                "is_active": True
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)

    def test_create_notification_invalid_data(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_cannot_create_notification(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.url,
            {
                "title": "Test",
                "message": "Hello"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NotificationDetailTests(BaseAPITestCase):

    def setUp(self):
        self.notification = Notification.objects.create(
            title="Title",
            message="Message",
            is_active=True
        )

        self.url = f"/CMS/notifications/{self.notification.id}/"


    def test_admin_can_get_notification(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.notification.title)

    def test_get_notification_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get("/CMS/notifications/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_get_notification(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_update_notification(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "title": "Updated"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.notification.refresh_from_db()

        self.assertEqual(self.notification.title, "Updated")

    def test_patch_notification_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            "/CMS/notifications/9999/",
            {"title": "Updated"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_update_notification(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.url,
            {
                "title": "Updated"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_notification(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Notification.objects.filter(pk=self.notification.pk).exists()
        )

    def test_delete_notification_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete("/CMS/notifications/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_delete_notification(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ShowLastNotifTests(APITestCase):

    def setUp(self):
        self.url = "/CMS/showlastnotif/"

    def test_return_latest_active_notification(self):
        Notification.objects.create(
            title="Old",
            message="Old",
            is_active=True
        )

        latest = Notification.objects.create(
            title="Latest",
            message="Latest",
            is_active=True
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], latest.id)
        self.assertEqual(response.data["title"], latest.title)

    def test_return_404_when_no_active_notification_exists(self):
        Notification.objects.create(
            title="Inactive",
            message="Inactive",
            is_active=False
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)