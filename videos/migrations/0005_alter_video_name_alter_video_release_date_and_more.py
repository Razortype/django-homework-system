# Generated by Django 4.1.4 on 2023-01-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_remove_video_youtube_url_video_video_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='release_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(max_length=100),
        ),
    ]
