# Generated by Django 2.2.8 on 2019-12-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0007_auto_20191222_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdb',
            name='password',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
    ]
