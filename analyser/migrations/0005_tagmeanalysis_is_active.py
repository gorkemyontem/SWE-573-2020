# Generated by Django 3.1.5 on 2021-01-31 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyser', '0004_sentenceanalysis_is_analized'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagmeanalysis',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]