# Generated by Django 4.2.3 on 2023-08-10 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_alter_post_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
