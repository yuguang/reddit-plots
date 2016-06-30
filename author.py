import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import pandas as pd
from connect import engine

# number of gilded authors by subreddit
gilded_authors_by_subreddit = pd.read_sql_query("""
    SELECT subreddit, COUNT(DISTINCT author) as authors
    FROM reddit_comments
    WHERE gilded > 0
    GROUP BY subreddit
    ORDER BY authors DESC;
    """, engine)

df = gilded_authors_by_subreddit[0:100]
data = [
    Bar(
        x=df.subreddit,
        y=df.authors
    )
]
layout = Layout(title="Unique Gilded Authors by Subreddit", yaxis=YAxis(title="Gilded Authors from 2007 - 2015"))
plot_url = py.plot(Figure(data=data, layout=layout))

# number of authors with scores >1k by subreddit
upvoted_authors_by_subreddit = pd.read_sql_query("""
    SELECT subreddit, COUNT(DISTINCT author) as authors
    FROM reddit_comments
    GROUP BY subreddit
    HAVING SUM(ups) > 1000
    ORDER BY authors DESC;
    """, engine)

df = upvoted_authors_by_subreddit[0:100]
data = [
    Bar(
        x=df.subreddit,
        y=df.authors
    )
]
layout = Layout(title="Unique Upvoted Authors by Subreddit", yaxis=YAxis(title="Upvoted Authors from 2007 - 2015 (with > 1k total upvotes)"))
plot_url = py.plot(Figure(data=data, layout=layout))

# histogram of upvotes
upvote_frequency = pd.read_sql_query("""
    SELECT ups::INT, COUNT(created_utc) as frequency
    FROM reddit_comments
    WHERE ups > -1
    GROUP BY ups
    ORDER BY ups ASC;
    """, engine)

df = upvote_frequency[0:21]
data = [
    Bar(
        x=df.ups,
        y=df.frequency
    )
]
layout = Layout(title="Upvotes for Reddit submissions", yaxis=YAxis(title="Frequency"), xaxis=XAxis(title="Upvotes"))
plot_url = py.plot(Figure(data=data, layout=layout))

