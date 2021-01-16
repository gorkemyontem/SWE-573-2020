import praw
import os
import environ
import requests
import base64
import pprint
import json
from .models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis, TagMeAnalysis, TagMeSentenceAnalysis
from scraper.models import Comments, Submission
from datetime import datetime
from django.core.cache import cache
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
            sentenceAnalysis = AnalysisModelService.save_sentence_analysis(comment.comment_id, comment.submission.submission_id, comment.subreddit.subreddit_id, comment.redditor.redditor_id, sentence.sentiment.polarity, sentence.sentiment.subjectivity, sentence, 'body', index, sentence.words, sentence.noun_phrases, comment.created_utc )
            AnalyserService.analyse_tagme(sentence, sentenceAnalysis)
            
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
                sentenceAnalysis = AnalysisModelService.save_sentence_analysis("submission", submission.submission_id, submission.subreddit.subreddit_id, submission.redditor.redditor_id, sentence.sentiment.polarity, sentence.sentiment.subjectivity, sentence, 'title+body', index, sentence.words, sentence.noun_phrases, submission.created_utc)
                AnalyserService.analyse_tagme(sentence, sentenceAnalysis)
            if index == 0:
                index = 1
                
            AnalysisModelService.save_submission_analysis(submission, blob.sentiment.polarity, blob.sentiment.subjectivity, blob.words, blob.noun_phrases, total_polarity/index, total_subjectivity/index)
            submission.is_analized = True
            submission.save()
    
    @staticmethod
    def analyse_tagme(sentenceText, sentenceAnalysis):
        response = requests.get('https://tagme.d4science.org/tagme/tag?lang=en&gcube-token=' + env('TAGME_TOKEN') + "&text=" + sentenceText)
        if response.status_code < 300:
            tagsRaw = json.loads(response.text)
            if tagsRaw is not None and tagsRaw['annotations'] is not None: 
                for annotation in tagsRaw['annotations']:
                    if 'title' in annotation:
                        tagmeanalysis = AnalysisModelService.save_tagme_analysis(annotation['id'], annotation['spot'], annotation['start'], annotation['link_probability'], annotation['rho'], annotation['end'], annotation['title'])
                        AnalysisModelService.save_tagme_sentence_analysis(tagmeanalysis, sentenceAnalysis)
                        sentenceAnalysis.is_analized = True
                        sentenceAnalysis.save()
                    else: 
                        print("title NOT FOUND")


class AnalysisModelService:

    @staticmethod
    def save_tagme_analysis(tagme_id, spot, start, link_probability, rho, end, title):
        try:
            tagMeAnalysis = TagMeAnalysis.objects.get(spot=spot, title=title)
            print("====== exist tagme ======")
            return tagMeAnalysis
        except TagMeAnalysis.DoesNotExist: 
            print("====== doesnt exist ======")
            tagMeAnalysis = TagMeAnalysis()
            tagMeAnalysis.tagme_id = tagme_id
            tagMeAnalysis.spot = spot
            tagMeAnalysis.start = start
            tagMeAnalysis.link_probability = link_probability
            tagMeAnalysis.rho = rho
            tagMeAnalysis.end = end
            tagMeAnalysis.title = title
            tagMeAnalysis.save()
            return tagMeAnalysis
       
    @staticmethod
    def save_tagme_sentence_analysis(tagmeanalysis, sentenceanalysis):
        tagmesentenceanalysis = TagMeSentenceAnalysis()
        tagmesentenceanalysis.tagmeanalysis = tagmeanalysis
        tagmesentenceanalysis.sentenceanalysis = sentenceanalysis
        tagmesentenceanalysis.save()
        return tagmesentenceanalysis

    @staticmethod
    def save_sentence_analysis(comment_id, submission_id, subreddit_id, author_id, polarity, subjectivity, text, text_type, order, words, noun_phrases, created_utc):
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
        sentenceAnalysis.reddit_created_utc = created_utc
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
        commentAnalysis.reddit_created_utc = comment.created_utc
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
        submissionAnalysis.reddit_created_utc = submission.created_utc
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
