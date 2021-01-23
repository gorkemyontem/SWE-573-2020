import os
import environ
import requests
import json
from .models import SentenceAnalysis, SubmissionAnalysis, CommentAnalysis, TagMeAnalysis, TagMeSentenceAnalysis
from scraper.models import Comments, Submission
from textblob import TextBlob
import time
from django.core.cache import cache
import re

env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(__file__)) + '\.env'
environ.Env.read_env(ENV_DIR)

class AnalyserService:

    @staticmethod
    def polarity_analysis_comment(comment):
        # print(comment.comment_id)
        blob = TextBlob(comment.body)
        index = 0
        total_polarity = 0.0
        total_subjectivity = 0.0
        try: 
            for sentence in blob.sentences:
                if len(sentence.stripped) < 10:
                    continue

                index += 1
                total_polarity += sentence.sentiment.polarity
                total_subjectivity += sentence.sentiment.subjectivity
                AnalysisModelService.save_sentence_analysis(comment.comment_id, comment.submission.submission_id, comment.subreddit.subreddit_id, comment.redditor.redditor_id, sentence.sentiment.polarity, sentence.sentiment.subjectivity, sentence, 'body', index, sentence.words, sentence.noun_phrases, comment.created_utc )
            if index == 0:
                index = 1
            AnalysisModelService.save_comment_analysis(comment, blob.sentiment.polarity, blob.sentiment.subjectivity, blob.words, blob.noun_phrases, total_polarity/index, total_subjectivity/index)
            comment.is_analized = True
            comment.save()
            print("saved =>", comment.comment_id)
        except Exception as e:
            print("Oops [polarity_analysis_comment]!  Try again..." + str(e) + comment.comment_id)

    @staticmethod
    def polarity_analysis_submission(submission):
        # print(submission.submission_id, submission.title[0:25], submission.selftext[0:25])
        blobText = submission.title + " " + submission.selftext
        blob = TextBlob(blobText)
        index = 0
        total_polarity = 0.0
        total_subjectivity = 0.0

        try: 
            for sentence in blob.sentences:
                if len(sentence.stripped) < 10:
                    continue

                index += 1
                total_polarity += sentence.sentiment.polarity
                total_subjectivity += sentence.sentiment.subjectivity
                AnalysisModelService.save_sentence_analysis("submission", submission.submission_id, submission.subreddit.subreddit_id, submission.redditor.redditor_id, sentence.sentiment.polarity, sentence.sentiment.subjectivity, sentence, 'title+body', index, sentence.words, sentence.noun_phrases, submission.created_utc)
            if index == 0:
                index = 1
            
            AnalysisModelService.save_submission_analysis(submission, blob.sentiment.polarity, blob.sentiment.subjectivity, blob.words, blob.noun_phrases, total_polarity/index, total_subjectivity/index)
            submission.is_analized = True
            submission.save()
            print("saved =>", submission.submission_id)
        except Exception as e:
            print("Oops [polarity_analysis_submission]!  Try again..." + str(e))

    @staticmethod
    def tagme_analysis_sentences(sentenceAnalysis):
        tagsatoh = cache.get('tagsatoh')
        tagsitop = cache.get('tagsitop')
        tagsqtoz = cache.get('tagsqtoz')
        tagsrest = cache.get('tagsrest')
        # print(sentenceAnalysis.id)
        try: 
            for tagMeAnalysisId in AnalyserService.run_tagme_and_get_array(sentenceAnalysis.text, tagsatoh, tagsitop, tagsqtoz, tagsrest): 
                AnalysisModelService.save_tagme_sentence_analysis(tagMeAnalysisId, sentenceAnalysis)   

            sentenceAnalysis.is_analized = True
            sentenceAnalysis.save()
            print("saved =>", sentenceAnalysis.submission_id)
        except Exception as e:
            print("Oops [tagme_analysis_sentences]!  Try again..." + str(e))

            
    @staticmethod
    def run_tagme_and_get_array(text, tagsatoh, tagsitop, tagsqtoz, tagsrest):
        # print('https://tagme.d4science.org/tagme/tag?lang=en&gcube-token=' + env('TAGME_TOKEN') + "&text=" + text)
        response = requests.get('https://tagme.d4science.org/tagme/tag?lang=en&gcube-token=' + env('TAGME_TOKEN') + "&text=" + text)
        registeredTagMeAnalysisList = []
        if response.status_code > 299:
            print("[run_tagme_and_get_array]: RESPONE ERROR", response.status_code, text)
            return registeredTagMeAnalysisList
        tagsRaw = json.loads(response.text) 
        if tagsRaw is None:
            print("[run_tagme_and_get_array]: tagsRaw NOT FOUND", text)
            return registeredTagMeAnalysisList

        if tagsRaw['annotations'] is None: 
            print("[run_tagme_and_get_array]: annotations NOT FOUND", text)
            return registeredTagMeAnalysisList

        if not tagsRaw['annotations'] : 
            print("[run_tagme_and_get_array]: annotations empty []", text)
            return registeredTagMeAnalysisList
        

        # t1 = time.perf_counter()
        for annotation in tagsRaw['annotations']:
            if 'title' in annotation:
                tagmeanalysisId = AnalysisModelService.save_tagme_analysis(annotation['id'], annotation['spot'], annotation['start'], annotation['link_probability'], annotation['rho'], annotation['end'], annotation['title'], tagsatoh, tagsitop, tagsqtoz, tagsrest)
                registeredTagMeAnalysisList.append(tagmeanalysisId)
            else: 
                print("[run_tagme_and_get_array]: title NOT FOUND")

        # t2 = time.perf_counter()
        # print(f'all saving and checking tags step {round(t2-t1)} seconds')
        return registeredTagMeAnalysisList


class AnalysisModelService:

    @staticmethod
    def save_tagme_analysis(tagme_id, spot, start, link_probability, rho, end, title, tagsatoh, tagsitop, tagsqtoz, tagsrest):

        if re.match('^[a-h,A-H]', spot): 
            findings = [item for item in tagsatoh if item[1] == spot and item[2] == title]
        if re.match('^[i-p,I-P]', spot):
            findings = [item for item in tagsitop if item[1] == spot and item[2] == title]
        if re.match('^[q-z,Q-Z]', spot): 
            findings = [item for item in tagsqtoz if item[1] == spot and item[2] == title]
        else: 
            findings = [item for item in tagsrest if item[1] == spot and item[2] == title]

        if findings: 
            # print("*CACHE*")
            return findings[0][0] 
        try: 
            tagMeAnalysis = TagMeAnalysis.objects.get(spot=spot, title=title)
            # print("Exist")
            return tagMeAnalysis.id
        except TagMeAnalysis.DoesNotExist: 
            print("DoesNotExist")
            tagMeAnalysis = TagMeAnalysis()
            tagMeAnalysis.tagme_id = tagme_id
            tagMeAnalysis.spot = spot
            tagMeAnalysis.start = start
            tagMeAnalysis.link_probability = link_probability
            tagMeAnalysis.rho = rho
            tagMeAnalysis.end = end
            tagMeAnalysis.title = title
            tagMeAnalysis.save()
            return tagMeAnalysis.id
       
    @staticmethod
    def save_tagme_sentence_analysis(tagMeAnalysisId, sentenceanalysis):
        # HACK
        tagMeAnalysis = TagMeAnalysis()
        tagMeAnalysis.id = tagMeAnalysisId
        tagmesentenceanalysis = TagMeSentenceAnalysis()
        tagmesentenceanalysis.tagmeanalysis = tagMeAnalysis
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
                    flattened.append(val[:100])
            else:
                flattened.append(sublist[:100])
        
        return flattened
