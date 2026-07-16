from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from Customers.models import (
    validate_iran_phone , CustomerLevel , Customers , Comments
)



class ValidationIranPhoneTests (TestCase):
    
    def test_valid_phone(self):
        validate_iran_phone("09123456789")


    def test_phone_not_starting_with_09 (self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("08123456789")
    

    def test_phone_with_country_code (self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("+989123456789")


    def test_phone_with_less_than_11_digit (self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("0912345678")
    

    def test_phone_with_more_than_11_digit (self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("091234567890")


    def test_phone_containing_letters_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("09123abc789")


    def test_phone_containing_spaces(self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("0912 345678")


    def test_phone_containing_special_characters(self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("0912-345678")


    def test_empty_phone(self):
        with self.assertRaises(ValidationError):
            validate_iran_phone("")


class CustomerLevelModelTests (TestCase):

    def test_create_cutomer_level (self):
        level = CustomerLevel.objects.create(
            name="Gold" ,
            discount_percent=20 ,
        )

        self.assertEqual(level.name , "Gold")
        self.assertEqual(level.discount_percent , 20)
    

    def test_str_return_name (self):
        level = CustomerLevel.objects.create(
            name="Silver" , 
            discount_percent=10 ,
        )

        self.assertEqual(str(level) , "Silver")



class CustomerModelTests (TestCase):

    def setUp(self):
        self.level = CustomerLevel.objects.create(
            name="Gold" ,
            discount_percent=20 ,
        )
    

    def test_create_customer(self):
        customer = Customers.objects.create(
            fullname="Farzad" ,
            phone="09123456789" ,
            address="shiraz" ,
            level = self.level ,
            code=1001 ,
        )


        self.assertEqual(customer.fullname  ,"Farzad")
        self.assertEqual(customer.phone  , "09123456789")
        self.assertEqual(customer.address  ,"shiraz")
        self.assertEqual(customer.level  ,self.level)
        self.assertEqual(customer.code  ,1001)


    def test_str_returns_fullname (self):
        customer = Customers.objects.create(
            fullname="Ali" ,
            phone="09111111111" ,
        )
    

    def test_phone_is_unique(self):
        Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
        )

        with self.assertRaises(IntegrityError):
            Customers.objects.create(
                fullname="Reza",
                phone="09123456789",
            )


    def test_code_is_unique(self):
        Customers.objects.create(
            fullname="Ali",
            phone="09100000001",
            code=500,
        )

        with self.assertRaises(IntegrityError):
            Customers.objects.create(
                fullname="Reza",
                phone="09100000002",
                code=500,
            )


    def test_valid_phone_passes_validation(self):
        customer = Customers(
            fullname="Ali",
            phone="09123456789",
        )

        customer.full_clean()

    def test_invalid_phone_fails_validation(self):
        customer = Customers(
            fullname="Ali",
            phone="12345678901",
        )

        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_fullname_can_be_null(self):
        customer = Customers.objects.create(
            phone="09100000003",
        )

        self.assertIsNone(customer.fullname)

    def test_address_can_be_null(self):
        customer = Customers.objects.create(
            phone="09100000004",
        )

        self.assertIsNone(customer.address)

    def test_level_can_be_null(self):
        customer = Customers.objects.create(
            phone="09100000005",
        )

        self.assertIsNone(customer.level)

    def test_code_can_be_null(self):
        customer = Customers.objects.create(
            phone="09100000006",
        )

        self.assertIsNone(customer.code)

    def test_customer_can_have_level(self):
        customer = Customers.objects.create(
            fullname="Ali",
            phone="09100000007",
            level=self.level,
        )

        self.assertEqual(customer.level.name, "Gold")

    def test_customer_level_reverse_relation(self):
        Customers.objects.create(
            fullname="Ali",
            phone="09100000008",
            level=self.level,
        )

        Customers.objects.create(
            fullname="Reza",
            phone="09100000009",
            level=self.level,
        )

        self.assertEqual(self.level.customers.count(), 2)


class CommentsModelTests(TestCase):

    def setUp(self):
        self.customer = Customers.objects.create(
            fullname="Ali",
            phone="09123456789",
        )

    def test_create_comment(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Very good",
        )

        self.assertEqual(comment.customer, self.customer)
        self.assertEqual(comment.text, "Very good")

    def test_default_status_is_pending(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Test comment",
        )

        self.assertEqual(comment.status, "pending")

    def test_can_create_approved_comment(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Approved",
            status="approved",
        )

        self.assertEqual(comment.status, "approved")

    def test_can_create_rejected_comment(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Rejected",
            status="rejected",
        )

        self.assertEqual(comment.status, "rejected")

    def test_created_at_is_set(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Hello",
        )

        self.assertIsNotNone(comment.created_at)

    def test_str_returns_expected_value(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Hello",
        )

        self.assertEqual(
            str(comment),
            "comment by 09123456789 : pending."
        )

    def test_customer_can_have_multiple_comments(self):
        Comments.objects.create(
            customer=self.customer,
            text="Comment 1",
        )

        Comments.objects.create(
            customer=self.customer,
            text="Comment 2",
        )

        self.assertEqual(self.customer.comments.count(), 2)

    def test_comment_belongs_to_customer(self):
        comment = Comments.objects.create(
            customer=self.customer,
            text="Hello",
        )

        self.assertEqual(comment.customer.phone, "09123456789")

    def test_deleting_customer_deletes_comments(self):
        Comments.objects.create(
            customer=self.customer,
            text="Comment",
        )

        self.customer.delete()

        self.assertEqual(Comments.objects.count(), 0)