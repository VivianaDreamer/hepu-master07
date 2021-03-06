# Generated by Django 4.0.4 on 2022-05-26 17:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0022_results_lcoh_down_data_results_npc_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='land_cost',
            field=models.FloatField(default=6000, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be gratter than 0')], verbose_name='Land cost [USD/ha/year]'),
        ),
    ]
