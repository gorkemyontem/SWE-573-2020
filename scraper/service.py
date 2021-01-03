import praw
import os
import environ
from django.core.serializers.python import Serializer
from .models import Subreddit, Submission, AuthorRedditor, Comments
from datetime import datetime
from django.utils import timezone
from django.utils.text import Truncator
import pprint

env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(__file__)) + '\.env'
environ.Env.read_env(ENV_DIR)

class RedditAuth:

    @staticmethod
    def public_auth():
        reddit = praw.Reddit(client_id=env('REDDIT_CLIENT_ID'),
                             client_secret=env('REDDIT_CLIENT_SECRET'),
                             user_agent=env('REDDIT_USER_AGENT'))
        # print(reddit.read_only)
        return reddit

    @staticmethod
    def private_auth():
        reddit = praw.Reddit(client_id=env('REDDIT_CLIENT_ID'),
                             client_secret=env('REDDIT_CLIENT_SECRET'),
                             user_agent=env('REDDIT_USER_AGENT'),
                             username=env('REDDIT_USERNAME'),
                             password=env('REDDIT_PASSWORD'))
        # print(reddit.read_only)
        return reddit


class ScrapperService:
    @staticmethod
    def search_subreddit(searchText, limit):
        # todo searchtext yoksa eger??
        try:
            reddit = RedditAuth.public_auth()
            subredditRes = reddit.subreddit(searchText) # API REQUEST
            subreddit = ScrapperService.save_subreddit(subredditRes)
            pprint.pprint(vars(subredditRes))
            
            # print(20*'=' + " hot")
            # hot100submissions = subredditRes.hot(limit=limit)
            # ScrapperService.save_subreddit_tree(subreddit, hot100submissions)

            # print(20*'=' + " new")
            # new100submissions = subredditRes.new(limit=limit)
            # ScrapperService.save_subreddit_tree(subreddit, new100submissions)

            print(20*'=' + " controversial")
            controversial100submissions = subredditRes.controversial(limit=limit)
            ScrapperService.save_subreddit_tree(subreddit, controversial100submissions)

            print(20*'=' + " top")
            top100submissions = subredditRes.top(limit=limit)
            ScrapperService.save_subreddit_tree(subreddit, top100submissions)

            # print(20*'=' + " gilded")
            # gilded100submissions = subredditRes.gilded(limit=limit)
            # ScrapperService.save_subreddit_tree(subreddit, gilded100submissions)

        except Exception as e:
            print("Oops!  Try again..." + str(e))

    @staticmethod
    def save_subreddit_tree(subreddit, submissions):
        try:
            for submissionRes in submissions:
                if(not hasattr(submissionRes, 'author') or not hasattr(submissionRes.author, 'id')):
                    continue
                redditor = ScrapperService.save_author(submissionRes.author) 
                submission = ScrapperService.save_submission(submissionRes, redditor) 
                # submissionRes.comments.replace_more(limit=None)
                # for commentRes in submissionRes.comments.list():
                #     comment = ScrapperService.save_comment(commentRes, subreddit, submission, redditor) 
        except Exception as e:
            print("Oops [save_subreddit_tree]!  Try again..." + str(e))

    @staticmethod
    def save_subreddit(subredditRes):
        try:
            subreddit = Subreddit.objects.get(subreddit_id=subredditRes.id)
            print("====== exist subreddit ======")
            return subreddit
        except Subreddit.DoesNotExist:
            print("====== DoesNotExist subreddit ======")
            subreddit = Subreddit()
            subreddit.subreddit_id = subredditRes.id
            subreddit.name  = subredditRes.name
            subreddit.display_name  = subredditRes.display_name
            subreddit.description  = Truncator(subredditRes.description).chars(4999)
            subreddit.description_html  = Truncator(subredditRes.description_html).chars(4999)
            subreddit.subscribers  = subredditRes.subscribers
            subreddit.created_utc = datetime.fromtimestamp(subredditRes.created_utc, tz=timezone.utc)
            subreddit.save()
            return subreddit

    @staticmethod
    def save_author(authorRes):
        try:
            redditor = AuthorRedditor.objects.get(redditor_id=authorRes.id)
            print("====== exist author ======")
            return redditor
        except AuthorRedditor.DoesNotExist:
            print("====== DoesNotExist author ======")
            redditor = AuthorRedditor()
            redditor.redditor_id = authorRes.id                                   
            redditor.name = authorRes.name                                   
            redditor.created_utc = datetime.fromtimestamp(authorRes.created_utc, tz=timezone.utc)                                  
            redditor.save()
            return redditor

    @staticmethod
    def save_submission(submissionRes, redditor):
        # obj, created = AuthorRedditor.objects.get_or_create(first_name='John', last_name='Lennon')
        try:
            submission = Submission.objects.get(submission_id=submissionRes.id)
            print("====== exist submision ======")
            return submission
        except Submission.DoesNotExist:
            print("====== DoesNotExist submision ======")
            submission = Submission()
            submission.redditor = redditor
            submission.submission_id = submissionRes.id
            submission.name = submissionRes.name
            submission.title = submissionRes.title
            submission.url = submissionRes.url
            submission.selftext = Truncator(submissionRes.selftext).chars(4999)
            submission.num_comments = submissionRes.num_comments
            submission.score = submissionRes.score
            submission.upvote_ratio = submissionRes.upvote_ratio
            submission.created_utc =  datetime.fromtimestamp(submissionRes.created_utc, tz=timezone.utc)
            if hasattr(submissionRes, 'link_flair_template_id'):
                submission.link_flair_template_id = submissionRes.link_flair_template_id
            if hasattr(submissionRes, 'link_flair_text'):
                submission.link_flair_text = submissionRes.link_flair_text
            submission.save()
            return submission
                        
            # if hasattr(submissionRes, 'ups'):
            #     print(submissionRes.ups)
            # if hasattr(submissionRes, 'downs'):
            #     print(submissionRes.downs)

    @staticmethod
    def save_comment(commentRes, subreddit, submission, redditor):
        try:
            comment = Comments.objects.get(comment_id=commentRes.id)
            print("====== exist comment ======")
            return comment
        except Comments.DoesNotExist:
            print("====== DoesNotExist comment ======")
            comment = Comments()
            comment.comment_id = commentRes.id
            comment.subreddit = subreddit
            comment.submission = submission
            comment.redditor = redditor
            comment.parent_id = commentRes.parent_id
            comment.body = Truncator(commentRes.body).chars(4999)
            comment.body_html = Truncator(commentRes.body_html).chars(4999)
            comment.is_submitter = commentRes.is_submitter
            comment.score = commentRes.score
            comment.created_utc = datetime.fromtimestamp(commentRes.created_utc, tz=timezone.utc)
            comment.save()
            return comment
 
## reddit.subreddit('all').search('url:"https://google.com"')
# for subreddit in reddit.subreddits.default(limit=None):
#     print(subreddit)

##### PRINTING
# import pprint

# # assume you have a Reddit instance bound to variable `reddit`
# submission = reddit.submission(id="39zje0")
# print(submission.title) # to make it non-lazy
# pprint.pprint(vars(submission))




##### SUBMISSION
# # assume you have a Reddit instance bound to variable `reddit`
# submission = reddit.submission(id="39zje0")
# print(submission.title)  # Output: reddit will soon only be available ...

# # or
# submission = reddit.submission(url='https://www.reddit.com/...')

##### AUTHOR
# # assume you have a Submission instance bound to variable `submission`
# redditor1 = submission.author
# print(redditor1.name)  # Output: name of the redditor

# # assume you have a Reddit instance bound to variable `reddit`
# redditor2 = reddit.redditor("bboe")
# print(redditor2.link_karma)  # Output: u/bboe's karma


##### Comments
# # assume you have a Reddit instance bound to variable `reddit`
# top_level_comments = list(submission.comments)
# all_comments = submission.comments.list()


# # assume you have a Reddit instance bound to variable `reddit`
# submission = reddit.submission(id="39zje0")
# submission.comment_sort = "new"
# top_level_comments = list(submission.comments)
