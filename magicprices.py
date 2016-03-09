#!/usr/bin/env python

# initialize timer
import time
start_time = time.time()

import TCGplayer

# Get the complete current list of MTG sets
MTGSetList = TCGplayer.getSetList()

## #Choose a random set
## import random
## set = random.choice(MTGSetList)
    
## # Get the price list for one MTG set
## PriceGuide = TCGplayer.getPriceGuideForSet(set)
## print PriceGuide

# Get the price lists for all MTG sets
ComprehensivePG = { }
for MTGset in MTGSetList:
    PriceGuide = TCGplayer.getPriceGuideForSet(MTGset)
    ComprehensivePG[MTGset] = PriceGuide
#print ComprehensivePG[set]

# Pickle the PriceGuide
from util import getDateAndTime, getRunTime
fn = 'PriceGuide TCGPlayer ' + getDateAndTime() + getRunTime(start_time)
print fn
fh = open(fn,'w')
import pickle
pickle.dump(ComprehensivePG,fh)
fh.close()

