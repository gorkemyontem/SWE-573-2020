from .service import RedditAuth, ScrapperService
from .models import Subreddit, Submission, AuthorRedditor, Comments
from django_q.tasks import async_task
from django_q.models import Schedule

def create_schedule_once(): 
    # Schedule.objects.create(func='scraper.tasks.daily_tasks', schedule_type=Schedule.DAILY)
    # Schedule.objects.create(func='scraper.tasks.find_submission_without_comment', schedule_type=Schedule.ONCE)
    print("New Scraper tasks scheduled!")

def daily_tasks():
    # Creates 27 tasks at once
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
            async_task('scraper.tasks.crawl_subreddit', subredditId, callType, group='daily')

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
    print("BEGIN find_submission_without_comment")
    for submission in Submission.objects.raw('SELECT s.id, s.name, s.submission_id, s.title, s.num_comments FROM scraper_submission as s LEFT JOIN scraper_comments as cmnts ON cmnts.submission_id = s.id WHERE cmnts.submission_id IS NULL AND s.num_comments > 10 AND s.num_comments < 2000 ORDER BY RANDOM() LIMIT 1000'):
        reddit = RedditAuth.public_auth()
        submissionRes = reddit.submission(id=submission.submission_id)
        ScrapperService.save_single(submissionRes, True)
    print("END find_submission_without_comment")




# def find_submission_without_comment():
#     for submission in Submission.objects.raw(' SELECT s.id, s.name, s.submission_id, s.title, s.num_comments FROM scraper_submission as s LEFT JOIN scraper_comments as cmnts ON cmnts.submission_id = s.id WHERE cmnts.submission_id IS NULL AND s.num_comments > 10 AND s.num_comments < 2000 ORDER BY RANDOM() LIMIT 1'):
#         reddit = RedditAuth.public_auth()
#         submissionRes = reddit.submission(id=submission.submission_id)
#         ScrapperService.save_single(submissionRes, True)
