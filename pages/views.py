import praw
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import DashboardSearchForm
from django.http import JsonResponse

from .service import RedditAuth


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
                print(searchText)
                reddit = RedditAuth.public_auth()
                print(reddit.read_only)  # Output: True
                for submission in reddit.subreddit("learnpython").hot(limit=10):
                    print(submission.title)
                #subreddit = reddit.subreddit(keyword)
                #new_sr = subreddit.new(limit=100)
                #for submission in new_sr:

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
