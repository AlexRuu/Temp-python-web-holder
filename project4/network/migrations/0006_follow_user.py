# Generated by Django 4.2.3 on 2023-08-06 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_follow_delete_follower_alter_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]