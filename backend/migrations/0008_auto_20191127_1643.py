# Generated by Django 2.2.6 on 2019-11-27 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20191127_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='content',
            field=models.CharField(max_length=255),
        ),
    ]
