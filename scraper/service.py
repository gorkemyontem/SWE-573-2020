import praw
import os
import environ
import pprint
from prawcore import NotFound
from django.core.serializers.python import Serializer
from .models import Subreddit, Submission, AuthorRedditor, Comments
from datetime import datetime
from django.utils import timezone
from django.utils.text import Truncator

env = environ.Env()
ENV_DIR =  os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
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


class ScraperService:

    @staticmethod
    def subreddit_search(searchText, limit):
        try:
            reddit = RedditAuth.public_auth()
            searchedSubmissions = reddit.subreddit("all").search(searchText, limit=limit) # API REQUEST
            ScraperService.save_all(searchedSubmissions, True)
        except Exception as e:
            print("Oops! [subreddit_search] Try again..." + str(e))

    @staticmethod
    def save_all(submissions, includeComments = False):
        try:
            submissionIndex = 0
            for submissionRes in submissions:
                submissionIndex += 1
                ScraperService.save_single(submissionRes, includeComments)
                # print(f'{submissionIndex} => {submissionRes.name}')

        except Exception as e:
            print("Oops [save_all]!  Try again..." + str(e))


    @staticmethod
    def scrape_single_submission(submission):
        try:
            reddit = RedditAuth.public_auth()
            submissionRes = reddit.submission(id=submission.submission_id)
            ScraperService.save_single(submissionRes, True)
        except Exception as e:
            print("Oops [scrape_bulk_submission]!  Try again..." + str(e))


    @staticmethod
    def save_single(submissionRes, includeComments = True):
        try:
            subreddit, isSubredditAlreadyExist = RedditModelService.save_subreddit(submissionRes.subreddit)
            if(not hasattr(submissionRes, 'author') or not hasattr(submissionRes.author, 'id')):
                return
            redditor, isSubmissionAuthorAlreadyExist = RedditModelService.save_author(submissionRes.author) 
            submission, isSubmissionAlreadyExist = RedditModelService.save_submission(submissionRes, subreddit, redditor) 
            if includeComments:
                submissionRes.comments.replace_more(limit=None)
                #### DEBUG 
                commentsCount = len(submissionRes.comments.list())
                print(submissionRes.id, commentsCount)
                commentIndex = 0
                #### DEBUG 
                for commentRes in submissionRes.comments.list():
                    commentIndex += 1
                    if(not hasattr(commentRes, 'author') or not hasattr(commentRes.author, 'id')):
                        continue
                    
                    if(commentRes.author is not None):
                        commentRedditor, isCommentAuthorAlreadyExist = RedditModelService.save_author(commentRes.author) 
                        comment, isCommentAlreadyExist = RedditModelService.save_comment(commentRes, subreddit, submission, commentRedditor) 
                        print(f'{commentIndex}/{commentsCount} => {commentRes.name}')

        except Exception as e:
            print("Oops [save_single]!  Try again..." + str(e))

class RedditModelService:

    @staticmethod
    def save_subreddit(subredditRes):
        try:
            subreddit = Subreddit.objects.get(subreddit_id=subredditRes.id)
            return subreddit, True
        except Subreddit.DoesNotExist:
            subreddit = Subreddit()
            subreddit.subreddit_id = subredditRes.id
            subreddit.name  = subredditRes.name
            subreddit.display_name  = subredditRes.display_name
            subreddit.description  = Truncator(subredditRes.description).chars(4800)
            subreddit.description_html  = Truncator(subredditRes.description_html).chars(4800)
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
            return subreddit, False


    @staticmethod
    def save_author(authorRes):
        try:
            redditor = AuthorRedditor.objects.get(redditor_id=authorRes.id)
            return redditor, True
        except AuthorRedditor.DoesNotExist:
            redditor = AuthorRedditor()
            redditor.redditor_id = authorRes.id                                   
            redditor.name = authorRes.name                                   
            redditor.comment_karma = authorRes.comment_karma
            redditor.link_karma = authorRes.link_karma
            redditor.total_karma = authorRes.total_karma
            redditor.verified = authorRes.verified
            redditor.created_utc = datetime.fromtimestamp(authorRes.created_utc, tz=timezone.utc)                                  
            redditor.save()
            return redditor, False

    @staticmethod
    def save_submission(submissionRes, subreddit, redditor):
        try:
            submission = Submission.objects.get(submission_id=submissionRes.id)
            return submission, True
        except Submission.DoesNotExist:
            submission = Submission()
            submission.subreddit = subreddit
            submission.redditor = redditor
            submission.submission_id = submissionRes.id
            submission.name = submissionRes.name
            submission.title = submissionRes.title
            submission.url = submissionRes.url
            submission.selftext = Truncator(submissionRes.selftext).chars(4800)
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
            return submission, False
                        
    @staticmethod
    def save_comment(commentRes, subreddit, submission, redditor):
        try:
            comment = Comments.objects.get(comment_id=commentRes.id)
            return comment, True
        except Comments.DoesNotExist:
            comment = Comments()
            comment.comment_id = commentRes.id
            comment.subreddit = subreddit
            comment.submission = submission
            comment.redditor = redditor
            comment.name = commentRes.name
            comment.permalink = commentRes.permalink
            comment.link_id = commentRes.link_id
            comment.parent_id = commentRes.parent_id
            comment.body = Truncator(commentRes.body).chars(4800)
            comment.body_html = Truncator(commentRes.body_html).chars(4800)
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
            return comment, False

