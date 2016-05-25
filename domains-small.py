import sys, os, django
sys.path.append(os.path.join("/home/yuguang/PycharmProjects/reddit", "project"))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
django.setup()
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from reddit.models import Domain, Subreddit
import csv
import pandas as pd
from connect import engine

domains_raw = """en.wikipedia.org
reddit.com
youtube.com
i.imgur.com
imgur.com
twitter.com
amazon.com
google.com
news.bbc.co.uk
www.nytimes.com
www.flickr.com
www.imdb.com
github.com
youtu.be
pcpartpicker.com
huffingtonpost.com"""

TOP_DOMAINS = []

# get the top 20 subreddits
subreddits = pd.read_sql_query("""
SELECT subreddit
FROM reddit_comments
GROUP BY subreddit
ORDER BY COUNT(created_utc) DESC
LIMIT 20
;""", engine)

TOP_SUBREDDITS = list(subreddits)

TOP_SUBREDDITS = TOP_SUBREDDITS + ['science', 'programming']

Model = Subreddit

for domain in domains_raw.split('\n'):
    TOP_DOMAINS.append(domain)

year_months = [(2007,10),(2007,11),(2007,12)]
for year in range(2008,2016):
    for month in range(1,13):
        year_months.append((year, month))
# initialize a dictionary to keep track of domains
all_domains = defaultdict(list)
# loop through all the months and get the top 20 domains
for year, month in year_months:
    # get the sum of all domains
    padded_month = '{0:02d}'.format(month)
    domains = Model.objects.filter(month='{}-{}'.format(year, padded_month))
    total = domains.aggregate(Sum('count'))['count__sum']
    partial = 0
    for domain in TOP_SUBREDDITS:
        percentage = 0
        if Model == Subreddit:
            domain_count = Model.objects.filter(month='{}-{}'.format(year, padded_month), name=domain).aggregate(Sum('count'))['count__sum']
        else:
            domain_count = Model.objects.filter(month='{}-{}'.format(year, padded_month), name__contains=domain).aggregate(Sum('count'))['count__sum']
        if domain_count:
            percentage = float(domain_count / float(total))
            partial += percentage
            all_domains[domain].append(percentage)
        else:
            all_domains[domain].append(0)
    # calculate the percentage for "other" (leftover domains or subreddits)
    all_domains['other'].append(1 - partial)

with open('domain.csv', 'wb') as outfile:
    writer = csv.writer(outfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['month', 'domain', 'market share'])
    for domain, counts in all_domains.iteritems():
        for year, month in year_months:
            # padded_month = '{0:02d}'.format(month)
            index = year_months.index((year, month))
            writer.writerow([index, domain, counts[index]])

import unittest

class TestMain(unittest.TestCase):

    def test_counts(self):
        for domain, counts in all_domains.iteritems():
            self.assertEqual(len(counts), 99)

if __name__ == '__main__':
    unittest.main()