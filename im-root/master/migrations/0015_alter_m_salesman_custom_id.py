# Generated by Django 3.2.7 on 2022-01-13 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0014_m_salesman'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_salesman',
            name='custom_id',
            field=models.CharField(default='000000006', max_length=15),
        ),
    ]
