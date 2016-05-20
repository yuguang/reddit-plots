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