# Generated by Django 2.2.8 on 2019-12-21 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0002_auto_20191221_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdb',
            name='privLevel',
            field=models.IntegerField(),
        ),
    ]
