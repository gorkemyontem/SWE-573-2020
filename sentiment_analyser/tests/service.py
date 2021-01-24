import datetime
import pprint
from django.test import TestCase
from accounts.models import CustomUser
from scraper.models import Subreddit, AuthorRedditor, Submission, Comments
from analyser.models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis, TagMeAnalysis, TagMeSentenceAnalysis
from scraper.service import RedditAuth, ScraperService, RedditModelService
from analyser.service import AnalyserService
from django.utils import timezone

class TestRedditAuthService(TestCase):

    def test_public_auth(self): 
        RedditAuth.public_auth()

    def test_private_auth(self): 
        RedditAuth.private_auth()

class TestScraperService(TestCase):

    def test_subreddit_search(self): 
        ScraperService.subreddit_search("xcovidx", 2)
    
    def test_save_all(self):     
        reddit = RedditAuth.public_auth() 
        searchedSubmissions = reddit.subreddit("covid").hot(limit=1) # API REQUEST
        ScraperService.save_all(searchedSubmissions, False)

    def test_scrape_single_submission(self): 
        reddit = RedditAuth.public_auth() 
        submissionRes = reddit.submission(id="kpmrwp") 
        ScraperService.save_single(submissionRes, True)
        submission = Submission.objects.get(submission_id='kpmrwp')
        ScraperService.scrape_single_submission(submission)
        
    def test_save_single_all(self): 
        reddit = RedditAuth.public_auth() 
        submissionRes = reddit.submission(id="kpmrwp") 
        ScraperService.save_single(submissionRes, True)
        ScraperService.save_single(submissionRes, True)
   
class TestAnalyserService(TestCase):

    def test_polarity_analysis_comment(self): 
        reddit = RedditAuth.public_auth() 
        submissionRes = reddit.submission(id="kpmrwp")
        ScraperService.save_single(submissionRes, True)
        comment = Comments.objects.get(pk=1)
        AnalyserService.polarity_analysis_comment(comment)

    def test_polarity_analysis_submission(self): 
        reddit = RedditAuth.public_auth() 
        submissionRes = reddit.submission(id="kpmrwp")
        ScraperService.save_single(submissionRes, False)
        submission = Submission.objects.get(submission_id='kpmrwp')
        AnalyserService.polarity_analysis_submission(submission)

    def test_tagme_analysis_sentences(self): 
        sentenceAnalysis = SentenceAnalysis.objects.create(comment_id="comment_id", submission_id="submission_id", subreddit_id="subreddit_id", author_id="author_id", classification="classification", text="text", text_type="text_type", words ="{notnull}", noun_phrases = "{notnull}")
        AnalyserService.tagme_analysis_sentences(sentenceAnalysis)
    
    def test_run_tagme_and_get_array(self): 
        AnalyserService.run_tagme_and_get_array("Hello, Steve Job")
