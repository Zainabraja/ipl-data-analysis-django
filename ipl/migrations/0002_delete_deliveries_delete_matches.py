# Generated by Django 4.1 on 2022-08-28 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='deliveries',
        ),
        migrations.DeleteModel(
            name='matches',
        ),
    ]