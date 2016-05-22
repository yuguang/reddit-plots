import pandas as pd
from connect import engine
from collections import defaultdict, Counter
import networkx as nx

df = pd.read_sql_query("""
SELECT subreddit_a, subreddit_b, COUNT(DISTINCT author) as authors
FROM (
SELECT a.subreddit1 as subreddit_a, b.subreddit2 as subreddit_b, a.author1 as author
FROM (
--   find the authors with the most comments that have positive scores
  SELECT author, subreddit,
--   select the top 80 percent of authors based on number of comments
  PERCENTILE_CONT(0.2) WITHIN GROUP (ORDER BY comments::INT) OVER(PARTITION BY subreddit) AS threshold
  FROM (
    SELECT author, subreddit, COUNT(created_utc) AS comments
    FROM reddit_comments
    WHERE score > 0
    GROUP BY author, subreddit
  )
) AS a(author1, subreddit1, threshold)
JOIN (
--   find the authors who have commented more than 10 times in subreddits that have more than 1k comments
  SELECT author, subreddit, COUNT(created_utc) as comments
  FROM reddit_comments
  WHERE subreddit IN (
    SELECT subreddit
    FROM reddit_comments
    GROUP BY subreddit HAVING COUNT(created_utc) > 1000
  )
  ORDER BY comments
--   get authors who have commented in the subreddit at least 10 times
  GROUP BY author, subreddit HAVING COUNT(subreddit) > 9
) AS b(author2, subreddit2, comments)
ON a.author1=b.author2
WHERE a.subreddit1!=b.subreddit2 AND b.comments > a.threshold
) 
GROUP BY subreddit_a, subreddit_b
ORDER BY authors DESC
LIMIT 70000;""", engine)

THRESHOLD = 51
related_subreddit = defaultdict(list)
subreddit_count = Counter()
# for each item in subreddit_b
for line in df.values:
    subreddit_a, subreddit_b, weight = line
    if subreddit_count[subreddit_a] < THRESHOLD and subreddit_count[subreddit_b] < THRESHOLD:
        # append subreddit_a to list in dictionary
        related_subreddit[subreddit_b].append((subreddit_a, weight))
        # keep a count of how many times a subreddit has been linked
        subreddit_count[subreddit_a] += 1
        subreddit_count[subreddit_b] += 1


G = nx.Graph()
for node, subreddits in related_subreddit.iteritems():
    # display only the top k links
    for subreddit in subreddits[:THRESHOLD]:
        name, weight = subreddit
        G.add_edge(node, name, weight=weight)

nx.draw(G)
nx.write_gexf(G, 'graph.gexf')
