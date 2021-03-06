from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save
from django.db.models import Max


@receiver(post_save, sender=m_product)
def createStockForWarehouse(sender, instance, created, **kwargs):
    if created:
        warehouseList = m_warehouse.objects.all()
        for whouse in warehouseList:
            stocks.objects.create(product=instance, warehouse=whouse)


@receiver(post_save, sender=m_warehouse)
def createStocksInWarehouse(sender, instance, created, **kwargs):
    if created:
        products = m_product.objects.all()
        for pd in products:
            stocks.objects.create(product=pd, warehouse=instance)


@receiver(post_save, sender=m_supplier)
def updateCustomId(sender, instance, created, **kwargs):
    def getNewSupplierId():
        autoInc = auto_increments.objects.aggregate(id=Max('supplier_id'))
        auto_increments.objects.create(supplier_id=autoInc['id'] + 1)
        return format(autoInc['id'] + 1, '05d')

    if created:
        instance.custom_id = getNewSupplierId()
        instance.save()


@receiver(post_save, sender=m_customer)
def updateCustomId(sender, instance, created, **kwargs):
    def getNewCustomerId():
        autoInc = auto_increments.objects.aggregate(id=Max('customer_id'))
        auto_increments.objects.create(customer_id=autoInc['id'] + 1)
        return format(autoInc['id'] + 1, '05d')

    if created:
        instance.custom_id = getNewCustomerId()
        instance.save()

@receiver(post_save, sender=stocks)
def updateBatchId(sender, instance, created, **kwargs):
    def getNewBatchId():
        autoInc = auto_increments.objects.aggregate(id=Max('batch_id'))
        auto_increments.objects.create(batch_id=autoInc['id'] + 1)
        return format(autoInc['id'] + 1, '05d')

    if created:
        instance.batch_id = getNewBatchId()
        instance.save()

@receiver(post_save, sender=m_salesman)
def updateCustomId(sender, instance, created, **kwargs):
    def getNewSalesmanId():
        autoInc = auto_increments.objects.aggregate(id=Max('salesman_id'))
        auto_increments.objects.create(salesman_id=autoInc['id'] + 1)
        return format(autoInc['id'] + 1, '05d')

    if created:
        instance.custom_id = getNewSalesmanId()
        instance.save()