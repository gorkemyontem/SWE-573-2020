from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json
from django.core.cache import cache
from analyser.models import CommentAnalysis
from scraper.models import Subreddit
from textblob import TextBlob, Word
from collections import Counter
import os
import environ
import requests
import time
import concurrent.futures
from analyser.service import AnalyserService
from scraper.service import ScraperService
from scraper.models import Subreddit, Submission, AuthorRedditor, Comments
from analyser.models import SentenceAnalysis, CommentAnalysis, TagMeAnalysis
from analyser.tasks import one_time_schedules, polarity_analysis_submission_task, polarity_analysis_comment_task, tagme_analysis_sentences_task
from .queries import Queries



env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(__file__)) + '\.env'
environ.Env.read_env(ENV_DIR)
    
class StatsScheduleAjax(View):
    template_name = None 

    def multiprocess_comment_scraping(self): 
        for _ in range(40):
            bulk = []
            bulk.extend(Submission.objects.raw('SELECT s.id, s.name, s.submission_id, s.title, s.num_comments FROM scraper_submission as s LEFT JOIN scraper_comments as cmnts ON cmnts.submission_id = s.id WHERE cmnts.submission_id IS NULL AND s.num_comments > 10 AND s.num_comments < 2000 ORDER BY RANDOM() LIMIT 25'))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(ScraperService.scrape_single_submission, bulk)


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            action = self.kwargs.get('action')
            if action is None:
                return JsonResponse({"success":False}, status=400)
            else:
                print(action)
                result = {
                    'daily': one_time_schedules,
                    'comment-scraping' : self.multiprocess_comment_scraping,
                    'submission-analysis' : polarity_analysis_submission_task,
                    'comment-analysis' : polarity_analysis_comment_task,
                    'tagme-analysis' : tagme_analysis_sentences_task,
                }[action]()
            return JsonResponse({"success":True }, status=200)

class DataWords(View):
    template_name = None
    cache_key = 'cache.data-words-analysis-{0}-detail'
    cache_time = 1*60*60*3 # 3 saat

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            subredditId = self.kwargs.get('pk')
            self.cache_key = self.cache_key.format(subredditId)
            subreddit = Subreddit.objects.get(pk=subredditId)
            data = {}
            if subreddit is None:
                return JsonResponse({"success": False}, status=400)
            # TODO https variable, link probability variable, data variable, 
            if cache.get(self.cache_key) is None: 
                bar30 = Queries.bar30(subreddit.subreddit_id)
                data['bar30labels'] = bar30[0]
                data['bar30counts'] = bar30[1]
                cache.set(self.cache_key, data, self.cache_time)
            else: 
                data = cache.get(self.cache_key)

        return JsonResponse({"success":True, "data": data}, status=200)


class DataBubble(View):
    template_name = None
    cache_key = 'cache.data-bubble-analysis-{0}-detail'
    cache_time = 1*60*60*3 

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            subredditId = self.kwargs.get('pk')
            self.cache_key = self.cache_key.format(subredditId)
            subreddit = Subreddit.objects.get(pk=subredditId)
            data = {}
            if subreddit is None:
                return JsonResponse({"success": False}, status=400)
            
            if cache.get(self.cache_key) is None: 

                buble100 = Queries.buble100(subreddit.subreddit_id)
                data['bubble500labels'] = buble100[0]
                data['bubble500counts'] = buble100[1]
                data['bubble500polarity'] = buble100[2]
                cache.set(self.cache_key, data, self.cache_time)
            else: 
                data = cache.get(self.cache_key)

        return JsonResponse({"success":True, "data": data}, status=200)


class DataSubmissions(View):
    template_name = None
    cache_key = 'cache.data-submission-analysis-{0}-detail'
    cache_time = 1*60*60*3 

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            subredditId = self.kwargs.get('pk')
            self.cache_key = self.cache_key.format(subredditId)
            subreddit = Subreddit.objects.get(pk=subredditId)
            data = {}
            if subreddit is None:
                return JsonResponse({"success": False}, status=400)
            
            if cache.get(self.cache_key) is None: 
                submissions = Submission.objects.filter(subreddit_id = subreddit.id, is_analized = True, created_utc__range=["2020-12-01", "2021-01-08"]).order_by('-score').values('id', 'submission_id', 'name', 'title', 'url', 'selftext', 'num_comments', 'score', 'created_utc', 'redditor_id')[:100]
                data['top100submissions'] =  json.dumps(list(submissions), cls=DjangoJSONEncoder)
                cache.set(self.cache_key, data, self.cache_time)
            else: 
                data = cache.get(self.cache_key)

        return JsonResponse({"success":True, "data": data}, status=200)


class DataComments(View):
    template_name = None
    cache_key = 'cache.data-comments-analysis-{0}-{1}'
    cache_time = 1*60*60*3 

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            subredditId = self.kwargs.get('pk')
            submissionId = self.kwargs.get('submission_id')
            self.cache_key = self.cache_key.format(subredditId, submissionId)
            subreddit = Subreddit.objects.get(pk=subredditId)
            submission = Submission.objects.get(pk=submissionId)
            data = {}
            if subreddit is None or submission is None:
                return JsonResponse({"success": False}, status=400)
            
            if cache.get(self.cache_key) is None: 

                goodComments = Comments.objects.filter(submission_id = submission.id, is_analized = True, created_utc__range=["2020-12-01", "2021-01-08"]).order_by('-score')[:10]
                badComments = Comments.objects.filter(submission_id = submission.id, is_analized = True, created_utc__range=["2020-12-01", "2021-01-08"]).order_by('score')[:10]
                data['goodComments'] = list(goodComments)
                data['badComments'] = list(badComments)
                cache.set(self.cache_key, data, self.cache_time)
            else: 
                data = cache.get(self.cache_key)

        return JsonResponse({"success":True, "data": data}, status=200)
    # def flattenNouns(self, nounsData):
    #     nouns = []
    #     for nounsArr in nounsData:
    #         nouns.extend(nounsArr)
    #     return nouns

    # def getSetsOfWordsAndNouns(self, wordsAndNouns):
    #     words = []
    #     nouns = []
    #     for wordsArr, nounsArr in wordsAndNouns:
    #         words.extend(wordsArr)
    #         nouns.extend(nounsArr)
    #     wordsSet = set(words) 
    #     nounsSet = set(nouns) 
    #     return (wordsSet, nounsSet)
