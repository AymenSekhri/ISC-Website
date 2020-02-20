# Generated by Django 2.2.8 on 2020-02-20 20:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0021_auto_20200220_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bio', models.TextField()),
                ('contacts', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UsersApp.UsersDB')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('type', models.SmallIntegerField()),
                ('posting_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('tags', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UsersApp.UsersDB')),
            ],
        ),
    ]
