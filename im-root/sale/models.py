from django.db import models
import uuid
from master.models import m_customer, m_product, m_warehouse, m_supplier, m_bank
import datetime


# Create your models here.

class payments(models.Model):
    TRANSACTION_CHOICES = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit')
    )
    PAYMENT_CHOICES = (
        ('CASH', 'Cash'),
        ('BANK', 'Bank')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(m_customer, null=True, blank=True, on_delete=models.SET_NULL, related_name='payments')
    supplier = models.ForeignKey(m_supplier, null=True, blank=True, on_delete=models.SET_NULL, related_name='payments')
    debit_or_credit = models.CharField(max_length=20, choices=TRANSACTION_CHOICES, default='DEBIT')
    amount = models.FloatField(default=0, null=False, blank=False)
    date = models.DateTimeField(default=datetime.datetime.now(), null=False, blank=False)
    payment_type = models.CharField(max_length=20, default='CASH', choices=PAYMENT_CHOICES, null=False, blank='False')
    bank = models.ForeignKey(m_bank, null=True, blank=True, on_delete=models.SET_NULL)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        name = ''
        if self.customer:
            name = self.customer.name
        elif self.supplier:
            name = self.supplier.name

        return name + ' - ' + str(self.invoice_no) + ' - ' + str(self.amount)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'


class sale(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(m_customer, null=True, blank=True, on_delete=models.SET_NULL, related_name='sale')
    name = models.CharField(max_length=50, null=False, blank=False)
    contact = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    warehouse = models.ForeignKey(m_warehouse, null=False, blank=False, default='Main Warehouse',
                                  on_delete=models.CASCADE, related_name='sale')
    invoice_no = models.CharField(max_length=200, unique=True, blank=False, null=False)
    payment_received_gt = models.FloatField(null=False, blank=False, default=0)
    payment_due_gt = models.FloatField(null=False, blank=False, default=0)
    date = models.DateTimeField(default=datetime.datetime.now(), null=False, blank=False)
    productAndQuantity = models.ManyToManyField('productAndQuantity', related_name='sale')
    payment = models.ManyToManyField('payments', related_name='sale')

    def __str__(self):
        return self.invoice_no

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'


class productAndQuantity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    product = models.ForeignKey(m_product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1, null=False, blank=False)
    price = models.FloatField(default=0, null=False, blank=False)
    discount_in_percent = models.IntegerField(default=0, null=False, blank=False, verbose_name='Discount %')
    invoice_no = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return str(self.product) + '-' + str(self.quantity) + '-' + str(self.discount_in_percent) + '-' + str(
            self.invoice_no)

    class Meta:
        verbose_name = 'Product in Quantity'
        verbose_name_plural = 'Product And Quantity'

class purchase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    supplier = models.ForeignKey(m_supplier, null=True, blank=True, on_delete=models.SET_NULL, related_name='purchase')
    name = models.CharField(max_length=50, null=False, blank=False)
    contact = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    warehouse = models.ForeignKey(m_warehouse, null=False, blank=False, default='Main Warehouse',
                                  on_delete=models.CASCADE, related_name='purchase')
    invoice_no = models.CharField(max_length=200, unique=True, blank=False, null=False)
    payment_paid_gt = models.FloatField(null=False, blank=False, default=0)
    payment_due_gt = models.FloatField(null=False, blank=False, default=0)
    date = models.DateTimeField(default=datetime.datetime.now(), null=False, blank=False)
    productAndQuantity = models.ManyToManyField('productAndQuantity', related_name='purchase')

    def __str__(self):
        return self.invoice_no

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'