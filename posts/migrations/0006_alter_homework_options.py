# Generated by Django 4.1.4 on 2023-02-27 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_homework_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homework',
            options={'ordering': ('expired_date',)},
        ),
    ]
