import praw
import json
from django.views.generic import TemplateView, View, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponseRedirect
import pprint
from .forms import DashboardSearchForm
from django.http import JsonResponse
from django_q.tasks import async_task
from django.core.cache import cache

from scraper.service import RedditAuth, ScrapperService
from scraper.models import Subreddit, Submission, AuthorRedditor, Comments
from analyser.models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis
from analyser.service import AnalyserService

class SchedulerPageView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # async_task('scraper.tasks.inform_everyone', hook="scraper.tasks.hook_after_inform_everyone")
        return JsonResponse("DONE", safe =False)


class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    
    def dispatch(self, request, *args, **kwargs):
        # for _ in range(500):
        #     for comment in Comments.objects.all().filter(is_analized=False)[:750]: 
        #         AnalyserService.analyse_comment(comment)

            # for submission in Submission.objects.all().filter(is_analized=False)[:250]: 
            #     AnalyserService.analyse_submission(submission)

        print("DONE")
        return super().dispatch(request, *args, **kwargs)

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

class AnalysisPageView(DetailView):
    template_name = 'pages/analysis.html'
    model = Subreddit
    subreddit_detail_cache_key = 'cache.subreddit-{0}-detail'
    subreddit_detail_cache_time = 10 # 3 saat
    # subreddit_detail_cache_time = 1*60*60*3 # 3 saat

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.subreddit_detail_cache_key = self.subreddit_detail_cache_key.format(self.kwargs.get('pk'))
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if cache.get(self.subreddit_detail_cache_key) is None: 

            submissions = Submission.objects.all().filter(subreddit=self.kwargs.get('pk')).count()
            comments = Comments.objects.all().filter(subreddit=self.kwargs.get('pk')).count()


            additional_context = { 
                "submissionCount" : submissions,
                "commentCount" : comments,
            }

            cache.set(self.subreddit_detail_cache_key, additional_context, self.subreddit_detail_cache_time)
        else: 
            additional_context = cache.get(self.subreddit_detail_cache_key)

        data['additional_context'] = additional_context
        return data



   
   
class DashboardPageView(TemplateView):
    template_name = 'pages/dashboard.html'
    top5submissions_cache_key = 'cache.top5submissions'
    top5submissions_cache_time = 1*60*60*3 # 3 saat

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if cache.get(self.top5submissions_cache_key) is None: 
            top5subredditsSubmissions =  Subreddit.objects.raw('SELECT s.id, s.display_name, (SELECT Count(id) FROM scraper_submission WHERE subreddit_id = s.id) as submissions_count, (SELECT Count(id) FROM scraper_comments WHERE subreddit_id = s.id) as comments_count  FROM scraper_subreddit s WHERE id in (SELECT sc.subreddit_id FROM scraper_submission sc GROUP BY sc.subreddit_id ORDER BY sc.count DESC LIMIT 5)')
            cache.set(self.top5submissions_cache_key, top5subredditsSubmissions, self.top5submissions_cache_time)
        else: 
            top5subredditsSubmissions = cache.get(self.top5submissions_cache_key)
        data['top5submissions'] = top5subredditsSubmissions
        return data

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DashboardSearchForm(request.POST)
            if form.is_valid():
                searchText = form.cleaned_data['searchText']
                print('searchText:' + searchText)
                async_task('scraper.tasks.create_schedule_once')
                async_task('analyser.tasks.create_schedule_once')
                
        return render(request, self.template_name)
 

class StatsPageView(TemplateView):
    template_name = 'pages/stats.html'
    db_counts_cache_key = 'cache.dbcounts'
    db_counts_cache_time = 1*60*60*3 # 3 saat

    def myround(self, x, base=5):
        return base * round(round(x)/base)
        
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if cache.get(self.db_counts_cache_key) is None: 
            subredditCounts =  Subreddit.objects.all().count()
            submissionCounts =  Submission.objects.all().count()
            authorRedditorCounts =  AuthorRedditor.objects.all().count()
            commentsCounts =  Comments.objects.all().count()
            sentenceAnalysisCounts =  SentenceAnalysis.objects.all().count()
            submissionAnalysisCounts =  SubmissionAnalysis.objects.all().count()
            commentAnalysisCounts =  CommentAnalysis.objects.all().count()
            submissionsRatio =  submissionAnalysisCounts / submissionCounts * 100
            commentsRatio =  commentAnalysisCounts / commentsCounts * 100
            
            top5subredditsComments =  Subreddit.objects.raw('SELECT s.id, s.display_name, s.subscribers, s.title, s.url, (SELECT Count(id) FROM scraper_submission WHERE subreddit_id = s.id) as submissions_count, (SELECT Count(id) FROM scraper_comments WHERE subreddit_id = s.id) as comments_count  FROM scraper_subreddit s WHERE id in (SELECT sc.subreddit_id FROM scraper_comments sc GROUP BY sc.subreddit_id ORDER BY sc.count DESC LIMIT 5)')
            top5subredditsSubmissions =  Subreddit.objects.raw('SELECT s.id, s.display_name, s.subscribers, s.title, s.url, (SELECT Count(id) FROM scraper_submission WHERE subreddit_id = s.id) as submissions_count, (SELECT Count(id) FROM scraper_comments WHERE subreddit_id = s.id) as comments_count  FROM scraper_subreddit s WHERE id in (SELECT sc.subreddit_id FROM scraper_submission sc GROUP BY sc.subreddit_id ORDER BY sc.count DESC LIMIT 5)')
            counts = { 
                "subreddit" : subredditCounts,
                "submission" : submissionCounts,
                "authorRedditor" : authorRedditorCounts,
                "comments" : commentsCounts,
                "sentenceAnalysis" : sentenceAnalysisCounts,
                "submissionAnalysis" : submissionAnalysisCounts,
                "commentAnalysis" : commentAnalysisCounts,
                "submissionsRatio" : self.myround(submissionsRatio),
                "commentsRatio" : self.myround(commentsRatio),
                "top5subredditsComments" : top5subredditsComments,
                "top5subredditsSubmissions" : top5subredditsSubmissions,
            }
            cache.set(self.db_counts_cache_key, counts, self.db_counts_cache_time)
        else: 
            counts = cache.get(self.db_counts_cache_key)

        data['db_counts'] = counts
        return data

      # @staticmethod
    # def post(request):
    #     print(request)
    #     return super().dispatch()
    #
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     print(len(form))
    #     form.send_email()
    #     return super().form_valid(form)
    #
