# Generated by Django 3.1.5 on 2021-01-13 00:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analyser', '0002_auto_20210113_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagMeAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tagme_id', models.IntegerField(default=0)),
                ('spot', models.CharField(max_length=500)),
                ('start', models.IntegerField(default=0)),
                ('link_probability', models.FloatField(default=0.0)),
                ('rho', models.FloatField(default=0.0)),
                ('end', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=500)),
                ('created_utc', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TagMeSentenceAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_utc', models.DateTimeField(default=django.utils.timezone.now)),
                ('sentenceanalysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyser.sentenceanalysis')),
                ('tagmeanalysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyser.tagmeanalysis')),
            ],
        ),
    ]
