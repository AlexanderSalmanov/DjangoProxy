# Generated by Django 3.2 on 2023-11-14 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites_management', '0002_remove_site_internal_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='num_transitions',
            field=models.IntegerField(default=0),
        ),
    ]
