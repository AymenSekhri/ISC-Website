# Generated by Django 2.2.8 on 2020-02-20 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0020_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdb',
            name='privLevel',
            field=models.SmallIntegerField(default=4),
        ),
    ]
