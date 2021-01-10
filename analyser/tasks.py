from scraper.service import RedditAuth, ScrapperService
from scraper.models import Subreddit, Submission, AuthorRedditor, Comments
from django_q.tasks import async_task

def create_daily_schedule_once(): 
    Schedule.objects.create(func='scraper.tasks.daily_tasks', schedule_type=Schedule.DAILY)

def daily_tasks():
    # 27 tane task olusturuyor
    subreddits = [
        'all',
        'COVID',
        'COVID19',
        'Coronavirus',
        'CoronavirusUS',
        'CoronavirusUK',
        'CoronavirusCA',
        'CovIdiots',
        'USTravelBan'
    ]
    callTypes = [
        'hot',
        'new',
        'top'
    ]
    for subredditId in subreddits:
        for callType in callTypes:
            async_task('scraper.tasks.crawl_subreddit', subredditId, callType)

def crawl_subreddit(subredditId, callType = 'hot', limit = 300):
    print(20*'=' + subredditId + " " + callType + 20*'=')
    reddit = RedditAuth.public_auth()
    subredditRes = reddit.subreddit(subredditId)

    if callType == 'hot':
        hotSubmissions = subredditRes.hot(limit=limit)
        ScrapperService.save_all(hotSubmissions, False)
    elif callType == 'new':
        newSubmissions = subredditRes.new(limit=limit)
        ScrapperService.save_all(newSubmissions, False)
    elif callType == 'top':
        topSubmissions = subredditRes.top(limit=limit)
        ScrapperService.save_all(topSubmissions, False)

def find_submission_without_comment(task = None):
    for submission in Submission.objects.raw('SELECT s.id, s.name, s.submission_id, s.title, s.num_comments FROM scraper_submission as s LEFT JOIN scraper_comments as cmnts ON cmnts.submission_id = s.id WHERE cmnts.submission_id IS NULL AND s.num_comments > 10 AND s.num_comments < 1000 LIMIT 1'):
        async_task('scraper.tasks.crawl_submission', submission.submission_id, hook='scraper.tasks.find_submission_without_comment')

def crawl_submission(id): 
    reddit = RedditAuth.public_auth()
    submissionRes = reddit.submission(id=id)
    ScrapperService.save_single(submissionRes, True)

# def inform_everyone():
#     print("BU BIR TESTTIR")

# def hook_after_inform_everyone(task):
#     print(task.result)
