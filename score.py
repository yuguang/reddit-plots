from __future__ import print_function #python 3 support
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import pandas as pd
from connect import engine

# average score compared to comment length
df = pd.read_sql_query("""SELECT AVG(score::FLOAT) as avg_score, count as comment_length FROM reddit_comments WHERE count < 2000 GROUP BY comment_length ORDER BY comment_length ASC;""", engine)
layout = Layout(title="Average Score vs Comment Length", yaxis=YAxis(title="Avg. Score"), xaxis=XAxis(title="Comment Length (in words)"))
data = [Scatter(name='comment length vs avg score', y=df.avg_score, x=df.comment_length, mode='markers')]
py.plot(Figure(data=data,layout=layout))

# median and quartile scores compared to comment length
df = pd.read_sql_query("""SELECT comment_length, MIN(lower_bound::INT) as minimum, MIN(upper_bound::INT) as maximum, MIN(lower_qt::INT) AS lower_qt, MIN(median::INT) AS median, MIN(upper_qt::INT) AS upper_qt
FROM
( SELECT count as comment_length,
PERCENTILE_CONT(0.02) WITHIN GROUP (ORDER BY score::INT) OVER(PARTITION BY count) AS lower_bound,
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY score::INT) OVER(PARTITION BY count) AS lower_qt,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score::INT) OVER(PARTITION BY count) AS median,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY score::INT) OVER(PARTITION BY count) AS upper_qt,
PERCENTILE_CONT(0.98) WITHIN GROUP (ORDER BY score::INT) OVER(PARTITION BY count) AS upper_bound
FROM reddit_comments WHERE count < 2000) GROUP BY comment_length;""", engine)
# plot in high charts
for line in df.sort_values(by='comment_length').values:
    print("[", line[0], ",", line[1], ",", line[3], ",", line[4], ",", line[5], ",", line[2], "],")
