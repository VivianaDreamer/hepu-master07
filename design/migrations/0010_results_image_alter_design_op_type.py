# Generated by Django 4.0.4 on 2022-05-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0009_remove_design_curtailed_energy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='results/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='design',
            name='op_type',
            field=models.CharField(choices=[('PPA', 'PPA'), ('On-site', 'User-defined generation vector')], default='PPA', max_length=30, verbose_name='Energy input'),
        ),
    ]
