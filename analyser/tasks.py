from django_q.tasks import async_task
from scraper.models import Comments, Submission
from .service import AnalyserService
from django_q.models import Schedule

def create_schedule_once(): 
    Schedule.objects.create(func='analyser.tasks.analyse_submissions', schedule_type=Schedule.CRON, cron = '0 */6 * * *')
    Schedule.objects.create(func='analyser.tasks.analyse_comments', schedule_type=Schedule.MINUTES, minutes=10)
    print("Analyser tasks scheduled!")

def analyse_comments():
    for comment in Comments.objects.all().filter(is_analized=False)[:750]: 
        AnalyserService.analyse_comment(comment)


def analyse_submissions():
    for submission in Submission.objects.all().filter(is_analized=False)[:750]: 
        AnalyserService.analyse_submission(submission)
 