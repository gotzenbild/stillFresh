# Generated by Django 2.2.6 on 2019-10-27 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20191027_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='id_code',
            field=models.IntegerField(default=0),
        ),
    ]