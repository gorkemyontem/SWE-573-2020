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

class SchedulerPageView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        async_task('scraper.tasks.inform_everyone', hook="scraper.tasks.hook_after_inform_everyone")

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
                async_task('scraper.tasks.find_submission_without_comment')
                    
                # ScrapperService.subreddit_search(searchText, 300)
        # return render(request, 'explore/index.html', { 'data': data })
        return render(request, self.template_name)

    def post2(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DashboardSearchForm(request.POST)
            if form.is_valid():
                searchText = form.cleaned_data['searchText']
                print(searchText)
                reddit = RedditAuth.public_auth()
                for submission in reddit.subreddit(searchText).hot(limit=1):
                    print("======================3333")
                    print(submission.author) #ADROBLES2024 #Provides an instance of Redditor.
                    print(submission.clicked) #False #Whether or not the submission has been clicked by the client.
                    print(submission.comments) #<praw.models.comment_forest.CommentForest object at 0x7f25136c4040> #Provides an instance of CommentForest.
                    print(submission.created_utc) #1589565284.0 #Time the submission was created, represented in Unix Time.
                    print(submission.distinguished) #moderator #Whether or not the submission is distinguished.
                    print(submission.edited) #False #Whether or not the submission has been edited.
                    print(submission.id) #gkdz0s #ID of the submission.
                    print(submission.is_original_content) #False #Whether or not the submission has been set as original content.
                    print(submission.is_self) #False # Whether or not the submission is a selfpost (text-only).
                    print(submission.link_flair_text) #None #The link flair’s text content, or None if not flaired.
                    print(submission.locked) #False # Whether or not the submission has been locked.
                    print(submission.name) #t3_gkdz0s #Fullname of the submission.
                    print(submission.num_comments) #29 #The number of comments on the submission.
                    print(submission.over_18) #False #Whether or not the submission has been marked as NSFW.
                    print(submission.permalink) #/r/COVID/comments/gkdz0s/rcovid_has_its_own_chatroom_if_link_doesnt_work/ #A permalink for the submission.
                    print(submission.saved) #False #Whether or not the submission is saved.
                    print(submission.score) #26 #The number of upvotes for the submission.
                    print(submission.selftext) # #The submissions’ selftext - an empty string if a link post.
                    print(submission.spoiler) #False #Whether or not the submission has been marked as a spoiler.
                    print(submission.stickied) #True #Whether or not the submission is stickied.
                    print(submission.subreddit) #COVID #Provides an instance of Subreddit.
                    print(submission.title) #/r/COVID has it's own chatroom! (If link doesn't work, check the sidebar. #The title of the submission.
                    print(submission.upvote_ratio) #0.94 #The percentage of upvotes from all votes on the submission.
                    print(submission.url) #https://www.reddit.com/chat/r/covid/channel/72771897_d260d801faccd540fb5b64df32f53528520d34cb #The URL the submission links to, or the permalink if a selfpost.
                    # print(submission.link_flair_template_id) #The link flair’s ID, or None if not flaired.
                    # print(submission.poll_data) #A PollData object representing the data of this submission, if it is a poll submission.
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
