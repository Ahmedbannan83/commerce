# Generated by Django 4.2.6 on 2023-10-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner_user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
