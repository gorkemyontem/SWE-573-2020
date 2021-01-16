# Generated by Django 3.1.5 on 2021-01-10 15:52

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_id', models.CharField(max_length=50)),
                ('submission_id', models.CharField(max_length=50)),
                ('subreddit_id', models.CharField(max_length=50)),
                ('author_id', models.CharField(max_length=50)),
                ('words', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None), size=1)),
                ('noun_phrases', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None), size=1)),
                ('is_submitter', models.BooleanField(default=False)),
                ('avg_polarity', models.FloatField(default=0.0)),
                ('avg_subjectivity', models.FloatField(default=0.0)),
                ('avg_classification', models.CharField(max_length=50)),
                ('polarity', models.FloatField(default=0.0)),
                ('subjectivity', models.FloatField(default=0.0)),
                ('classification', models.CharField(max_length=50)),
                ('controversiality', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('ups', models.IntegerField(default=0)),
                ('downs', models.IntegerField(default=0)),
                ('depth', models.IntegerField(default=0)),
                ('created_utc', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SentenceAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_id', models.CharField(max_length=50)),
                ('submission_id', models.CharField(max_length=50)),
                ('subreddit_id', models.CharField(max_length=50)),
                ('author_id', models.CharField(max_length=50)),
                ('polarity', models.FloatField(default=0.0)),
                ('subjectivity', models.FloatField(default=0.0)),
                ('classification', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=5000)),
                ('text_type', models.CharField(max_length=50)),
                ('words', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None), size=1)),
                ('noun_phrases', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None), size=1)),
                ('order', models.IntegerField(default=0)),
                ('created_utc', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('submission_id', models.CharField(max_length=50)),
                ('subreddit_id', models.CharField(max_length=50)),
                ('author_id', models.CharField(max_length=50)),
                ('words', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None), size=1)),
                ('noun_phrases', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None), size=1)),
                ('num_comments', models.IntegerField(default=0)),
                ('avg_polarity', models.FloatField(default=0.0)),
                ('avg_subjectivity', models.FloatField(default=0.0)),
                ('avg_classification', models.CharField(max_length=50)),
                ('polarity', models.FloatField(default=0.0)),
                ('subjectivity', models.FloatField(default=0.0)),
                ('classification', models.CharField(max_length=50)),
                ('score', models.IntegerField(default=0)),
                ('upvote_ratio', models.FloatField(default=0.0)),
                ('downs', models.IntegerField(default=0)),
                ('ups', models.IntegerField(default=0)),
                ('created_utc', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]