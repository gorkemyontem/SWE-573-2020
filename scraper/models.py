from django.db import models

class Subreddit(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    display_name = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    description_html = models.CharField(max_length=5000)
    subscribers = models.IntegerField(default=0)
    lang = models.CharField(max_length=50)
    over18 = models.BooleanField(default=False)
    subreddit_type = models.CharField(max_length=500)
    quarantine = models.BooleanField(default=False)
    restrict_commenting = models.BooleanField(default=False)
    restrict_posting = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    created_utc = models.DateTimeField()
    def __str__(self):
        return self.display_name

#region pprint subreddit
# {
#DONE=> 'created_utc': 1581434104.0,
#DONE=> 'description': 'COVID2019',
#DONE=> 'description_html': '<!-- SC_OFF --><div class="md"><p>COVID2019</p>\n''</div><!-- SC_ON -->',
#DONE=> 'display_name': 'COVID',
#DONE=> 'name': 't5_2f4kx6',
#DONE=> 'subscribers': 7677,
#DONE=> 'lang': 'en',
#DONE=> 'over18': False,
#DONE=> 'subreddit_type': 'public',
#DONE=> 'quarantine': False,
#DONE=> 'restrict_commenting': False,
#DONE=> 'restrict_posting': True,
#DONE=> 'title': 'Novel Coronavirus News, Analysis, Survival Stories, Etc.',
#DONE=> 'url': '/r/COVID/',
#endregion
 
class AuthorRedditor(models.Model):
    id = models.AutoField(primary_key=True)
    redditor_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    created_utc = models.DateTimeField()
    comment_karma = models.IntegerField(default=0)
    link_karma = models.IntegerField(default=0)
    total_karma = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name

#region autor pprint
# {
#DONE=>  'id': 'gnc18',
#DONE=>  'name': 'GD3123',
#DONE=> 'created_utc': 1400615905.0,
#DONE=> 'comment_karma': 343,
#DONE=> 'link_karma': 506,
#DONE=> 'total_karma': 849,
#DONE=> 'verified': True}
#endregion

class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    submission_id = models.CharField(max_length=50, unique=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    redditor = models.ForeignKey(AuthorRedditor, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500)
    selftext =  models.CharField(max_length=5000)
    link_flair_text = models.CharField(max_length=500, null=True)
    num_comments = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    upvote_ratio = models.FloatField(default=0.0)
    downs = models.IntegerField(default=0) 
    ups = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)
    over_18 = models.BooleanField(default=False)
    permalink =  models.CharField(max_length=500)
    category = models.CharField(max_length=500, null=True)
    comment_sort = models.CharField(max_length=500, null=True)
    content_categories = models.CharField(max_length=500, null=True)
    discussion_type = models.CharField(max_length=500, null=True)
    is_analized = models.BooleanField(default=False)
    created_utc = models.DateTimeField()

    def __str__(self):
        return self.title

#region pprint submisson
#  {
#DONE=> 'id': 'gmxq55',
#DONE=> 'name': 't3_gmxq55',
#DONE=> 'title': 'The United States has over 90,000 cases of CoViD-19. Of those, '
#DONE=> 'author': Redditor(name='blackwingbear'),
#DONE=> 'url': 'https://www.reddit.com/r/COVID/comments/gmxq55/the_united_states_has_over_90000_cases_of_covid19/',
#DONE=> 'selftext': '',
#DONE=> 'link_flair_text': None,
#DONE=> 'num_comments': 5,
#DONE=> 'score': 1,
#DONE=> 'upvote_ratio': 0.52,
#DONE=> 'created_utc': 1589923742.0,
#DONE=> 'downs': 0,
#DONE=> 'ups': 1,
#DONE=> 'subreddit': Subreddit(display_name='COVID'),
#DONE=> 'archived': True,
#DONE=> 'over_18': False,
#DONE=> 'permalink': '/r/COVID/comments/gmxq55/the_united_states_has_over_90000_cases_of_covid19/',
#DONE=> 'category': None,  dataanalyse:[photography, Null]
#DONE=> 'comment_sort': 'confidence',
#DONE=> 'content_categories': None,  dataanalyse:['photography', 'gaming', 'diy_and_crafts', 'entertainment', 'drawing_and_painting', 'comics', Null]
#DONE=> 'discussion_type': None,  dataanalyse:[CHAT, Null]

#endregion

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.CharField(max_length=50, unique=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    redditor = models.ForeignKey(AuthorRedditor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    permalink = models.CharField(max_length=500)
    link_id = models.CharField(max_length=50)
    parent_id = models.CharField(max_length=50)
    body = models.CharField(max_length=5000)
    body_html = models.CharField(max_length=5000)
    is_submitter = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    controversiality = models.IntegerField(default=0)
    archived =  models.BooleanField(default=False)
    comment_type = models.CharField(max_length=500, null=True),
    is_analized = models.BooleanField(default=False)
    created_utc = models.DateTimeField()
  
    def __str__(self):
        return self.name
 
#region pprint comments
#DONE=> 'id': 'fmwlc2w',
#DONE=> 'subreddit': Subreddit(display_name='COVID'),
#DONE=> 'author': Redditor(name='ProtiK'),
#DONE=> 'parent_id': 't1_fmwjdd5',
#DONE=> 'body': "That's correct. The exact process is very location-dependent but "
#DONE=> 'body_html': '<div class="md"><p>That&#39;s correct. The exact process is '
#DONE=> 'is_submitter': False,
#DONE=> 'created_utc': 1586448634.0,
#DONE=> 'score': 1,
#DONE=> 'name': 't1_fmwlc2w',
#DONE=> 'link_id': 't3_fwtkgz',
#DONE=> 'permalink': '/r/COVID/comments/fwtkgz/being_illegally_kicked_out_of_my_residence_during/fmwlc2w/',
#DONE=> 'ups': 1,
#DONE=> 'downs': 0,
#DONE=> 'depth': 5,
#DONE=> 'controversiality': 0,
#DONE=> 'archived': True,
#DONE=> 'comment_type': None,
#endregion
