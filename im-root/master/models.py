from django.db import models
import uuid


# Create your models here.

class m_product_name(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product Name'
        verbose_name_plural = 'Product Names'


class m_category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    product_name = models.ForeignKey(m_product_name, on_delete=models.CASCADE, related_name='m_product_name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class m_product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product_name = models.ForeignKey(m_product_name, null=False, blank=False, on_delete=models.CASCADE,
                                     related_name='m_product')
    category = models.ForeignKey(m_category, null=True, blank=True, on_delete=models.CASCADE)
    default_purchase_price = models.FloatField(default=0, null=False, blank=False)
    default_sales_price = models.FloatField(default=0, null=False, blank=False)
    minimum_quantity = models.FloatField(default=0, null=False, blank=False)
    barcode = models.BigIntegerField(null=False, blank=False, primary_key=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        categoryName = ''
        if self.category:
            categoryName = ' - ' + self.category.name
        return self.product_name.name + categoryName

    class Meta:
        verbose_name = 'Product Details'
        verbose_name_plural = 'All Product Details'


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


class warehouse_transfer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ManyToManyField(m_product)
    warehouse_source = models.ForeignKey(m_warehouse, on_delete=models.CASCADE,
                                         related_name='warehouse_transfer_source')
    warehouse_dest = models.ForeignKey(m_warehouse, on_delete=models.CASCADE, related_name='warehouse_transfer_dest')
    quantity = models.FloatField(null=False, blank=False, default=0)
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.warehouse_source + ' to ' + self.warehouse_dest

    class Meta:
        verbose_name = 'Warehouse Transfer'
        verbose_name_plural = 'Warehouse Transfers'


class stocks(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(m_product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(m_warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.product.product_name.name + ' in ' + self.warehouse.name

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        unique_together = (('product', 'warehouse'),)


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


