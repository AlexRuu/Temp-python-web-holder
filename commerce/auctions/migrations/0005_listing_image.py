# Generated by Django 4.2.3 on 2023-07-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_bids_bid_rename_comments_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]