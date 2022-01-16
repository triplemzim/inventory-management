from django.db import models
import uuid
from django.utils import timezone
from django.db.models import Max


# Create your models here.

class m_brand(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Brand Name'
        verbose_name_plural = 'Brand Names'


class m_category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class m_product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    brand = models.ForeignKey(m_brand, null=False, blank=False, on_delete=models.CASCADE,
                              related_name='m_product')
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(m_category, null=True, blank=True, on_delete=models.CASCADE)
    default_purchase_price = models.FloatField(default=0, null=False, blank=False)
    default_sales_price = models.FloatField(default=0, null=False, blank=False)
    minimum_quantity = models.FloatField(default=0, null=False, blank=False, verbose_name='Critical Product Quantity')
    barcode = models.BigIntegerField(null=False, blank=False, primary_key=True)
    photo = models.ImageField(null=True, blank=True)
    date_created = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        categoryName = ''
        brandName = ''

        if self.category:
            categoryName = ' - ' + self.category.name
        if self.brand:
            brandName = self.brand.name + ' - '
        return brandName + self.name + categoryName

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product List'


class m_warehouse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=200)
    custom_id = models.CharField(max_length=200, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name + ' - ' + self.custom_id

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'


class m_customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    contact = models.CharField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(null=True, blank=True)
    custom_id = models.CharField(max_length=10, null=False, blank=False, default='GENERATING...')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class m_supplier(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    contact = models.CharField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(null=True, blank=True)
    custom_id = models.CharField(max_length=10, null=False, blank=False, default='GENERATING...')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class m_bank(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    branch = models.CharField(max_length=200, null=True, blank=True)
    account_number = models.CharField(max_length=200, null=False, blank=False)
    initial_balance = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name + self.branch

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'


class auto_increments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    batch_id = models.PositiveIntegerField(null=False, blank=False, default=1)
    customer_id = models.PositiveIntegerField(null=False, blank=False, default=1)
    supplier_id = models.PositiveIntegerField(null=False, blank=False, default=1)
    salesman_id = models.PositiveIntegerField(null=True, blank=True, default=1)


class stocks(models.Model):
    # def getNewBatchId():
    #     autoInc = auto_increments.objects.aggregate(batchId=Max('batch_id'))
    #     auto_increments.objects.create(batch_id=autoInc['batchId'] + 1)
    #     return format(autoInc['batchId'] + 1, '09d')

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(m_product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(m_warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.FloatField(default=0, null=False, blank=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    batch_id = models.CharField(max_length=15, default='GENERATING...', blank=False, null=False)
    date_created = models.DateTimeField(default=timezone.now, null=False, blank=False)

    def __str__(self):
        return self.product.name + ' in ' + self.warehouse.name

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        unique_together = (('product', 'warehouse', 'batch_id'),)
        ordering = ['batch_id', '-quantity', 'date_created']


class bank_transactions(models.Model):
    TRANSACTION_CHOICES = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    bank = models.ForeignKey(m_bank, on_delete=models.CASCADE, related_name='bank_transactions')
    debit_or_credit = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, default='DEBIT')
    amount = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.bank.name + ' - ' + self.debit_or_credit + ' - ' + str(self.amount)

    class Meta:
        verbose_name = 'Bank Transaction'
        verbose_name_plural = 'Bank Transactions'


class m_salesman(models.Model):
    STATUS_CHOICE = (
        ("ACTIVE", "ACTIVE"),
        ("INACTIVE", "INACTIVE")
    )

    def getNewSalesmanId():
        autoInc = auto_increments.objects.aggregate(salesmanId=Max('salesman_id'))
        auto_increments.objects.create(salesman_id=autoInc['salesmanId'] + 1)
        return format(autoInc['salesmanId'] + 1, '09d')

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    custom_id = models.CharField(max_length=15, default='GENERATING...', blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    contact_no = models.CharField(max_length=15, blank=False, null=False)
    address = models.CharField(max_length=30, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now, null=False, blank=False)
    date_joined = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="ACTIVE")

    class Meta:
        verbose_name = 'Salesman'
        verbose_name_plural = 'Salesmen'
# class messages(models.Model):
#     id = models.AutoField(primary_key=True)
#     message = models.CharField(max_length=300, null=False, blank=False)
#     priority = models.PositiveIntegerField(default=1,null=False,blank=False)
