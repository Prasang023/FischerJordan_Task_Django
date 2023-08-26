from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import F

def validateMonth(value):
    if not (1 <= value <= 12):
        raise ValidationError(
            "Expiry month of credit/debit/prepaid cards must be in the range 1 <= month <= 12"
        )
    return value

# Validator for checking the length of EBT card numbers
def MinLengthValidator(value):
    if len(value) < 16:
        raise ValidationError(
            "EBT card numbers must be at least 16 digits long"
        )
    return value

class CreditCard(models.Model):
    number = models.CharField(
        max_length=17, default="4111111111111111"
    )
    last_4 = models.CharField(max_length=4)
    
    # Constants for card brands that ACME supports
    TYPE_AMEX = "amex"
    TYPE_DISCOVER = "discover"
    TYPE_MASTERCARD = "mastercard"
    TYPE_VISA = "visa"
    CARD_BRAND_CHOICE = (
        (TYPE_AMEX, "Amex"),
        (TYPE_DISCOVER, "Discover"),
        (TYPE_MASTERCARD, "Mastercard"),
        (TYPE_VISA, "Visa"),
    )

    brand = models.CharField(max_length=255, choices=CARD_BRAND_CHOICE)
    exp_month = models.PositiveSmallIntegerField(validators=[validateMonth])
    exp_year = models.PositiveSmallIntegerField() # 2 digits, e.g. 26 instead of 2026

class EBTCard(models.Model):
    number = models.CharField(
        max_length=19,  # Set the maximum length to 19
        default="4111111111111112",
        validators=[
            MinLengthValidator,  # Set the minimum length to 16
        ]
    )
    last_4 = models.CharField(max_length=4)
    
    # Constants for card brands that ACME supports
    TYPE_AMEX = "amex"
    TYPE_DISCOVER = "discover"
    TYPE_MASTERCARD = "mastercard"
    TYPE_VISA = "visa"
    CARD_BRAND_CHOICE = (
        (TYPE_AMEX, "Amex"),
        (TYPE_DISCOVER, "Discover"),
        (TYPE_MASTERCARD, "Mastercard"),
        (TYPE_VISA, "Visa"),
    )

    brand = models.CharField(max_length=255, choices=CARD_BRAND_CHOICE)

class Order(models.Model):

    # Define a Check Constraint to ensure that the ebt_total is less than or equal to the order_total
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(ebt_total__lte=F('order_total')),
                name='ebt_totsl_check',
            ),
        ]

    # The total amount which needs to be paid by the customer, including taxes and fees
    order_total = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(0)],
    )

    # Constants for order statuses
    TYPE_DRAFT = "draft"
    TYPE_FAILED = "failed"
    TYPE_SUCCEEDED = "succeeded"
    ORDER_STATUS_CHOICE = (
        (TYPE_DRAFT, "draft"),
        (TYPE_FAILED, "failed"),
        (TYPE_SUCCEEDED, "succeeded"),
    )

    status = models.CharField(
        max_length=10, 
        choices=ORDER_STATUS_CHOICE, 
        default=TYPE_DRAFT
    )

    success_date = models.DateTimeField(
        "Date when an order was successfully charged",
        null=True,
        blank=True,
    )

    # UNCOMMENT THIS FIELD TO GET STARTED!
    #
    # The amount which can be paid for with EBT. It's not necessarily true that the
    # entire ebt_total will be satisfied with EBT tender.
    ebt_total = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)], default=0
    )

class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, db_index=True
    )

    # What the customer actually chose to pay on the payment_method
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(0)],
    )

    description = models.CharField(max_length=255)

    # Constants for payment options
    TYPE_CREDIT_CARD = "credit_card"
    TYPE_EBT_CARD = "ebt_card"
    PAYMENT_CHOICES = (
        (TYPE_CREDIT_CARD, "credit_card"),
        (TYPE_EBT_CARD, "ebt_card"),
    )

    # Select the type of payment option: credit_card or ebt_card
    payment_option = models.CharField(
        max_length=25, choices=PAYMENT_CHOICES, default=TYPE_CREDIT_CARD
    )
    
    payment_method_types= models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(default=1)
    payment_method = GenericForeignKey('payment_method_types', 'target_id')

    # Constants for payment statuses
    TYPE_REQ_CONF = "requires_confirmation"
    TYPE_SUCCEEDED = "succeeded"
    TYPE_FAILED = "failed"
    PAYMENT_STATUS_CHOICE = (
        (TYPE_REQ_CONF, "requires_confirmation"),
        (TYPE_SUCCEEDED, "succeeded"),
        (TYPE_FAILED, "failed"),
    )

    status = models.CharField(
        max_length=24, 
        choices=PAYMENT_STATUS_CHOICE, 
        default=TYPE_REQ_CONF,
    )

    success_date = models.DateTimeField(
        "Date when a payment was successfully charged",
        null=True,
        blank=True,
    )

    last_processing_error = models.TextField(null=True, blank=True)