# Generated by Django 3.2.7 on 2021-11-26 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0004_auto_20211127_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse_transfer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='p_payment',
            field=models.ManyToManyField(related_name='purchase', to='sale.payments', verbose_name='Payment'),
        ),
    ]
