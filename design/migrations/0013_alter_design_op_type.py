# Generated by Django 4.0.4 on 2022-05-03 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0012_alter_results_image1_alter_results_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='op_type',
            field=models.CharField(choices=[('PPA', 'PPA')], default='PPA', max_length=30, verbose_name='Energy input'),
        ),
    ]
