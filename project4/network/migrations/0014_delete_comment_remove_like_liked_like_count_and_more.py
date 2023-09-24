# Generated by Django 4.2.3 on 2023-08-16 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_alter_post_timestamp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.RemoveField(
            model_name='like',
            name='liked',
        ),
        migrations.AddField(
            model_name='like',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to='network.post'),
        ),
    ]