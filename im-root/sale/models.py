from django.db import models
import uuid
from master.models import m_customer, m_product, m_warehouse, m_supplier, m_bank, m_salesman
import datetime
from django.utils import timezone
from users.models import CustomUser



# Create your models here.

class payments(models.Model):
    TRANSACTION_CHOICES = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit')
    )
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('bKash', 'bKash'),
        ('Bank', 'Bank')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(m_customer, null=True, blank=True, on_delete=models.SET_NULL, related_name='payments')
    supplier = models.ForeignKey(m_supplier, null=True, blank=True, on_delete=models.SET_NULL, related_name='payments')
    debit_or_credit = models.CharField(max_length=20, choices=TRANSACTION_CHOICES, default='DEBIT')
    amount = models.FloatField(default=0, null=False, blank=False)
    date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    payment_type = models.CharField(max_length=20, default='Cash', choices=PAYMENT_CHOICES, null=False, blank='False')
    bank = models.ForeignKey(m_bank, null=True, blank=True, on_delete=models.SET_NULL)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)

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
    date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    productAndQuantity = models.ManyToManyField('productAndQuantity', related_name='sale')
    payment = models.ManyToManyField('payments', related_name='sale')
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    salesman = models.ForeignKey(m_salesman, null=True, blank=True, on_delete=models.CASCADE, related_name='sale')

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
    expiry_date = models.DateTimeField(null=True, blank=True)
    salesman_discount = models.FloatField(default=0, null=True, blank=True, verbose_name='Salesman Discount')

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
    date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    productAndQuantity = models.ManyToManyField('productAndQuantity', related_name='purchase')
    p_payment = models.ManyToManyField('payments', related_name='purchase', verbose_name='Payment')
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.invoice_no

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'


class transfer_product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(m_product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=False, blank=False, default=0)

    def __str__(self):
        return str(self.product) + ' - ' + str(self.quantity)

    class Meta:
        verbose_name = 'Transfer Product'
        verbose_name_plural = 'Transfer Products'

class warehouse_transfer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product_list = models.ManyToManyField(transfer_product, related_name='warehouse_transfer')
    warehouse_source = models.ForeignKey(m_warehouse, on_delete=models.CASCADE,
                                         related_name='warehouse_transfer_source')
    warehouse_dest = models.ForeignKey(m_warehouse, on_delete=models.CASCADE, related_name='warehouse_transfer_dest')
    comment = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    # serial = models.IntegerField(default=getSerial(), null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.warehouse_source.name) + ' to ' + str(self.warehouse_dest.name)

    class Meta:
        verbose_name = 'Warehouse Transfer'
        verbose_name_plural = 'Warehouse Transfers'