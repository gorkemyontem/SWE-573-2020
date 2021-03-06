from django.test import TestCase, Client, RequestFactory
from accounts.models import CustomUser
from analyser.models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis, TagMeAnalysis, TagMeSentenceAnalysis
from pages.views import AnalysisPageView
from analyser.tasks import one_time_schedules, polarity_analysis_submission_task, polarity_analysis_comment_task, tagme_analysis_sentences_task
from scraper.models import Subreddit, AuthorRedditor, Submission, Comments
from scraper.service import RedditAuth, ScraperService, RedditModelService
from django_q.tasks import async_task
from django_q.models import Schedule
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime
import pprint
import json

class TestAnalysisPageView(TestCase):

    def setUp(self): 
        self.client = Client()
        self.factory = RequestFactory()
        self.username = 'lennon@thebeatles.com'
        self.password = 'johnpassword'
        self.url = reverse('analysis', args=[1])
        user = get_user_model().objects.create_user(username=self.username,  email=self.username, password=self.password)
        self.user = user

    def testLogin(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertEqual(logged_in, True)
