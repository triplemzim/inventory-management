from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save

@receiver(post_save, sender=m_product)
def createStocks(sender, instance, created, **kwargs):
    if created:
        warehouseList = m_warehouse.objects.all()
        for whouse in warehouseList:
            stocks.objects.create(product=instance, warehouse=whouse)

@receiver(post_save, sender=m_warehouse)
def createStocks(sender, instance, created, **kwargs):
    if created:
        products = m_product.objects.all()
        for pd in products:
            stocks.objects.create(product=pd, warehouse=instance)
