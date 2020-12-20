import praw


class RedditAuth:

    @staticmethod
    def public_auth():
        reddit = praw.Reddit(client_id='ltNTJnIBkNGAoA',
                             client_secret='C6K6s4QGwKqUD22nwSgSiOlTlKUhvQ',
                             user_agent='swe-573-covid')
        print(reddit.read_only)

        return reddit

    @staticmethod
    def private_auth():
        reddit = praw.Reddit(client_id='ltNTJnIBkNGAoA',
                             client_secret='C6K6s4QGwKqUD22nwSgSiOlTlKUhvQ',
                             user_agent='swe-573-covid',
                             username='gokmenyontem',
                             password='gokmen2904')
        print(reddit.read_only)

        return reddit
