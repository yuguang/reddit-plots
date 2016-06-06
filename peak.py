import pandas as pd
from connect import engine
import json

# noinspection SqlDerivedTableAlias
peak_hour_post_by_subreddit = pd.read_sql_query("""
SELECT subreddit, hour, COUNT(created_utc) as count
FROM (
    -- truncate dates into hours
    SELECT subreddit, DATE_PART(h, created_utc) as hour, created_utc, score
    FROM comment_timestamps
        -- select the most popular subreddits
        WHERE subreddit IN (
            SELECT subreddit
            FROM reddit_comments
            GROUP BY subreddit HAVING COUNT(created_utc) > 1000
        ) ORDER BY subreddit
    )
WHERE score > 1000
-- bubcket into subreddits and hours
GROUP BY subreddit, hour
ORDER BY count DESC, subreddit, hour
;""", engine)

# noinspection SqlDerivedTableAlias
peak_weekday_post_by_subreddit = pd.read_sql_query("""
SELECT subreddit, day, COUNT(created_utc) as count
FROM (
    -- truncate dates into days
    SELECT subreddit, DATE_PART(dow, created_utc) as day, created_utc, score
    FROM comment_timestamps
        -- select the most popular subreddits
        WHERE subreddit IN (
            SELECT subreddit
            FROM reddit_comments
            GROUP BY subreddit HAVING COUNT(created_utc) > 1000
        ) ORDER BY subreddit
    )
WHERE score > 1000
-- bubcket into subreddits and days
GROUP BY subreddit, day
ORDER BY count DESC, subreddit, day
;""", engine)

# noinspection SqlDerivedTableAlias
peak_month_post_by_subreddit = pd.read_sql_query("""
SELECT subreddit, month, COUNT(created_utc) as count
FROM (
    -- truncate dates into months
    SELECT subreddit, DATE_PART(month, created_utc) as month, created_utc, score
    FROM comment_timestamps
        -- select the most popular subreddits
        WHERE subreddit IN (
            SELECT subreddit
            FROM reddit_comments
            GROUP BY subreddit HAVING COUNT(created_utc) > 100
        ) ORDER BY subreddit
    )
WHERE score > 1000
-- bubcket into subreddits and months
GROUP BY subreddit, month
ORDER BY count DESC, subreddit, month
;""", engine)

output = []
total = peak_hour_post_by_subreddit.groupby('subreddit')['count'].sum()
for line in peak_hour_post_by_subreddit.sort(['subreddit', 'hour']).values:
    subreddit, hour, count = line
    if total[subreddit] < 300:
        continue
    percent = float(count/float(total[subreddit]))
    # convert hour to PST
    output.append('\t'.join(map(lambda x: str(x), [subreddit, (int(hour) + 5)%24, percent, '\n'])))
with open('peak.tsv', 'w') as outfile:
    outfile.writelines(output)

weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']
output = []
total = peak_weekday_post_by_subreddit.groupby('subreddit')['count'].sum()
for line in peak_weekday_post_by_subreddit.sort(['subreddit', 'day']).values:
    subreddit, day, count = line
    if total[subreddit] < 300:
        continue
    percent = float(count/float(total[subreddit]))
    output.append('\t'.join(map(lambda x: str(x), [subreddit, weekdays[int(day)], percent, '\n'])))
with open('peak.tsv', 'w') as outfile:
    outfile.writelines(output)

output = []
months = ['Jan',
 'Feb',
 'Mar',
 'Apr',
 'May',
 'Jun',
 'Jul',
 'Aug',
 'Sept',
 'Oct',
 'Nov',
 'Dec']
total = peak_month_post_by_subreddit.groupby('subreddit')['count'].sum()
for line in peak_month_post_by_subreddit.sort(['subreddit', 'month']).values:
    subreddit, month, count = line
    if total[subreddit] < 10:
        continue
    percent = float(count/float(total[subreddit]))
    output.append('\t'.join(map(lambda x: str(x), [subreddit, months[int(month) - 1], percent, '\n'])))
with open('peak.tsv', 'w') as outfile:
    outfile.writelines(output)
