# Generated by Django 4.0.6 on 2022-07-23 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_reservation_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='qty',
            field=models.SmallIntegerField(default=1),
        ),
    ]
