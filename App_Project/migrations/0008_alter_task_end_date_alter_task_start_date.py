# Generated by Django 4.2.2 on 2023-07-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Project', '0007_alter_employeetask_employee_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]