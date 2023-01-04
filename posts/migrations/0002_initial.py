# Generated by Django 4.1.4 on 2023-01-04 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.person'),
        ),
        migrations.AddField(
            model_name='homeworkdetail',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.homework'),
        ),
        migrations.AddField(
            model_name='homework',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.category'),
        ),
    ]
