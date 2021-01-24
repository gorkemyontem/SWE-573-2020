from django.test import TestCase
from accounts.models import CustomUser
from analyser.models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis, TagMeAnalysis, TagMeSentenceAnalysis
from analyser.tasks import one_time_schedules, polarity_analysis_submission_task, polarity_analysis_comment_task, tagme_analysis_sentences_task
from scraper.models import Subreddit, AuthorRedditor, Submission, Comments
from scraper.service import RedditAuth, ScraperService, RedditModelService
from django_q.tasks import async_task
from django_q.models import Schedule
from django.utils import timezone
import datetime
import pprint

class TestTask(TestCase):

    def test_one_time_schedules(self): 
        one_time_schedules()
        schedule1 = Schedule.objects.get(func='scraper.tasks.crawl_subreddits')
        schedule2 = Schedule.objects.get(func='analyser.tasks.polarity_analysis_submission_task')
        schedule3 = Schedule.objects.get(func='analyser.tasks.polarity_analysis_comment_task')
        self.assertEqual(str(schedule1), "scraper.tasks.crawl_subreddits")
        self.assertEqual(str(schedule2), "analyser.tasks.polarity_analysis_submission_task")
        self.assertEqual(str(schedule3), "analyser.tasks.polarity_analysis_comment_task")

    def test_polarity_analysis_submission_task(self): 
        polarity_analysis_submission_task(1, 1)

    def test_polarity_analysis_comment_task(self): 
        polarity_analysis_comment_task(1, 1)

    def test_tagme_analysis_sentences_task(self): 
        tagme_analysis_sentences_task(1, 1)

