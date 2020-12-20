import praw
import os
import environ

env = environ.Env()
ENV_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\.env'
environ.Env.read_env(ENV_DIR)

class RedditAuth:

    @staticmethod
    def public_auth():
        reddit = praw.Reddit(client_id=env('REDDIT_CLIENT_ID'),
                             client_secret=env('REDDIT_CLIENT_SECRET'),
                             user_agent=env('REDDIT_USER_AGENT'))
        print(reddit.read_only)
        return reddit

    @staticmethod
    def private_auth():
        reddit = praw.Reddit(client_id=env('REDDIT_CLIENT_ID'),
                             client_secret=env('REDDIT_CLIENT_SECRET'),
                             user_agent=env('REDDIT_USER_AGENT'),
                             username=env('REDDIT_USERNAME'),
                             password=env('REDDIT_PASSWORD'))
        print(reddit.read_only)
        return reddit
