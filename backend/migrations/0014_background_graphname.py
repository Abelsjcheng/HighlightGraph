# Generated by Django 2.2.6 on 2019-12-05 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_background_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='background',
            name='graphname',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
