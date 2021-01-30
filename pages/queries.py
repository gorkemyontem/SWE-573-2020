
from django.db import connection
from collections import namedtuple

class Queries():

    @staticmethod
    def bar30(subreddit_id):
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT 
                                ta.title, 
                                Count(*) 
                            FROM 
                                public.analyser_sentenceanalysis AS sa 
                                INNER JOIN public.analyser_tagmesentenceanalysis AS tsa ON tsa.sentenceanalysis_id = sa.id 
                                INNER JOIN public.analyser_tagmeanalysis AS ta ON tsa.tagmeanalysis_id = ta.id 
                            WHERE 
                                is_analized = true 
                                AND ta.link_probability > 0.1
                                AND sa.reddit_created_utc > '2020-12-01' AND sa.reddit_created_utc < '2021-01-08'
                                AND ta.title not in ('HTTPS', 'World Wide Web', 'Reddit', 'HTML', 'Hypertext Transfer Protocol', 'TL;DR', 'Imgur')
                                AND subreddit_id = %s 
                            GROUP BY 
                                ta.title 
                            HAVING 
                                count(*) > 1 
                            ORDER BY 
                                count(*) DESC 
                            LIMIT 
                                30;
                            ''', [subreddit_id])
            data = Queries.unzipTuple(cursor.fetchall())
        return data

    @staticmethod
    def buble100(subreddit_id):
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT 
                                ag_count.title, 
                                ag_count.count, 
                                CASE WHEN AVG(polarity) > 0 THEN 'Positive' WHEN AVG(polarity) < 0 THEN 'Negative' ELSE 'Neutral' END 
                                FROM 
                                public.analyser_sentenceanalysis sa 
                                INNER JOIN public.analyser_tagmesentenceanalysis tsa ON tsa.sentenceanalysis_id = sa.id 
                                INNER JOIN public.analyser_tagmeanalysis ta ON ta.id = tsa.tagmeanalysis_id 
                                INNER JOIN (
                                    SELECT 
                                    ta.title, 
                                    Count(*) 
                                    FROM 
                                    public.analyser_sentenceanalysis AS sa 
                                    INNER JOIN public.analyser_tagmesentenceanalysis AS tsa ON tsa.sentenceanalysis_id = sa.id 
                                    INNER JOIN public.analyser_tagmeanalysis AS ta ON tsa.tagmeanalysis_id = ta.id 
                                    WHERE 
                                    is_analized = true 
                                    AND ta.link_probability > 0.5 
                                    AND sa.reddit_created_utc > '2020-12-01' AND sa.reddit_created_utc < '2021-01-08'
                                    AND subreddit_id = %s 
                                    GROUP BY 
                                    title
                                ) AS ag_count ON ag_count.title = ta.title 
                                WHERE 
                                sa.subreddit_id = '2f4kx6' 
                                AND ag_count.title not in (
                                    'HTTPS', 'World Wide Web', 'Reddit', 
                                    'HTML', 'Hypertext Transfer Protocol'
                                ) 
                                AND (
                                    polarity < -0.1 
                                    OR polarity > 0.1
                                ) 
                                GROUP BY 
                                ag_count.title, 
                                ag_count.count 
                                HAVING 
                                ag_count.count > 1 
                                ORDER BY 
                                ag_count.count DESC 
                                LIMIT 
                                100;
                        ''', [subreddit_id])
            data = Queries.unzipTuple(cursor.fetchall())
        return data
   
    @staticmethod
    def top10submissions(subreddit_id = 1):
        with connection.cursor() as cursor:
            cursor.execute(''' 
                            SELECT * FROM scraper_submission as ss
                            INNER JOIN analyser_submissionanalysis as asa ON asa.submission_id = ss.submission_id 
                            WHERE ss.is_analized = True
                            AND ss.created_utc > '2020-12-01' AND ss.created_utc < '2021-01-08'
                            AND ss.subreddit_id = %s
                            ORDER BY ss.score DESC 
                            LIMIT 10
                        ''', [subreddit_id])
            data = Queries.dictfetchall(cursor)
        return data

    @staticmethod
    def top10comments(submission_id = 1):
        with connection.cursor() as cursor:
            cursor.execute(''' 
                    SELECT * FROM scraper_comments as sc
                    INNER JOIN analyser_commentanalysis as aca ON aca.comment_id = sc.comment_id 
                    WHERE sc.is_analized = True
                    --AND sc.created_utc > '2020-12-01' AND sc.created_utc < '2021-01-08'
                    AND sc.submission_id = 1
                    ORDER BY sc.score DESC 
                    LIMIT 10
                        ''', [submission_id])
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
 