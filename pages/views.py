import praw
import json
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import DashboardSearchForm
from django.http import JsonResponse
from django_q.tasks import async_task

from scraper.service import RedditAuth, ScrapperService
from scraper.models import Subreddit, Submission, AuthorRedditor, Comments
from analyser.service import AnalyserService

class SchedulerPageView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # async_task('scraper.tasks.inform_everyone', hook="scraper.tasks.hook_after_inform_everyone")
        return JsonResponse("DONE", safe =False)


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class DashboardPageView(TemplateView):
    template_name = 'pages/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DashboardSearchForm(request.POST)
            if form.is_valid():
                searchText = form.cleaned_data['searchText']
                print('searchText:' + searchText)
                # async_task('scraper.tasks.create_schedule_once')
                # async_task('analyser.tasks.create_schedule_once')
                
        return render(request, self.template_name)
 
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
