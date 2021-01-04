import praw
from prawcore import NotFound
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
    def subreddit_all(limit):
        try:
            reddit = RedditAuth.public_auth()

            allSubmissions = reddit.subreddit('all') # API REQUEST
           
            print(20*'=' + " hot " + 20*'=')
            hotSubmissions = allSubmissions.hot(limit=limit)
            ScrapperService.save_subreddit_tree(None, hotSubmissions)

            print(20*'=' + " new " + 20*'=')
            newSubmissions = allSubmissions.new(limit=limit)
            ScrapperService.save_subreddit_tree(None, newSubmissions)

            # print(20*'=' + " controversial " + 20*'=')
            # controversialSubmissions = allSubmissions.controversial(limit=limit)
            # ScrapperService.save_subreddit_tree(None, controversialSubmissions)

            print(20*'=' + " top " + 20*'=')
            topSubmissions = allSubmissions.top(limit=limit)
            ScrapperService.save_subreddit_tree(None, topSubmissions)
            
        except Exception as e:
            print("Oops! [subreddit_all] Try again..." + str(e))

    @staticmethod
    def subreddit_lookup_ondemand(searchText, limit):
        try:
            reddit = RedditAuth.public_auth()

            if not ScrapperService.subreddit_exists(reddit, searchText):
                return False

            subredditRes = reddit.subreddit(searchText) # API REQUEST
            subreddit = ScrapperService.save_subreddit(subredditRes)
            # pprint.pprint(vars(subredditRes))
            
            print(20*'=' + " hot " + 20*'=')
            hotSubmissions = subredditRes.hot(limit=limit)
            ScrapperService.save_subreddit_tree(subreddit, hotSubmissions, True)

            print(20*'=' + " new " + 20*'=')
            newSubmissions = subredditRes.new(limit=limit)
            ScrapperService.save_subreddit_tree(subreddit, newSubmissions, True)

            print(20*'=' + " controversial " + 20*'=')
            controversialSubmissions = subredditRes.controversial(limit=limit)
            ScrapperService.save_subreddit_tree(subreddit, controversialSubmissions, True)

            print(20*'=' + " top " + 20*'=')
            topSubmissions = subredditRes.top(limit=limit)
            ScrapperService.save_subreddit_tree(subreddit, topSubmissions, True)
            
            return True

        except Exception as e:
            print("Oops! [subreddit_lookup_ondemand] Try again..." + str(e))
            return False

    @staticmethod
    def subreddit_exists(reddit, sub):
        exists = True
        try:
            reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
        return exists

    @staticmethod
    def save_subreddit_tree(subreddit, submissions, includeComments = False):
        try:
            for submissionRes in submissions:
                if subreddit is None:
                    subreddit = ScrapperService.save_subreddit(submissionRes.subreddit)
                
                print(submissionRes.name)
                if(not hasattr(submissionRes, 'author') or not hasattr(submissionRes.author, 'id')):
                    continue

                redditor = ScrapperService.save_author(submissionRes.author) 
                submission = ScrapperService.save_submission(submissionRes, subreddit, redditor) 
                if includeComments:
                    submissionRes.comments.replace_more(limit=1)
                    print(len(submissionRes.comments.list()))
                    for commentRes in submissionRes.comments.list():
                        if(not hasattr(commentRes, 'author') or not hasattr(commentRes.author, 'id')):
                            continue

                        if(commentRes.author is not None):
                            commentRedditor = ScrapperService.save_author(commentRes.author) 
                            comment = ScrapperService.save_comment(commentRes, subreddit, submission, commentRedditor) 
        except Exception as e:
            print("Oops [save_subreddit_tree]!  Try again..." + str(e))

    @staticmethod
    def save_subreddit(subredditRes):
        try:
            subreddit = Subreddit.objects.get(subreddit_id=subredditRes.id)
            print("====== exist subreddit ======")
            return subreddit
        except Subreddit.DoesNotExist:
            print("====== NEW SUBREDDIT ======")
            subreddit = Subreddit()
            subreddit.subreddit_id = subredditRes.id
            subreddit.name  = subredditRes.name
            subreddit.display_name  = subredditRes.display_name
            subreddit.description  = Truncator(subredditRes.description).chars(4999)
            subreddit.description_html  = Truncator(subredditRes.description_html).chars(4999)
            subreddit.subscribers  = subredditRes.subscribers
            subreddit.lang = subredditRes.lang
            subreddit.over18 = subredditRes.over18
            subreddit.subreddit_type = subredditRes.subreddit_type
            subreddit.quarantine = subredditRes.quarantine
            subreddit.restrict_commenting = subredditRes.restrict_commenting
            subreddit.restrict_posting = subredditRes.restrict_posting
            subreddit.title = subredditRes.title
            subreddit.url = subredditRes.url
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
            redditor.comment_karma = authorRes.comment_karma
            redditor.link_karma = authorRes.link_karma
            redditor.total_karma = authorRes.total_karma
            redditor.verified = authorRes.verified
            redditor.created_utc = datetime.fromtimestamp(authorRes.created_utc, tz=timezone.utc)                                  
            redditor.save()
            return redditor

    @staticmethod
    def save_submission(submissionRes, subreddit, redditor):
        # obj, created = AuthorRedditor.objects.get_or_create(first_name='John', last_name='Lennon')
        try:
            submission = Submission.objects.get(submission_id=submissionRes.id)
            print("====== exist submision ======")
            return submission
        except Submission.DoesNotExist:
            print("====== DoesNotExist submision ======")
            submission = Submission()
            submission.subreddit = subreddit
            submission.redditor = redditor
            submission.submission_id = submissionRes.id
            submission.name = submissionRes.name
            submission.title = submissionRes.title
            submission.url = submissionRes.url
            submission.selftext = Truncator(submissionRes.selftext).chars(4999)
            submission.num_comments = submissionRes.num_comments
            submission.score = submissionRes.score
            submission.upvote_ratio = submissionRes.upvote_ratio
            submission.downs = submissionRes.downs
            submission.ups = submissionRes.ups
            submission.archived = submissionRes.archived
            submission.over_18 = submissionRes.over_18
            submission.permalink = submissionRes.permalink
            submission.category = submissionRes.category
            submission.comment_sort = submissionRes.comment_sort
            submission.content_categories = submissionRes.content_categories
            submission.discussion_type = submissionRes.discussion_type
            submission.created_utc =  datetime.fromtimestamp(submissionRes.created_utc, tz=timezone.utc)
            if hasattr(submissionRes, 'link_flair_text'):
                submission.link_flair_text = submissionRes.link_flair_text
            submission.save()
            return submission
                        
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
            comment.name = commentRes.name
            comment.permalink = commentRes.permalink
            comment.link_id = commentRes.link_id
            comment.parent_id = commentRes.parent_id
            comment.body = Truncator(commentRes.body).chars(4999)
            comment.body_html = Truncator(commentRes.body_html).chars(4999)
            comment.is_submitter = commentRes.is_submitter
            comment.score = commentRes.score
            comment.ups = commentRes.ups
            comment.downs = commentRes.downs
            comment.depth = commentRes.depth
            comment.controversiality = commentRes.controversiality
            comment.archived = commentRes.archived
            comment.comment_type = commentRes.comment_type
            comment.created_utc = datetime.fromtimestamp(commentRes.created_utc, tz=timezone.utc)
            comment.save()
            return comment
 


##### SINGLES
# submission = reddit.submission(id="39zje0")
# submission = reddit.submission(url='https://www.reddit.com/...')
# redditor2 = reddit.redditor("bboe")
# pprint.pprint(vars(submission))
