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
#
# import textblob  
from textblob import TextBlob

# from textblob import TextBlob, Word, Blobber
# from textblob.classifiers import NaiveBayesClassifier
# from textblob.taggers import NLTKTagger

env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(__file__)) + '\.env'
environ.Env.read_env(ENV_DIR)

class AnalyserService:

    @staticmethod
    def analyse_text():
        text = '''
        The titular threat of The Blob has always struck me as the ultimate movie
        monster: an insatiably hungry, amoeba-like mass able to penetrate
        virtually any safeguard, capable of--as a doomed doctor chillingly
        describes it--"assimilating flesh on contact.
        Snide comparisons to gelatin be damned, it's a concept with the most
        devastating of potential consequences, not unlike the grey goo scenario
        proposed by technological theorists fearful of
        artificial intelligence run rampant.
        '''
        print(text)

        # blob = TextBlob(text)
        # blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
        #                     #  ('threat', 'NN'), ('of', 'IN'), ...]

        # blob.noun_phrases   # WordList(['titular threat', 'blob',
        #                     #            'ultimate movie monster',
        #                     #            'amoeba-like mass', ...])

        # for sentence in blob.sentences:
        #     pprint.pprint(vars(sentence))
        #     print(sentence.sentiment.polarity)
