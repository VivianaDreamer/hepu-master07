# Generated by Django 4.0.4 on 2022-05-04 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0013_alter_design_op_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='results',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='results',
            name='image3',
        ),
        migrations.AddField(
            model_name='results',
            name='lcoh_data',
            field=models.TextField(blank=True, null=True, verbose_name='LCOH_data'),
        ),
    ]
