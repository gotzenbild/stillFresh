# Generated by Django 2.2.6 on 2019-10-27 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_user_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User_Token',
        ),
    ]
