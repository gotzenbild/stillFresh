# Generated by Django 2.1 on 2019-10-26 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='store',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Store'),
        ),
    ]