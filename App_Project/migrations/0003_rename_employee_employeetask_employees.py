# Generated by Django 4.2.1 on 2023-05-15 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Project', '0002_employeetask'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeetask',
            old_name='employee',
            new_name='employees',
        ),
    ]