
from django.db import connection
from collections import namedtuple
from datetime import datetime
from scraper.models import Subreddit
import json
class Params:
  def __init__(self, startDate, endDate, probability, rho, query):
    self.startDate = datetime.strptime(startDate,'%d.%m.%Y').strftime("%m-%d-%Y") 
    self.endDate = datetime.strptime(endDate,'%d.%m.%Y').strftime("%m-%d-%Y") 
    self.probability = probability
    self.rho = rho
    self.query = query

class Queries():
    @staticmethod
    def parseParameters(args):
        q = json.loads(args)
        p = Params(q["startDate"], q["endDate"], q["probability"], q["rho"], q["query"])
        return p

    @staticmethod
    def getMostCrawledSubreddits(limit):
        return Subreddit.objects.raw('SELECT s.id, s.display_name, (SELECT Count(*) FROM scraper_submission WHERE subreddit_id = s.id) as submissions_count, (SELECT Count(*) FROM scraper_comments WHERE subreddit_id = s.id) as comments_count  FROM scraper_subreddit s WHERE id in (SELECT sc.subreddit_id FROM scraper_submission sc GROUP BY sc.subreddit_id ORDER BY sc.count DESC LIMIT %s)', [limit])


    @staticmethod
    def bar30(subreddit_id, args):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT 
                                ata.title, 
                                Count(*) 
                            FROM 
                                public.analyser_sentenceanalysis AS asa 
                                INNER JOIN public.analyser_tagmesentenceanalysis AS atsa ON atsa.sentenceanalysis_id = asa.id 
                                INNER JOIN public.analyser_tagmeanalysis AS ata ON atsa.tagmeanalysis_id = ata.id 
                            WHERE 
                                is_analized = true 
                                AND ata.link_probability > {probability}
                                AND ata.rho > {rho}
                                AND ata.is_active = True
                                AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                                AND subreddit_id = '{subredditId}'
                            GROUP BY 
                                ata.title 
                            HAVING 
                                count(*) > 1 
                            ORDER BY 
                                count(*) DESC 
                            LIMIT 
                                30;
                            '''.format(subredditId=subreddit_id, startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho))
            data = Queries.unzipTuple(cursor.fetchall())
        return data

    @staticmethod
    def buble100(subreddit_id, args = ''):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT 
                                ag_count.title, 
                                ag_count.count, 
                                CASE WHEN AVG(polarity) > 0 THEN 'Positive' WHEN AVG(polarity) < 0 THEN 'Negative' ELSE 'Neutral' END 
                                FROM public.analyser_sentenceanalysis asa 
                                INNER JOIN public.analyser_tagmesentenceanalysis atsa ON atsa.sentenceanalysis_id = asa.id 
                                INNER JOIN public.analyser_tagmeanalysis ata ON ata.id = atsa.tagmeanalysis_id 
                                INNER JOIN (
                                    SELECT 
                                        ata.title, 
                                        Count(*) 
                                    FROM 
                                    public.analyser_sentenceanalysis AS asa 
                                    INNER JOIN public.analyser_tagmesentenceanalysis AS atsa ON atsa.sentenceanalysis_id = asa.id 
                                    INNER JOIN public.analyser_tagmeanalysis AS ata ON atsa.tagmeanalysis_id = ata.id 
                                    WHERE 
                                        is_analized = true 
                                        AND ata.link_probability > {probability} 
                                        AND ata.rho > {rho}
                                        AND ata.is_active = True
                                        AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                                        AND subreddit_id = '{subredditId}'
                                    GROUP BY title
                                ) AS ag_count ON ag_count.title = ata.title 
                                WHERE asa.subreddit_id = '{subredditId}'
                                GROUP BY 
                                ag_count.title, 
                                ag_count.count 
                                HAVING 
                                ag_count.count > 1 
                                ORDER BY 
                                ag_count.count DESC 
                                LIMIT 
                                100;
                    '''.format(subredditId=subreddit_id, startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho))

            data = Queries.unzipTuple(cursor.fetchall())
        return data
   
    @staticmethod
    def top10submissions(subreddit_id = 1, args = ''):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT ss.id, ss.submission_id, ss.url, ss.permalink, ss.title, ss.selftext, ss.name, ss.num_comments, ss.score, ss.subreddit_id, ss.upvote_ratio, ss.redditor_id, asa.avg_polarity, asa.avg_classification, asa.avg_subjectivity, asa.classification, asa.subjectivity, asa.polarity, asa.reddit_created_utc, asa.author_id, asa.words, asa.noun_phrases 
                            FROM scraper_submission as ss
                            INNER JOIN analyser_submissionanalysis as asa ON asa.submission_id = ss.submission_id 
                            WHERE ss.is_analized = True
                            AND ss.created_utc > '{startDate}' AND ss.created_utc < '{endDate}'
                            AND ss.subreddit_id = '{subredditId}'
                            ORDER BY ss.score DESC 
                            LIMIT 10
                    '''.format(subredditId=subreddit_id, startDate=params.startDate, endDate=params.endDate))

            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def top10comments(submission_id = 1, args = ''):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute('''
                    SELECT * FROM scraper_comments as sc
                    INNER JOIN analyser_commentanalysis as aca ON aca.comment_id = sc.comment_id 
                    WHERE sc.is_analized = True
                    AND sc.created_utc > '{startDate}' AND sc.created_utc < '{endDate}'
                    AND sc.submission_id = '{submissionId}'
                    ORDER BY sc.score DESC 
                    LIMIT 10
            '''.format(submissionId=submission_id, startDate=params.startDate, endDate=params.endDate))

            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def sentenceAnalysisOfSubmission(submission_id = '', args = ''):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT 
                                asa.id, asa.text, asa.polarity, asa.classification, asa.subjectivity, asa.words, asa.noun_phrases, 
                                string_agg(CONCAT('[spot:', ata.spot, ', ', 'title:', ata.title,  ', ', 'p:', ROUND(ata.link_probability::numeric, 2),  ', ', 'rho:', ROUND(ata.rho::numeric,2),']'), ' | ') AS entities
                            FROM analyser_sentenceanalysis AS asa 
                            INNER JOIN analyser_tagmesentenceanalysis AS atsa ON atsa.sentenceanalysis_id = asa.id 
                            INNER JOIN analyser_tagmeanalysis AS ata ON atsa.tagmeanalysis_id = ata.id 
                            WHERE asa.submission_id = '{submissionId}'
                            AND ata.link_probability > {probability} 
                            AND ata.rho > {rho}
                            AND ata.is_active = True
                            AND asa.text_type = 'title+body' 
                            GROUP BY asa.id
                            ORDER BY asa.order ASC
                    '''.format(submissionId=submission_id, probability=params.probability, rho=params.rho))
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def sentenceAnalysisOfComment(comment_id = '', args = ''):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT 
                                asa.id, asa.text, asa.polarity, asa.classification, asa.subjectivity, asa.words, asa.noun_phrases, 
                                string_agg(CONCAT('[spot:', ata.spot, ', ', 'title:', ata.title,  ', ', 'p:', ROUND(ata.link_probability::numeric, 2),  ', ', 'rho:', ROUND(ata.rho::numeric,2),']'), ' | ') AS entities
                            FROM analyser_sentenceanalysis AS asa 
                            INNER JOIN analyser_tagmesentenceanalysis AS atsa ON atsa.sentenceanalysis_id = asa.id 
                            INNER JOIN analyser_tagmeanalysis AS ata ON atsa.tagmeanalysis_id = ata.id 
                            WHERE asa.comment_id = '{commentId}' 
                            AND ata.link_probability > {probability} 
                            AND ata.rho > {rho}
                            AND ata.is_active = True
                            AND asa.text_type = 'body' 
                            GROUP BY asa.id
                            ORDER BY asa.order ASC
                    '''.format(commentId=comment_id, probability=params.probability, rho=params.rho))
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def wordCloud(subreddit_id = '', args = ''):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT word as name, Count(*) as weight 
                            FROM (SELECT unnest(words) as word FROM analyser_sentenceanalysis 
                            WHERE subreddit_id = '{subredditId}' GROUP BY words) AS wordtable
                            GROUP BY word
                            HAVING count(*) > 10
                            ORDER BY Count(*) DESC
                            LIMIT 2000
                    '''.format(subredditId=subreddit_id))
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def entityCloud(subreddit_id, args):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT 
                                ata.title as name,
                                Count(*) as weight 
                            FROM 
                                public.analyser_sentenceanalysis AS asa 
                                INNER JOIN public.analyser_tagmesentenceanalysis AS atsa ON atsa.sentenceanalysis_id = asa.id 
                                INNER JOIN public.analyser_tagmeanalysis AS ata ON atsa.tagmeanalysis_id = ata.id 
                            WHERE 
                                is_analized = true 
                                AND ata.link_probability > {probability} 
                                AND ata.rho > {rho}
                                AND ata.is_active = True
                                AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                                AND subreddit_id =  '{subredditId}'
                            GROUP BY 
                                ata.title 
                            HAVING 
                                count(*) > 1 
                            ORDER BY 
                                count(*) DESC 
                            LIMIT 
                                500;
                    '''.format(subredditId=subreddit_id, startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho))
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def network(subreddit_id, args):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor: 
            cursor.execute(''' 
                        SELECT atsa.sentenceanalysis_id AS group_id, cte.id AS id FROM analyser_tagmesentenceanalysis AS atsa
                        INNER JOIN analyser_sentenceanalysis AS asa ON asa.id = atsa.sentenceanalysis_id
                        INNER JOIN analyser_tagmeanalysis AS ata ON ata.id = atsa.tagmeanalysis_id
                        INNER JOIN (
                        SELECT row_number() over () as id, ata.title as label FROM analyser_tagmesentenceanalysis AS atsa
                            INNER JOIN analyser_sentenceanalysis AS asa ON asa.id = atsa.sentenceanalysis_id
                            INNER JOIN analyser_tagmeanalysis AS ata ON ata.id = atsa.tagmeanalysis_id
                            WHERE asa.subreddit_id = '{subredditId}'
                            AND ata.link_probability > {probability} 
                            AND ata.rho > {rho}
                            AND ata.is_active = True
                            AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                            GROUP BY ata.title
                            HAVING Count(1) > 40
                        ) AS cte ON  cte.label = ata.title
                        WHERE asa.subreddit_id = '{subredditId}'
                        AND ata.link_probability > {probability} 
                        AND ata.rho > {rho}
                        AND ata.is_active = True
                        ORDER BY atsa.sentenceanalysis_id ASC
                        LIMIT 10000
                    '''.format(subredditId=subreddit_id, startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho))
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def networkDataset(subreddit_id, args):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                        SELECT row_number() over () as id, ata.title as label FROM analyser_tagmesentenceanalysis AS atsa
                        INNER JOIN analyser_sentenceanalysis AS asa ON asa.id = atsa.sentenceanalysis_id
                        INNER JOIN analyser_tagmeanalysis AS ata ON ata.id = atsa.tagmeanalysis_id
                        WHERE asa.subreddit_id = '{subredditId}'
                        AND ata.link_probability > {probability} 
                        AND ata.rho > {rho}
                        AND ata.is_active = True
                        AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                        GROUP BY ata.title
                        HAVING Count(1) > 40
                    '''.format(subredditId=subreddit_id, startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho))
            data = Queries.dictfetchall(cursor)
        return data


    @staticmethod
    def networkSearch(args):
        params = Queries.parseParameters(args)
        with connection.cursor() as cursor: 
            cursor.execute(''' 
                        SELECT atsa.sentenceanalysis_id AS group_id, cte.id AS id FROM analyser_tagmesentenceanalysis AS atsa
                        INNER JOIN analyser_sentenceanalysis AS asa ON asa.id = atsa.sentenceanalysis_id
                        INNER JOIN analyser_tagmeanalysis AS ata ON ata.id = atsa.tagmeanalysis_id
                        INNER JOIN (
                        SELECT row_number() over () as id, ata.title as label FROM analyser_tagmesentenceanalysis AS atsa
                            INNER JOIN analyser_sentenceanalysis AS asa ON asa.id = atsa.sentenceanalysis_id
                            INNER JOIN analyser_tagmeanalysis AS ata ON ata.id = atsa.tagmeanalysis_id
                            WHERE asa.text LIKE '%{searchText}%'
                            AND ata.link_probability > {probability} 
                            AND ata.rho > {rho}
                            AND ata.is_active = True
                            AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                            GROUP BY ata.title
                        ) AS cte ON  cte.label = ata.title
                        WHERE asa.text LIKE '%{searchText}%'
                        AND ata.link_probability > {probability} 
                        AND ata.rho > {rho}
                        AND ata.is_active = True
                        ORDER BY atsa.sentenceanalysis_id ASC
                        LIMIT 10000
                    '''.format(startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho, searchText=params.query))
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def networkSearchDataset(args):
        params = Queries.parseParameters(args)
        print(params)
        with connection.cursor() as cursor:
            cursor.execute(''' 
                        SELECT row_number() over () as id, ata.title as label FROM analyser_tagmesentenceanalysis AS atsa
                        INNER JOIN analyser_sentenceanalysis AS asa ON asa.id = atsa.sentenceanalysis_id
                        INNER JOIN analyser_tagmeanalysis AS ata ON ata.id = atsa.tagmeanalysis_id
                        WHERE asa.text LIKE '%{searchText}%'
                        AND ata.link_probability > {probability} 
                        AND ata.rho > {rho}
                        AND ata.is_active = True
                        AND asa.reddit_created_utc > '{startDate}' AND asa.reddit_created_utc < '{endDate}'
                        GROUP BY ata.title
                    '''.format(startDate=params.startDate, endDate=params.endDate, probability=params.probability, rho=params.rho, searchText=params.query))
            data = Queries.dictfetchall(cursor)
        return data
						

    @staticmethod
    def stats():
        with connection.cursor() as cursor:
            cursor.execute(''' 
                        SELECT relname as dbtable, n_live_tup as dbcount
                        FROM pg_stat_all_tables
                        WHERE relname like 'analyser%' OR relname like 'scraper%'
                        ''')
            data = Queries.tupleToObject(cursor)
        return data

    @staticmethod
    def unzipTuple(arr):
        return [list(i) for i in zip(*arr)]

    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [ dict(zip(columns, row)) for row in cursor.fetchall()
        ]

    @staticmethod
    def namedtuplefetchall(cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

    @staticmethod
    def tupleToObject(cursor):
        dicto = dict()
        [ dicto.update({row[0]: row[1]}) for row in cursor.fetchall()]
        return dicto
 