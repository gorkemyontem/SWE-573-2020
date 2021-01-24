from django_q.tasks import async_task
from scraper.models import Comments, Submission
from .service import AnalyserService
from django_q.models import Schedule
from django.core.cache import cache
import concurrent.futures
from analyser.models import SentenceAnalysis, TagMeAnalysis
from scraper.models import Submission, Comments
from .thread import DjangoConnectionThreadPoolExecutor
import time
import re

def one_time_schedules(): 
    Schedule.objects.create(func='scraper.tasks.crawl_subreddits', schedule_type=Schedule.DAILY)
    # Schedule.objects.create(func='scraper.tasks.find_submission_without_comment', schedule_type=Schedule.DAILY)
    Schedule.objects.create(func='analyser.tasks.polarity_analysis_submission_task', schedule_type=Schedule.CRON, cron = '0 */6 * * *')
    Schedule.objects.create(func='analyser.tasks.polarity_analysis_comment_task', schedule_type=Schedule.MINUTES, minutes=10)

def polarity_analysis_submission_task(range_limit = 100, loop_limit = 50):
    for _ in range(range_limit):
        bulk = []
        bulk.extend(Submission.objects.all().filter(is_analized=False)[:loop_limit])

        t1 = time.perf_counter()
        with DjangoConnectionThreadPoolExecutor() as executor:
            executor.map(AnalyserService.polarity_analysis_submission, bulk)
        
        t2 = time.perf_counter()
        print(f'Submission {_} - Finished in {round(t2-t1)} seconds')   


def polarity_analysis_comment_task(range_limit = 3000, loop_limit = 50):
    for _ in range(range_limit):
        bulk = []
        bulk.extend(Comments.objects.all().filter(is_analized=False)[:loop_limit])

        t1 = time.perf_counter()
        with DjangoConnectionThreadPoolExecutor() as executor: 
            executor.map(AnalyserService.polarity_analysis_comment, bulk)

        t2 = time.perf_counter() 
        print(f'Comment {_} - Finished in {round(t2-t1)} seconds')


def tagme_analysis_sentences_task(range_limit = 100000, loop_limit = 25):
    # tags =    TagMeAnalysis.objects.all().values_list('id','spot','title')
    # tagCache = {}
    # tagCache['atoh'] = [item for item in tags if re.match('^[a-h,A-H]', item[1])] 
    # tagCache['itop'] = [item for item in tags if re.match('^[i-p,I-P]', item[1])]
    # tagCache['qtoz'] = [item for item in tags if re.match('^[q-z,Q-Z]', item[1])]
    # tagCache['rest'] = [item for item in tags if not re.match('^[a-zA-Z]', item[1])]
    # cache.set('tagCache', tagCache, 1*60*60*6)
    for _ in range(range_limit):
        bulk = []
        bulk.extend(SentenceAnalysis.objects.all().filter(is_analized= False)[:loop_limit])

        t1 = time.perf_counter()
        with DjangoConnectionThreadPoolExecutor() as executor:
            executor.map(AnalyserService.tagme_analysis_sentences, bulk)
        
        t2 = time.perf_counter()
        print(f'TagMe {_} - Finished in {round(t2-t1)} seconds')
