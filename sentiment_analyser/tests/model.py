from django.test import TestCase
from accounts.models import CustomUser
from scraper.models import Subreddit, AuthorRedditor, Submission, Comments
from analyser.models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis, TagMeAnalysis, TagMeSentenceAnalysis
import datetime
from django.utils import timezone

class TestAccountsModels(TestCase):

    def test_model_str(self): 
        email = CustomUser.objects.create(email="user@example.com")
        # username password is required
        self.assertEqual(str(email), "user@example.com")


class TestScraperModels(TestCase):

    def test_model_str_subreddit(self): 
        subreddit = Subreddit.objects.create(display_name="Covid", subreddit_id = "subreddit_id", name = "name", description = "description", description_html = "description_html", lang = "lang", subreddit_type = "subreddit_type", title = "title", url = "url", created_utc=datetime.datetime.now(tz=timezone.utc))
        self.assertEqual(str(subreddit), "Covid")

    def test_model_str_author(self): 
        author = AuthorRedditor.objects.create(name="GD3123", redditor_id ="redditor_id", created_utc=datetime.datetime.now(tz=timezone.utc))
        self.assertEqual(str(author), "GD3123")

    def test_model_str_submission(self): 
        subreddit = Subreddit.objects.create(display_name="Covid", subreddit_id = "subreddit_id", name = "name", description = "description", description_html = "description_html", lang = "lang", subreddit_type = "subreddit_type", title = "title", url = "url", created_utc=datetime.datetime.now(tz=timezone.utc))
        author = AuthorRedditor.objects.create(name="GD3123", redditor_id ="redditor_id", created_utc=datetime.datetime.now(tz=timezone.utc))
        submission = Submission.objects.create(title="The United States has over 90,000 cases", subreddit=subreddit, redditor=author, submission_id = "submission_id", name = "name", url = "url", selftext = "selftext", permalink = "permalink", category = "category", comment_sort = "comment_sort", content_categories = "content_categories", discussion_type = "discussion_type", created_utc=datetime.datetime.now(tz=timezone.utc))
        self.assertEqual(str(submission), "The United States has over 90,000 cases")

    def test_model_str_comments(self): 
        subreddit = Subreddit.objects.create(display_name="Covid", subreddit_id = "subreddit_id", name = "name", description = "description", description_html = "description_html", lang = "lang", subreddit_type = "subreddit_type", title = "title", url = "url", created_utc=datetime.datetime.now(tz=timezone.utc))
        author = AuthorRedditor.objects.create(name="GD3123", redditor_id ="redditor_id", created_utc=datetime.datetime.now(tz=timezone.utc))
        submission = Submission.objects.create(title="The United States has over 90,000 cases", subreddit=subreddit, redditor=author, submission_id = "submission_id", name = "name", url = "url", selftext = "selftext", permalink = "permalink", category = "category", comment_sort = "comment_sort", content_categories = "content_categories", discussion_type = "discussion_type", created_utc=datetime.datetime.now(tz=timezone.utc))
        comments = Comments.objects.create(name="t1_fmwlc2w", comment_id = "comment_id", subreddit=subreddit, redditor=author, submission=submission, permalink = "permalink", link_id = "link_id", parent_id = "parent_id", body = "body", body_html = "body_html", created_utc=datetime.datetime.now(tz=timezone.utc))
        self.assertEqual(str(comments), "t1_fmwlc2w")



class TestAnalyserModels(TestCase):

    def test_model_str_sentence_analysis(self): 
        sentenceAnalysis = SentenceAnalysis.objects.create(comment_id="comment_id", submission_id="submission_id", subreddit_id="subreddit_id", author_id="author_id", classification="classification", text="text", text_type="text_type", words ="{notnull}", noun_phrases = "{notnull}")
        self.assertEqual(str(sentenceAnalysis), "1")

    def test_model_str_submission_analysis(self): 
        submissionAnalysis = SubmissionAnalysis.objects.create(submission_id = "submission_id", subreddit_id = "subreddit_id", author_id = "author_id", avg_classification = "avg_classification", classification = "classification", words ="{notnull}", noun_phrases = "{notnull}")
        self.assertEqual(str(submissionAnalysis), "submission_id")

    def test_model_str_comment_analysis(self): 
        commentAnalysis = CommentAnalysis.objects.create(comment_id = "comment_id", submission_id = "submission_id", subreddit_id = "subreddit_id", author_id = "author_id", avg_classification = "avg_classification", classification = "classification", words ="{notnull}", noun_phrases = "{notnull}")
        self.assertEqual(str(commentAnalysis), "comment_id")

    def test_model_str_tagme_analysis(self): 
        tagMeAnalysis = TagMeAnalysis.objects.create(spot="donald", title="Donald Trump")
        self.assertEqual(str(tagMeAnalysis), "Donald Trump")

    def test_model_str_tagme_sentence_analysis(self): 
        sentenceAnalysis = SentenceAnalysis.objects.create(comment_id="comment_id", submission_id="submission_id", subreddit_id="subreddit_id", author_id="author_id", classification="classification", text="text", text_type="text_type", words ="{notnull}", noun_phrases = "{notnull}")
        tagMeAnalysis = TagMeAnalysis.objects.create(spot="donald", title="Donald Trump")
        tagMeSentenceAnalysis = TagMeSentenceAnalysis.objects.create(sentenceanalysis=sentenceAnalysis, tagmeanalysis=tagMeAnalysis)
        self.assertEqual(str(tagMeSentenceAnalysis), "1")
