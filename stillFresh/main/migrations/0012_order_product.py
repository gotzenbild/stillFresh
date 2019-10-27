# Generated by Django 2.1 on 2019-10-26 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20191026_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=100)),
                ('qty', models.FloatField()),
                ('order', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Order')),
            ],
        ),
    ]
