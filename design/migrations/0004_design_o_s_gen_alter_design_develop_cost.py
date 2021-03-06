# Generated by Django 4.0.3 on 2022-04-21 19:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0003_design_debt_design_debt_term_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='o_s_gen',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Input File'),
        ),
        migrations.AlterField(
            model_name='design',
            name='develop_cost',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Value must be on range between 1 and 100'), django.core.validators.MaxValueValidator(limit_value=100, message='Value must be on range between 1 and 100')], verbose_name='Specific Development cost [USD/kW]'),
        ),
    ]
