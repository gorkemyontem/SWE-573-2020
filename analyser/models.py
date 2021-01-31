from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class SentenceAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.CharField(max_length=50)
    submission_id = models.CharField(max_length=50)
    subreddit_id = models.CharField(max_length=50)
    author_id = models.CharField(max_length=50)
    polarity = models.FloatField(default=0.0)
    subjectivity = models.FloatField(default=0.0)
    classification = models.CharField(max_length=50)
    text = models.CharField(max_length=5000)
    text_type = models.CharField(max_length=50) ## submission title, selftext, comment body
    words = ArrayField(ArrayField(models.CharField(max_length=100, blank=True)), size=1 )
    noun_phrases = ArrayField(ArrayField(models.CharField(max_length=200, blank=True)), size=1 )
    order = models.IntegerField(default=0)
    reddit_created_utc =  models.DateTimeField(null=True, blank=True) # submission or comment created time
    is_analized = models.BooleanField(default=False)
    created_utc = models.DateTimeField(default=timezone.now) # analyse created time

    def __str__(self):
        return str(self.id)

class SubmissionAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    submission_id = models.CharField(max_length=50)
    subreddit_id = models.CharField(max_length=50)
    author_id = models.CharField(max_length=50)
    words = ArrayField(ArrayField(models.CharField(max_length=100, blank=True)), size=1)
    noun_phrases = ArrayField(ArrayField(models.CharField(max_length=200, blank=True)), size=1 )
    num_comments = models.IntegerField(default=0)
    avg_polarity = models.FloatField(default=0.0)
    avg_subjectivity = models.FloatField(default=0.0)
    avg_classification = models.CharField(max_length=50)
    polarity = models.FloatField(default=0.0)
    subjectivity = models.FloatField(default=0.0)
    classification = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    upvote_ratio = models.FloatField(default=0.0)
    downs = models.IntegerField(default=0) 
    ups = models.IntegerField(default=0)
    reddit_created_utc =  models.DateTimeField(null=True, blank=True)  # submission created time
    created_utc = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.submission_id

class CommentAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.CharField(max_length=50)
    submission_id = models.CharField(max_length=50)
    subreddit_id = models.CharField(max_length=50)
    author_id = models.CharField(max_length=50)
    words = ArrayField(ArrayField(models.CharField(max_length=100, blank=True)), size=1)
    noun_phrases = ArrayField(ArrayField(models.CharField(max_length=200, blank=True)), size=1 )
    is_submitter = models.BooleanField(default=False)
    avg_polarity = models.FloatField(default=0.0)
    avg_subjectivity = models.FloatField(default=0.0)
    avg_classification = models.CharField(max_length=50)
    polarity = models.FloatField(default=0.0)
    subjectivity = models.FloatField(default=0.0)
    classification = models.CharField(max_length=50)
    controversiality = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    reddit_created_utc =  models.DateTimeField(null=True, blank=True) # comment created time
    created_utc = models.DateTimeField(default=timezone.now) # analysis time

    def __str__(self):
        return self.comment_id
    
class TagMeAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    tagme_id = models.IntegerField(default=0)
    spot = models.CharField(max_length=500)
    start = models.IntegerField(default=0)
    link_probability = models.FloatField(default=0.0)
    rho = models.FloatField(default=0.0)
    end = models.IntegerField(default=0)
    title = models.CharField(max_length=500)
    created_utc = models.DateTimeField(default=timezone.now) # analysis time
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TagMeSentenceAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    tagmeanalysis = models.ForeignKey(TagMeAnalysis, on_delete=models.CASCADE)
    sentenceanalysis = models.ForeignKey(SentenceAnalysis, on_delete=models.CASCADE)
    created_utc = models.DateTimeField(default=timezone.now) # analysis time

    def __str__(self):
        return str(self.id)
