# Generated by Django 4.0.4 on 2022-05-24 21:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0020_design_eff_replacement_design_sp_footprint_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='water_consumption_data',
            field=models.TextField(blank=True, null=True, verbose_name='Water Consumption'),
        ),
        migrations.AlterField(
            model_name='design',
            name='debt',
            field=models.FloatField(default=60, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be greater than 0'), django.core.validators.MaxValueValidator(limit_value=100, message='Value must be lower than 100')], verbose_name='Debt [%]'),
        ),
        migrations.AlterField(
            model_name='design',
            name='equity_discount_rate',
            field=models.FloatField(default=12, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be greater than 0'), django.core.validators.MaxValueValidator(limit_value=100, message='Value must be lower than 100')], verbose_name='Equity discount rate [%]'),
        ),
        migrations.AlterField(
            model_name='design',
            name='first_category_tax',
            field=models.FloatField(default=25, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be greater than 0'), django.core.validators.MaxValueValidator(limit_value=100, message='Value must be lower than 100')], verbose_name='First category Tax [%]'),
        ),
        migrations.AlterField(
            model_name='design',
            name='interest_rate',
            field=models.FloatField(default=6, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be greater than 0'), django.core.validators.MaxValueValidator(limit_value=100, message='Value must be lower than 100')], verbose_name='Interest Rate [%]'),
        ),
        migrations.AlterField(
            model_name='design',
            name='land_cost',
            field=models.FloatField(default=60000, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be gratter than 0')], verbose_name='Land cost [USD/ha/year]'),
        ),
        migrations.AlterField(
            model_name='design',
            name='om',
            field=models.FloatField(default=50, validators=[django.core.validators.MinValueValidator(limit_value=0, message='Value must be gratter than 0')], verbose_name='O&M [USD/kW/year]'),
        ),
        migrations.AlterField(
            model_name='results',
            name='energy_consumption',
            field=models.FloatField(default=0.0, verbose_name='Energy consumption [GWh/year]'),
        ),
        migrations.AlterField(
            model_name='results',
            name='hydrogen_production',
            field=models.FloatField(default=0.0, verbose_name='Hydrogen production [tons/year]'),
        ),
        migrations.AlterField(
            model_name='results',
            name='load_factor',
            field=models.FloatField(default=0.0, verbose_name='Electrolyzer load factor [%]'),
        ),
        migrations.AlterField(
            model_name='results',
            name='oxigen_production',
            field=models.FloatField(default=0.0, verbose_name='Oxigen production [tons/year]'),
        ),
    ]
