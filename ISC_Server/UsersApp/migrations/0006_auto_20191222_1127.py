# Generated by Django 2.2.8 on 2019-12-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0005_auto_20191221_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdb',
            name='password',
            field=models.BinaryField(),
        ),
    ]
