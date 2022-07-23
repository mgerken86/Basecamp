# Generated by Django 4.0.6 on 2022-07-23 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gear_item',
            name='name',
            field=models.CharField(default='gear', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gear_item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='gear_item',
            name='qty',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]