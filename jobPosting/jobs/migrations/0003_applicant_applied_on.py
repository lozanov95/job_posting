# Generated by Django 3.2.6 on 2021-08-11 18:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20210810_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='applied_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
