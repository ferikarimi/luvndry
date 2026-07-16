from django.test import TestCase
from rest_framework.serializers import ValidationError
from Customers.models import CustomerLevel, Customers
from Customers.serializers import *


class DateJaliliMixinTests(TestCase):

    def setUp(self):
        self.mixin = DateJaliliMixin()

    def test_to_jalili_returns_none_when_date_is_none(self):
        self.assertIsNone(self.mixin.to_jalili(None))

    def test_to_jalili_returns_jalali_date(self):
        from datetime import datetime

        date = datetime(2025, 7, 10)

        result = self.mixin.to_jalili(date)

        self.assertIsInstance(result, str)
        self.assertIn("/", result)

    def test_to_jalili_translates_weekday_to_persian(self):
        from datetime import datetime

        date = datetime(2025, 7, 10)

        result = self.mixin.to_jalili(date)

        self.assertNotIn("Thursday", result)
        self.assertIn("پنج‌شنبه", result)


class CustomerRegisterSerializerTests(TestCase):

    def test_create_first_customer_sets_code_to_100(self):
        serializer = CustomerRegisterSerializer(
            data={
                "fullname": "Ali",
                "phone": "09123456789",
                "address": "Tehran",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertEqual(customer.code, 100)

    def test_create_customer_increments_code(self):
        Customers.objects.create(
            fullname="Reza",
            phone="09111111111",
            code=150,
        )

        serializer = CustomerRegisterSerializer(
            data={
                "fullname": "Ali",
                "phone": "09123456789",
                "address": "Tehran",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertEqual(customer.code, 151)

    def test_code_is_read_only(self):
        serializer = CustomerRegisterSerializer(
            data={
                "fullname": "Ali",
                "phone": "09123456789",
                "address": "Tehran",
                "code": 9999,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertNotEqual(customer.code, 9999)
        self.assertEqual(customer.code, 100)

    def test_serializer_creates_customer(self):
        serializer = CustomerRegisterSerializer(
            data={
                "fullname": "Ali",
                "phone": "09123456789",
                "address": "Tehran",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertEqual(Customers.objects.count(), 1)
        self.assertEqual(customer.fullname, "Ali")
        self.assertEqual(customer.phone, "09123456789")


class CustomerUpdateProfileSerializerTests(TestCase):

    def setUp(self):
        self.customer1 = Customers.objects.create(
            fullname="Ali",
            phone="09111111111",
            code=100,
        )

        self.customer2 = Customers.objects.create(
            fullname="Reza",
            phone="09122222222",
            code=101,
        )

    def test_update_customer_successfully(self):
        serializer = CustomerUpdateProfileSerializer(
            instance=self.customer1,
            data={
                "phone": "09133333333",
                "fullname": "New Ali",
                "address": "Mashhad",
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertEqual(customer.phone, "09133333333")
        self.assertEqual(customer.fullname, "New Ali")
        self.assertEqual(customer.address, "Mashhad")

    def test_validate_phone_rejects_duplicate_phone(self):
        serializer = CustomerUpdateProfileSerializer(
            instance=self.customer1,
            data={
                "phone": "09122222222",
            },
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_validate_phone_accepts_same_phone_for_same_customer(self):
        serializer = CustomerUpdateProfileSerializer(
            instance=self.customer1,
            data={
                "phone": "09111111111",
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_code_is_read_only(self):
        serializer = CustomerUpdateProfileSerializer(
            instance=self.customer1,
            data={
                "code": 999,
                "fullname": "Ali",
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertEqual(customer.code, 100)


class CustomerInfoSerializerTests(TestCase):

    def setUp(self):
        self.level = CustomerLevel.objects.create(
            name="Gold",
            discount_percent=20,
        )

        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            address="Tehran",
            code=100,
            level=self.level,
        )

    def test_serializer_returns_expected_fields(self):
        serializer = CustomerInfoSerializer(self.customer)

        self.assertEqual(serializer.data["code"], 100)
        self.assertEqual(serializer.data["phone"], "09123456789")
        self.assertEqual(serializer.data["fullname"], "Ali")
        self.assertEqual(serializer.data["address"], "Tehran")
        self.assertEqual(serializer.data["level"], self.level.id)

    def test_all_fields_are_read_only(self):
        serializer = CustomerInfoSerializer(
            instance=self.customer,
            data={
                "fullname": "New Name",
                "phone": "09100000000",
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        customer = serializer.save()

        self.assertEqual(customer.fullname, "Ali")
        self.assertEqual(customer.phone, "09123456789")


class CommentCreateSerializerTests(TestCase):

    def setUp(self):
        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

    def test_create_comment_successfully(self):
        serializer = CommentCreateSerializer(
            data={
                "phone": "09123456789",
                "text": "Excellent service",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()

        self.assertEqual(comment.customer, self.customer)
        self.assertEqual(comment.text, "Excellent service")
        self.assertEqual(Comments.objects.count(), 1)

    def test_create_comment_with_unknown_phone_raises_validation_error(self):
        serializer = CommentCreateSerializer(
            data={
                "phone": "09111111111",
                "text": "Excellent service",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        with self.assertRaises(serializers.ValidationError):
            serializer.save()

    def test_phone_is_write_only(self):
        serializer = CommentCreateSerializer(
            data={
                "phone": "09123456789",
                "text": "Excellent service",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()

        data = CommentCreateSerializer(comment).data

        self.assertNotIn("phone", data)

    def test_serializer_creates_comment_for_correct_customer(self):
        serializer = CommentCreateSerializer(
            data={
                "phone": "09123456789",
                "text": "Test",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()

        self.assertEqual(comment.customer.phone, "09123456789")


class CommentAdminSerializerTests(TestCase):

    def setUp(self):
        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

        self.comment = Comments.objects.create(
            customer=self.customer,
            text="Good",
        )

    def test_customer_is_string_representation(self):
        serializer = CommentAdminSerializer(self.comment)

        self.assertEqual(
            serializer.data["customer"],
            str(self.customer),
        )

    def test_customer_phone_returns_phone(self):
        serializer = CommentAdminSerializer(self.comment)

        self.assertEqual(
            serializer.data["customer_phone"],
            "09123456789",
        )

    def test_serializer_contains_all_fields(self):
        serializer = CommentAdminSerializer(self.comment)

        self.assertIn("id", serializer.data)
        self.assertIn("customer", serializer.data)
        self.assertIn("customer_phone", serializer.data)
        self.assertIn("text", serializer.data)
        self.assertIn("status", serializer.data)
        self.assertIn("created_at", serializer.data)


class CommentRecentlySerializerTests(TestCase):

    def setUp(self):
        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            code=100,
        )

        self.comment = Comments.objects.create(
            customer=self.customer,
            text="Very Good",
        )

    def test_hidden_phone_masks_phone_number(self):
        serializer = CommentRecentlySerializer(self.comment)

        self.assertEqual(
            serializer.data["hidden_phone"],
            "0912****789",
        )

    def test_created_at_jalili_is_generated(self):
        serializer = CommentRecentlySerializer(self.comment)

        self.assertIsNotNone(serializer.data["created_at_jalili"])
        self.assertIsInstance(serializer.data["created_at_jalili"], str)

    def test_serializer_contains_expected_fields(self):
        serializer = CommentRecentlySerializer(self.comment)

        self.assertIn("customer", serializer.data)
        self.assertIn("text", serializer.data)
        self.assertIn("created_at", serializer.data)
        self.assertIn("created_at_jalili", serializer.data)
        self.assertIn("hidden_phone", serializer.data)

    def test_hidden_phone_keeps_first_four_digits(self):
        serializer = CommentRecentlySerializer(self.comment)

        hidden_phone = serializer.data["hidden_phone"]

        self.assertTrue(hidden_phone.startswith("0912"))

    def test_hidden_phone_keeps_last_three_digits(self):
        serializer = CommentRecentlySerializer(self.comment)

        hidden_phone = serializer.data["hidden_phone"]

        self.assertTrue(hidden_phone.endswith("789"))


class AllCustomersSerializerTests(TestCase):

    def setUp(self):
        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
            address="Tehran",
            code=100,
        )

    def test_phone_is_returned_correctly(self):
        serializer = AllCustomersSerializer(self.customer)

        self.assertEqual(
            serializer.data["phone"],
            "09123456789",
        )

    def test_serializer_contains_expected_fields(self):
        serializer = AllCustomersSerializer(self.customer)

        self.assertEqual(
            set(serializer.data.keys()),
            {"id", "code", "phone", "fullname", "address"},
        )

    def test_serializer_returns_customer_information(self):
        serializer = AllCustomersSerializer(self.customer)

        self.assertEqual(serializer.data["fullname"], "Ali")
        self.assertEqual(serializer.data["address"], "Tehran")
        self.assertEqual(serializer.data["code"], 100)