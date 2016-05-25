import sys, os, django
sys.path.append(os.path.join("/home/yuguang/PycharmProjects/reddit", "project"))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
django.setup()
from collections import defaultdict
from django.db.models import Sum
from reddit.models import Domain, Subreddit
import csv

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
    domains = Domain.objects.filter(month='{}-{}'.format(year, padded_month))
    total = domains.aggregate(Sum('count'))['count__sum']
    # calculate the percentage for the domains in the dictionary and append
    for domain in domains.order_by('-count')[:50]:
        # prepend zeros to domains that just showed up this month
        if len(all_domains[domain.name]) == 0 and year_months.index((year, month)):
            all_domains[domain.name].extend([0]*(year_months.index((year, month))))
        all_domains[domain.name].append(float(domain.count / float(total)))
    # append zero to domains that don't have an entry for the month
    for domain, counts in all_domains.iteritems():
        if len(counts) < (year_months.index((year, month)) + 1):
            all_domains[domain].append(0)

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