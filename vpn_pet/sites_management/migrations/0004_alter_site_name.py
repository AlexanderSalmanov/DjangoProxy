# Generated by Django 3.2 on 2023-11-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites_management', '0003_site_num_transitions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
