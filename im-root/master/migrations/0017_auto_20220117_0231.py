# Generated by Django 3.2.7 on 2022-01-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0016_alter_m_salesman_custom_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='m_salesman',
            options={'verbose_name': 'Salesman', 'verbose_name_plural': 'Salesmen'},
        ),
        migrations.AlterField(
            model_name='m_salesman',
            name='address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]