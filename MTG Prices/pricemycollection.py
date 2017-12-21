#!/usr/bin/env python

print

import scrapeTCGP

fn = scrapeTCGP.getTCGPriceGuide()

# Unpickle the PriceGuide
fh = open(fn,'r')
import pickle
tcgPriceGuideHML = pickle.load(fh)
fh.close()

# Provide complete path to tab-delimited text file containing collection info.
# Should have 3 columns: card_name, set_name, and printing
file = '/Users/Nathaniel/Documents/06 - 2015-2017 - Postdoctoral Year Off/08 - MTG/00 - Programming/Python Scripts/V2/2017-12-21 - Krefman MTG Card Collection Raw.txt'

# Open the file
fh = open(file, 'r')
# Create a list of lists and populate with collection info
collection = [ ]
for information in fh:
    list = information.strip().split('\r')
    for item in list:
        templist=item.strip().split('\t')
        collection.append(templist)
fh.close()

setList = tcgPriceGuideHML.keys()

# Go line-by-line through the collection
for cardCount, cardInfo in enumerate(collection):

    # Tag all the non-foil cards
    if cardInfo[1] != 'set_name':
        cardName = cardInfo[0]
        cardSet = cardInfo[1]
        # Find out if it's a foil
        try:
            cardPrinting = cardInfo[2]
        # If not, append the label 'Non-Foil'
        except:
            collection[cardCount].append('Non-Foil')
            
        # Price out the cards
        if cardSet in setList:
            # Try getting the price of the card using the name and set
            try:
                collection[cardCount].extend(tcgPriceGuideHML[cardSet][cardName])

            # If the card is not found, check for alternate art variants
            except:
                # Average their max, med, and min prices
                variants = [ ]
                for card in tcgPriceGuideHML[cardSet]:
                    if card.find(cardName) > -1:
                        variants.append(tcgPriceGuideHML[cardSet][card])
                if len(variants) > 0:
                    # Calculate average max price
                    maxes = [sublist[0] for sublist in variants]
                    maxes = [float(i) for i in maxes]
                    max = sum(maxes) / float(len(maxes))
                    # Calculate average med price
                    meds = [sublist[1] for sublist in variants]
                    meds = [float(i) for i in meds]
                    med = sum(meds) / float(len(meds))
                    # Calculate average min price                    
                    mins = [sublist[2] for sublist in variants]
                    mins = [float(i) for i in mins]
                    min = sum(mins) / float(len(mins))
                    collection[cardCount].extend([str(max),str(med),str(min)])

                # Append empty values to cards that could not be priced                    
                else:
                    collection[cardCount].extend(['','',''])
                    print cardName, 'from', cardSet, 'could not be priced. [FLAG: mismatched cardname]'

        # For cards from obscure sets not in the list
        else:
            collection[cardCount].extend(['','',''])
            print cardName, 'from', cardSet, 'could not be priced. [FLAG: obscure edition]'
    else:
        collection[cardCount].extend(['TCGmax (non-foil)','TCGmed (non-foil)','TCGmin (non-foil)'])

print
    
# Save the priced-out collection to a new file
from util import getDateAndTime, getRunTime
fn = 'Collection Prices ' + getDateAndTime()[0:len(getDateAndTime())-1] + '.txt'
fh = open(fn, 'w')
for card in collection:
    counter = 0
    for x in card:
        counter += 1
        if counter != 6:
            x = str(x) + '\t'
        elif counter == 6:
            x = str(x) + '\n'
        else:
            print 'error'
        fh.write(x)
fh.close()

print 'Collection saved to file:', fn
print
