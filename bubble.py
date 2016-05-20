import json
import pandas as pd
from connect import engine

#make a bubble chart comparing subreddits
subreddit_summary = pd.read_sql_query("""
    SELECT subreddit, AVG(score::FLOAT) AS avg_score, SUM(gilded) as gilds, COUNT(created_utc) as comments, AVG(count::FLOAT) as comment_length
    FROM reddit_comments
    GROUP BY subreddit HAVING COUNT(created_utc) > 1000
    ORDER BY avg_score DESC;
    """, engine)
# plot in high charts
import matplotlib.pyplot as plt
import matplotlib.colors as colors
Accents = plt.get_cmap('Accent')
output = []
df = subreddit_summary[:1000]
mean_comment_length = df['comment_length'].mean()
for line in df.values:
    subreddit, avg_score, gilds, comments, comment_length = line
    normalized_length = comment_length/(mean_comment_length * 2)
    if normalized_length > 1:
        normalized_length = 1
    color = Accents(normalized_length)
    r,g,b,a = color
    output.append({'x': float(int(gilds)/float(comments)), 'y': avg_score, 'z': comments, 'name': subreddit, 'color': colors.rgb2hex((r,g,b))})
with open('bubble.json', 'w') as outfile:
    json.dump(output, outfile)
