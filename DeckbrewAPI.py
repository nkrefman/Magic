#!/usr/bin/env python

#####
# Deckbrew API Documentation: http://deckbrew.com/api/
#####

from urllib2 import urlopen
from urllib import quote, urlretrieve
from json import load, dumps
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# key = "API_KEY"
multiverseID = str(45278)
url = 'http://api.deckbrew.com/mtg/cards'
url += '?m=' + multiverseID

response = urlopen(url)
json_obj = load(response)

for card in json_obj:
    #print card.keys()
    editions = card['editions']
    #print type(editions)
    #print len(editions)
    for i,idx in enumerate(editions):
        #print editions[i]
        if type(editions[i]) == type({}):
            print
            print editions[i]['set']
            print editions[i]['multiverse_id']
            print str(editions[i]['image_url'])
            print
