#!/usr/bin/env python2

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import urllib2, json, uuid
import requests
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'examples/alice.txt')).read()
subreddit = 'AskReddit'

WIDTH = 800
HEIGHT = 600
image = Image.open('alice_color.png')
coloring = np.array(image)
wc = WordCloud(background_color="white", width=WIDTH, height=HEIGHT, max_words=500, mask=coloring,
               stopwords=STOPWORDS, min_font_size=12,
               max_font_size=40)
# generate word cloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(coloring)

# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
fig = plt.gcf()
# save wordcloud for subreddit
fig.savefig('{}.png'.format(subreddit), transparent=True)
