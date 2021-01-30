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


def multiprocess_comment_scraping(range_limit = 40): 
    for _ in range(range_limit):
        bulk = []
        bulk.extend(Submission.objects.raw('SELECT s.id, s.name, s.submission_id, s.title, s.num_comments FROM scraper_submission as s LEFT JOIN scraper_comments as cmnts ON cmnts.submission_id = s.id WHERE cmnts.submission_id IS NULL AND s.num_comments > 10 AND s.num_comments < 2000 ORDER BY RANDOM() LIMIT 25'))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(ScraperService.scrape_single_submission, bulk)



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
    for _ in range(range_limit):
        bulk = []
        bulk.extend(SentenceAnalysis.objects.all().filter(is_analized= False)[:loop_limit])

        t1 = time.perf_counter()
        with DjangoConnectionThreadPoolExecutor() as executor:
            executor.map(AnalyserService.tagme_analysis_sentences, bulk)
        
        t2 = time.perf_counter()
        print(f'TagMe {_} - Finished in {round(t2-t1)} seconds')
