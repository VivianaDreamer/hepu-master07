# Generated by Django 4.0.4 on 2022-05-03 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0010_results_image_alter_design_op_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='image',
        ),
        migrations.AddField(
            model_name='results',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='results/', verbose_name='Production Year 1 '),
        ),
        migrations.AddField(
            model_name='results',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='results/', verbose_name='H2 Production 20 years'),
        ),
        migrations.AddField(
            model_name='results',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='results/', verbose_name='Pie LCOH'),
        ),
    ]
