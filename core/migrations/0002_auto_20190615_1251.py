# Generated by Django 2.2.2 on 2019-06-15 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('initiative', '0002_auto_20190615_1251'),
        ('user', '0002_auto_20190615_1251'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
