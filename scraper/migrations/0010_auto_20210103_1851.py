# Generated by Django 3.1.4 on 2021-01-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0009_auto_20210103_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_type',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
