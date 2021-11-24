# Generated by Django 3.2.7 on 2021-11-24 20:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_delete_warehouse_transfer'),
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='transfer_product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.FloatField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.m_product')),
            ],
            options={
                'verbose_name': 'Transfer Product',
                'verbose_name_plural': 'Transfer Products',
            },
        ),
        migrations.CreateModel(
            name='warehouse_transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('product', models.ManyToManyField(related_name='warehouse_transfer', to='sale.transfer_product')),
                ('warehouse_dest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_transfer_dest', to='master.m_warehouse')),
                ('warehouse_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_transfer_source', to='master.m_warehouse')),
            ],
            options={
                'verbose_name': 'Warehouse Transfer',
                'verbose_name_plural': 'Warehouse Transfers',
            },
        ),
    ]