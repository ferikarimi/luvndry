from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Customers.models import Customers , Comments , CustomerLevel
from Customers.views import CommentPagination




User = get_user_model()

class CustomerRegisterViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("CustomerRegister")

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678",
        )

        self.valid_data = {
            "fullname": "Ali",
            "phone": "09123456789",
            "address": "Tehran",
        }

    def test_admin_can_register_customer(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customers.objects.count(), 1)

    def test_registered_customer_has_generated_code(self):
        self.client.force_authenticate(self.admin)

        self.client.post(self.url, self.valid_data)

        customer = Customers.objects.first()

        self.assertEqual(customer.code, 100)


    def test_invalid_data_returns_bad_request(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            self.url,
            {
                "fullname": "Ali",
                "phone": "123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_phone_returns_bad_request(self):
        Customers.objects.create(
            fullname="Reza",
            phone="09123456789",
            code=100,
        )

        self.client.force_authenticate(self.admin)

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_cannot_register_customer(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_register_customer(self):
        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class CustomerUpdateProfileViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("customerUpdateProfile")

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678",
        )

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            address="Tehran",
            code=100,
        )

        self.customer2 = Customers.objects.create(
            fullname="Reza",
            phone="09111111111",
            address="Mashhad",
            code=101,
        )

    # ---------------- GET ----------------

    def test_admin_can_get_customer_profile(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"code": self.customer.code},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_without_code_returns_bad_request(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_with_invalid_code_returns_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"code": 9999},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_get_customer_profile(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(
            self.url,
            {"code": self.customer.code},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_get_customer_profile(self):
        response = self.client.get(
            self.url,
            {"code": self.customer.code},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------- PATCH ----------------

    def test_admin_can_update_customer_profile(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "code": self.customer.code,
                "fullname": "New Ali",
                "address": "Tabriz",
            },
            format="json",
        )

        self.customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.customer.fullname, "New Ali")
        self.assertEqual(self.customer.address, "Tabriz")


    def test_patch_without_code_returns_bad_request(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "fullname": "Ali",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_with_invalid_code_returns_not_found(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "code": 9999,
                "fullname": "Ali",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_with_duplicate_phone_returns_bad_request(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "code": self.customer.code,
                "phone": self.customer2.phone,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_with_invalid_phone_returns_bad_request(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "code": self.customer.code,
                "phone": "123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_cannot_update_customer(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.url,
            {
                "code": self.customer.code,
                "fullname": "New Name",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_update_customer(self):
        response = self.client.patch(
            self.url,
            {
                "code": self.customer.code,
                "fullname": "New Name",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_keeps_other_fields_unchanged(self):
        self.client.force_authenticate(self.admin)

        self.client.patch(
            self.url,
            {
                "code": self.customer.code,
                "fullname": "Only Name Changed",
            },
            format="json",
        )

        self.customer.refresh_from_db()

        self.assertEqual(self.customer.fullname, "Only Name Changed")
        self.assertEqual(self.customer.phone, "09123456789")
        self.assertEqual(self.customer.address, "Tehran")



class CustomerDeleteViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678",
        )

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

        self.url = reverse(
            "CustomerDelete",
            kwargs={"code": self.customer.code},
        )

    def test_admin_can_delete_customer(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Customers.objects.filter(code=self.customer.code).exists()
        )

    def test_delete_non_existing_customer_returns_not_found(self):
        self.client.force_authenticate(self.admin)

        url = reverse(
            "CustomerDelete",
            kwargs={"code": 9999},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_delete_customer(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_delete_customer(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class CustomerCommentsCreateViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("CustomerCommentsCreate")

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

    def test_customer_can_create_comment(self):
        response = self.client.post(
            self.url,
            {
                "phone": "09123456789",
                "text": "Excellent service",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comments.objects.count(), 1)


    def test_unknown_customer_cannot_create_comment(self):
        response = self.client.post(
            self.url,
            {
                "phone": "09111111111",
                "text": "Excellent service",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comments.objects.count(), 0)

    def test_invalid_phone_returns_bad_request(self):
        response = self.client.post(
            self.url,
            {
                "phone": "123",
                "text": "Excellent service",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_text_is_required(self):
        response = self.client.post(
            self.url,
            {
                "phone": "09123456789",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_is_required(self):
        response = self.client.post(
            self.url,
            {
                "text": "Excellent service",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_response_message(self):
        response = self.client.post(
            self.url,
            {
                "phone": "09123456789",
                "text": "Excellent service",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["MESSAGE"],
            "Your comment has been submitted and will be displayed after approval.",
        )



class AdminCommentStatusViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678",
        )

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

        self.comment = Comments.objects.create(
            customer=self.customer,
            text="Good Service",
        )

        self.url = reverse(
            "AdminCommentStatus",
            kwargs={"pk": self.comment.id},
        )

    def test_admin_can_approve_comment(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "status": "approved",
            },
            format="json",
        )

        self.comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.status, "approved")

    def test_admin_can_reject_comment(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "status": "rejected",
            },
            format="json",
        )

        self.comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.status, "rejected")

    def test_invalid_status_returns_bad_request(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {
                "status": "invalid-status",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_not_found_returns_not_found(self):
        self.client.force_authenticate(self.admin)

        url = reverse(
            "AdminCommentStatus",
            kwargs={"pk": 9999},
        )

        response = self.client.patch(
            url,
            {
                "status": "approved",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_cannot_change_comment_status(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            self.url,
            {
                "status": "approved",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_change_comment_status(self):
        response = self.client.patch(
            self.url,
            {
                "status": "approved",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class CommentRecentlyViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("CommentRecently")

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

    def test_returns_only_approved_comments(self):
        Comments.objects.create(
            customer=self.customer,
            text="Approved",
            status="approved",
        )

        Comments.objects.create(
            customer=self.customer,
            text="Pending",
            status="pending",
        )

        Comments.objects.create(
            customer=self.customer,
            text="Rejected",
            status="rejected",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["text"], "Approved")

    def test_returns_maximum_fifteen_comments(self):
        for i in range(20):
            Comments.objects.create(
                customer=self.customer,
                text=f"Comment {i}",
                status="approved",
            )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 15)

    def test_returns_empty_list_when_no_comment_exists(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_serializer_contains_expected_fields(self):
        Comments.objects.create(
            customer=self.customer,
            text="Approved",
            status="approved",
        )

        response = self.client.get(self.url)

        self.assertIn("customer", response.data[0])
        self.assertIn("text", response.data[0])
        self.assertIn("created_at", response.data[0])
        self.assertIn("created_at_jalili", response.data[0])
        self.assertIn("hidden_phone", response.data[0])


    def test_comments_are_ordered_by_created_at_descending(self):
        first = Comments.objects.create(
            customer=self.customer,
            text="First",
            status="approved",
        )

        second = Comments.objects.create(
            customer=self.customer,
            text="Second",
            status="approved",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.data[0]["text"], second.text)
        self.assertEqual(response.data[1]["text"], first.text)


class AllCustomersViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("allcustomers")

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678",
        )

        self.gold = CustomerLevel.objects.create(
            name="طلایی",
            discount_percent=20,
        )

        self.silver = CustomerLevel.objects.create(
            name="نقره‌ای",
            discount_percent=10,
        )

        self.customer1 = Customers.objects.create(
            fullname="Ali Ahmadi",
            phone="09123456789",
            code=100,
            level=self.gold,
        )

        self.customer2 = Customers.objects.create(
            fullname="Reza Mohammadi",
            phone="09111111111",
            code=101,
            level=self.silver,
        )

        self.customer3 = Customers.objects.create(
            fullname="Mohammad",
            phone="09351234567",
            code=102,
        )

    def test_admin_can_get_customers(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_cannot_get_customers(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_get_customers(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_search_by_fullname(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"search": "Ali"},
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["fullname"],
            "Ali Ahmadi",
        )

    def test_search_by_phone(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"search": "091111"},
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["phone"],
            "09111111111",
        )

    def test_search_by_code(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"search": "102"},
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["code"],
            102,
        )

    def test_search_returns_empty_result(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"search": "Unknown"},
        )

        self.assertEqual(response.data["count"], 0)

    def test_filter_gold_level(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"level": "gold"},
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["fullname"],
            "Ali Ahmadi",
        )

    def test_filter_silver_level(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {"level": "silver"},
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["fullname"],
            "Reza Mohammadi",
        )

    def test_search_and_level_filter_together(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(
            self.url,
            {
                "search": "Ali",
                "level": "gold",
            },
        )

        self.assertEqual(response.data["count"], 1)

    def test_pagination_returns_twelve_items_per_page(self):
        for i in range(20):
            Customers.objects.create(
                fullname=f"Customer {i}",
                phone=f"0919000{i:04d}",
                code=1000 + i,
            )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(len(response.data["results"]), 12)


class CommentPaginationTests(APITestCase):

    def test_default_page_size(self):
        paginator = CommentPagination()

        self.assertEqual(paginator.page_size, 30)

    def test_page_size_query_param(self):
        paginator = CommentPagination()

        self.assertEqual(
            paginator.page_size_query_param,
            "page_size",
        )

    def test_max_page_size(self):
        paginator = CommentPagination()

        self.assertEqual(paginator.max_page_size, 60)


class AdminCommentListViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("AdminCommentList")

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="12345678",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="12345678",
        )

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

    def test_admin_can_get_comment_list(self):
        Comments.objects.create(
            customer=self.customer,
            text="Comment",
        )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_cannot_get_comment_list(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_get_comment_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_returns_all_comments(self):
        for i in range(5):
            Comments.objects.create(
                customer=self.customer,
                text=f"Comment {i}",
            )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.data["count"], 5)

    def test_comments_are_ordered_by_created_at_desc(self):
        first = Comments.objects.create(
            customer=self.customer,
            text="First",
        )

        second = Comments.objects.create(
            customer=self.customer,
            text="Second",
        )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.data["results"][0]["id"], second.id)
        self.assertEqual(response.data["results"][1]["id"], first.id)


    def test_pagination_returns_thirty_items(self):
        for i in range(35):
            Comments.objects.create(
                customer=self.customer,
                text=f"Comment {i}",
            )

        self.client.force_authenticate(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(len(response.data["results"]), 30)


class CustomerLevelViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("customerlevel")

        self.bronze = CustomerLevel.objects.create(
            name="برنزی",
            discount_percent=5,
        )

        self.silver = CustomerLevel.objects.create(
            name="نقره‌ای",
            discount_percent=10,
        )

        self.gold = CustomerLevel.objects.create(
            name="طلایی",
            discount_percent=20,
        )

    def test_returns_customer_level_statistics(self):
        Customers.objects.create(
            fullname="A",
            phone="09111111111",
            code=100,
            level=self.bronze,
        )

        Customers.objects.create(
            fullname="B",
            phone="09111111112",
            code=101,
            level=self.silver,
        )

        Customers.objects.create(
            fullname="C",
            phone="09111111113",
            code=102,
            level=self.gold,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["bronze"], 465)
        self.assertEqual(response.data["silver"], 228)
        self.assertEqual(response.data["gold"], 74)

    def test_returns_default_statistics_when_no_customer_exists(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["bronze"], 464)
        self.assertEqual(response.data["silver"], 227)
        self.assertEqual(response.data["gold"], 73)


    def test_multiple_customers_are_counted_correctly(self):
        for i in range(3):
            Customers.objects.create(
                fullname=f"B{i}",
                phone=f"0912000000{i}",
                code=100 + i,
                level=self.bronze,
            )

        for i in range(2):
            Customers.objects.create(
                fullname=f"S{i}",
                phone=f"0913000000{i}",
                code=200 + i,
                level=self.silver,
            )

        Customers.objects.create(
            fullname="G",
            phone="09140000000",
            code=300,
            level=self.gold,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.data["bronze"], 467)
        self.assertEqual(response.data["silver"], 229)
        self.assertEqual(response.data["gold"], 74)