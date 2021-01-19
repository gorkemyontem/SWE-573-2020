
from django.db import connection

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
                                AND title not in ('HTTPS', 'World Wide Web', 'Reddit', 'HTML', 'Hypertext Transfer Protocol', 'TL;DR', 'Imgur')
                                AND subreddit_id = %s 
                            GROUP BY 
                                title 
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
    def unzipTuple(arr):
        return [list(i) for i in zip(*arr)]

