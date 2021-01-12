import praw
import os
import environ
import pprint
from .models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis
from scraper.models import Comments, Submission
from datetime import datetime
from django.utils import timezone
from django.utils.text import Truncator
from textblob import TextBlob

# from textblob import TextBlob, Word, Blobber
# from textblob.classifiers import NaiveBayesClassifier
# from textblob.taggers import NLTKTagger

env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(__file__)) + '\.env'
environ.Env.read_env(ENV_DIR)

class AnalyserService:

    @staticmethod
    def analyse_comment(comment):
        print(comment.comment_id)
        blob = TextBlob(comment.body)
        index = 0
        total_polarity = 0.0
        total_subjectivity = 0.0
        for sentence in blob.sentences:
            index += 1
            total_polarity += sentence.sentiment.polarity
            total_subjectivity += sentence.sentiment.subjectivity
            AnalysisModelService.save_sentence_analysis(comment.comment_id, comment.submission.submission_id, comment.subreddit.subreddit_id, comment.redditor.redditor_id, sentence.sentiment.polarity, sentence.sentiment.subjectivity, sentence, 'body', index, sentence.noun_phrases, sentence.words)

        if index == 0:
            index = 1
        AnalysisModelService.save_comment_analysis(comment, blob.sentiment.polarity, blob.sentiment.subjectivity, blob.words, blob.noun_phrases, total_polarity/index, total_subjectivity/index)
        comment.is_analized = True
        comment.save()


    @staticmethod
    def analyse_submission(submission):
            print(submission.submission_id)
            blobText = submission.title + " " + submission.selftext
            blob = TextBlob(blobText)
            index = 0
            total_polarity = 0.0
            total_subjectivity = 0.0
            for sentence in blob.sentences:
                index += 1
                total_polarity += sentence.sentiment.polarity
                total_subjectivity += sentence.sentiment.subjectivity
                AnalysisModelService.save_sentence_analysis("submission", submission.submission_id, submission.subreddit.subreddit_id, submission.redditor.redditor_id, sentence.sentiment.polarity, sentence.sentiment.subjectivity, sentence, 'title+body', index, sentence.noun_phrases, sentence.words)

            if index == 0:
                index = 1
                
            AnalysisModelService.save_submission_analysis(submission, blob.sentiment.polarity, blob.sentiment.subjectivity, blob.words, blob.noun_phrases, total_polarity/index, total_subjectivity/index)
            submission.is_analized = True
            submission.save()

class AnalysisModelService:

    @staticmethod
    def save_sentence_analysis(comment_id, submission_id, subreddit_id, author_id, polarity, subjectivity, text, text_type, order, words, noun_phrases):
        classification = AnalysisModelService.get_classification(polarity)
        sentenceAnalysis = SentenceAnalysis()
        sentenceAnalysis.comment_id = comment_id 
        sentenceAnalysis.submission_id = submission_id          
        sentenceAnalysis.subreddit_id = subreddit_id
        sentenceAnalysis.author_id = author_id
        sentenceAnalysis.polarity = round(polarity, 3)
        sentenceAnalysis.subjectivity = round(subjectivity, 3)
        sentenceAnalysis.classification = classification
        sentenceAnalysis.text = text
        sentenceAnalysis.text_type = text_type
        sentenceAnalysis.order = order
        sentenceAnalysis.words = AnalysisModelService.flatten_list(words)
        sentenceAnalysis.noun_phrases = AnalysisModelService.flatten_list(noun_phrases)
        sentenceAnalysis.save()
        return sentenceAnalysis

    @staticmethod
    def save_comment_analysis(comment, polarity, subjectivity, words, noun_phrases, avg_polarity, avg_subjectivity):
        classification = AnalysisModelService.get_classification(polarity)
        avg_classification =  AnalysisModelService.get_classification(avg_polarity)
        commentAnalysis = CommentAnalysis()
        commentAnalysis.comment_id = comment.comment_id
        commentAnalysis.submission_id = comment.submission.submission_id
        commentAnalysis.subreddit_id = comment.subreddit.subreddit_id
        commentAnalysis.author_id = comment.redditor.redditor_id
        commentAnalysis.words = AnalysisModelService.flatten_list(words)
        commentAnalysis.noun_phrases = AnalysisModelService.flatten_list(noun_phrases)
        commentAnalysis.avg_polarity = round(avg_polarity, 3)
        commentAnalysis.avg_subjectivity = round(avg_subjectivity, 3)
        commentAnalysis.avg_classification = avg_classification
        commentAnalysis.polarity = round(polarity, 3)
        commentAnalysis.subjectivity = round(subjectivity, 3)
        commentAnalysis.classification = classification
        commentAnalysis.is_submitter = comment.is_submitter
        commentAnalysis.controversiality = comment.controversiality
        commentAnalysis.score = comment.score
        commentAnalysis.ups = comment.ups
        commentAnalysis.downs = comment.downs
        commentAnalysis.depth = comment.depth
        commentAnalysis.save()
        return commentAnalysis

    @staticmethod
    def save_submission_analysis(submission, polarity, subjectivity, words, noun_phrases, avg_polarity, avg_subjectivity):
        classification = AnalysisModelService.get_classification(polarity)
        avg_classification =  AnalysisModelService.get_classification(avg_polarity)
        submissionAnalysis = SubmissionAnalysis()
        submissionAnalysis.submission_id = submission.submission_id
        submissionAnalysis.subreddit_id = submission.subreddit.subreddit_id
        submissionAnalysis.author_id = submission.redditor.redditor_id
        submissionAnalysis.words = AnalysisModelService.flatten_list(words)
        submissionAnalysis.noun_phrases = AnalysisModelService.flatten_list(noun_phrases)
        submissionAnalysis.num_comments = submission.num_comments
        submissionAnalysis.avg_polarity = round(avg_polarity, 3)
        submissionAnalysis.avg_subjectivity = round(avg_subjectivity, 3)
        submissionAnalysis.avg_classification = avg_classification
        submissionAnalysis.polarity = round(polarity, 3)
        submissionAnalysis.subjectivity = round(subjectivity, 3)
        submissionAnalysis.classification = avg_classification
        submissionAnalysis.score = submission.score
        submissionAnalysis.upvote_ratio = submission.upvote_ratio
        submissionAnalysis.downs = submission.downs
        submissionAnalysis.ups = submission.ups
        submissionAnalysis.save()
        return submissionAnalysis


    @staticmethod
    def get_classification(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'


    @staticmethod
    def flatten_list(list):
        flattened = []
        for sublist in list:
            if type(sublist).__name__ == 'list': 
                for val in sublist:
                    flattened.append(val)
            else:
                flattened.append(sublist)
        
        return flattened

        


# class SubmissionAnalysis(models.Model):
#     id = models.AutoField(primary_key=True)
#     submission_id = models.CharField(max_length=50)
#     subreddit_id = models.CharField(max_length=50)
#     author_id = models.CharField(max_length=50)
#     words = ArrayField(ArrayField(models.CharField(max_length=100, blank=True)), size=1)
#     noun_phrases = ArrayField(ArrayField(models.CharField(max_length=200, blank=True)), size=1 )
#     num_comments = models.IntegerField(default=0)
#     avg_polarity = models.FloatField(default=0.0)
#     avg_subjectivity = models.FloatField(default=0.0)
#     avg_classification = models.CharField(max_length=50)
#     polarity = models.FloatField(default=0.0)
#     subjectivity = models.FloatField(default=0.0)
#     classification = models.CharField(max_length=50)
#     score = models.IntegerField(default=0)
#     upvote_ratio = models.FloatField(default=0.0)
#     downs = models.IntegerField(default=0) 
#     ups = models.IntegerField(default=0)
#     created_utc = models.DateTimeField()

#     def __str__(self):
#         return self.submission_id











# pprint.pprint(blob.tags)
# pprint.pprint(blob.noun_phrases) 
# pprint.pprint(blob.words) 
# pprint.pprint(blob.polarity) 

# print(sentence)
# print(sentence.noun_phrases)
# print(sentence.words)
# pprint.pprint(sentence.sentiment.polarity) 
# print(sentence.sentiment.polarity)
# print(sentence.sentiment.subjectivity)
