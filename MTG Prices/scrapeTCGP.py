#!/usr/bin/env python


def getSetList( ):

    import urllib

    # Get set names from tcgplayer.com

    print "GENERATING LIST OF SETS FROM TCGPLAYER.COM..."
    print
    
    tcgplayer = "http://magic.tcgplayer.com/magic_price_guides.asp"
    urlcontents = urllib.urlopen(tcgplayer)
    rawsets = urlcontents.readlines()

    # Initialize a list for storing sets
    MTGSetList = [ ]

    # Loop through lines of the webpage
    for x in rawsets:

        # Find lines that contain 'http://magic.tcgplayer.com/db/search_result.asp?Set_Name='
        if x.find('http://magic.tcgplayer.com/db/search_result.asp?Set_Name=') > -1:
            temp = x[98:].strip('\">\r\n')
            MTGSetList.append(temp)
        # Find lines that contain 'http://shop.tcgplayer.com/price-guide/magic/'
        if x.find('http://shop.tcgplayer.com/price-guide/magic/') > -1:
            # split them on quotation marks
            temp = x.split('\"')
            # Loop through each piece after splitting
            for y in temp:
                # Find the pieces that contain '>'
                if y.find('>') > -1:
                    temp2 = y.split('</')
                    # If the line doesn't contain 'border', add the set to the list of sets
                    if temp2[0][1:].find('border') == -1:
                        MTGSetList.append(temp2[0][1:])        

    #Add Commander 2013-2015 which don't otherwise appear...
    MTGSetList.append('Commander 2013')
    MTGSetList.append('Commander 2014')
    MTGSetList.append('Commander 2015')
    MTGSetList.append('Elspeth vs. Kiora')
    MTGSetList.append('Unique and Miscellaneous Promos')

    # Make a list of unique sets (some are listed redundantly)
    setofsets = set(MTGSetList)
    MTGSetList = list(setofsets)
    # Sort alphabetically
    MTGSetList.sort()
    
    return MTGSetList


def getPriceGuideForSet(MTGset):

    import urllib

    # Replace spaces with plus signs & generate the URL
    MTGsetURLFormatted = MTGset

    # Correct names that don't match to URLs
    if (MTGsetURLFormatted.find(' vs. ') > -1):
        if (MTGsetURLFormatted.find('Duel Decks: ') == -1):
            MTGsetURLFormatted = 'Duel Decks: ' + MTGsetURLFormatted
    if (MTGsetURLFormatted.find('Knights vs Dragons') > -1):
        MTGsetURLFormatted = 'Duel Decks: Knights vs. Dragons'
    if (MTGsetURLFormatted.find('Modern Event Deck') > -1):
        MTGsetURLFormatted = 'Magic ' + MTGsetURLFormatted
    if (MTGsetURLFormatted.find('Sixth') > -1):
        MTGsetURLFormatted = 'Classic Sixth Edition'
    if (MTGsetURLFormatted.find('Seventh') > -1):
        MTGsetURLFormatted = '7th Edition'
    if (MTGsetURLFormatted.find('Eighth') > -1):
        MTGsetURLFormatted = '8th Edition'
    if (MTGsetURLFormatted.find('Ninth') > -1):
        MTGsetURLFormatted = '9th Edition'
    if (MTGsetURLFormatted.find('Tenth') > -1):
        MTGsetURLFormatted = '10th Edition'
    if ((MTGsetURLFormatted.find('Launch Party Cards') > -1) or (MTGsetURLFormatted.find('Release Event Cards') > -1)):
        MTGsetURLFormatted = 'Launch+Party+%26+Release+Event+Promos'
    if (MTGsetURLFormatted.find('PDS:') > -1):
        MTGsetURLFormatted = 'Premium Deck Series:' + MTGsetURLFormatted[4:]
    if (MTGsetURLFormatted.find('WPN Promos') > -1):
        MTGsetURLFormatted = 'WPN/Gateway Promos'

    PriceGuideURL = "http://magic.tcgplayer.com/db/search_result.asp?Set_Name=" + MTGsetURLFormatted
    
    #print "Downloading prices for " + MTGset + " from URL:"
    #print PriceGuideURL

    urlcontents = urllib.urlopen(PriceGuideURL)
    rawPG = urlcontents.readlines()

    # Loop through lines of the webpage
    priceLines = [ ]
    for guideLine in rawPG:
        # Split at lines that say '<a href=\'
        temp = guideLine.split('<a href=\"')
        # Split again at '<'
        for i in temp:
            i = i.split('<')
            # Add the split lines to a list
            for j in i:
                priceLines.append(j)

    # Function to test whether a string is a number            
    def is_number(s): # s is a string
        try:
            float(s)
            return True
        except ValueError:
            return False

    # Import regex for regular expressions    
    import re

    # Initialize a dictionary to store the prices for each card
    PriceGuide = { } # Format: {'Card Name': [$High,$Med,$Low]}
              
    for priceline in priceLines:
        
        # Separate the card name or price from the leading text
        if (priceline.find('magic_single_card.asp?cn=') > -1) or (priceline.find('N/A') > -1):
            # For cards with no prices, make the line '00>00'
            # so the line so it can be split on '>' into two 2 items
            if priceline.find('N/A') > -1:
                priceline = '00>00'
                
            # Split the pricelines on '>'
            j = priceline.split('>')

            # If the second character of the second item of the list
            # is not a number (i.e. if it's a letter), or if the
            # second item contains letters at all

            try:
                
                if (False == (is_number(j[1][1])) or (re.search('[a-zA-Z]', j[1]))):
                    # Initialize a counter
                    counter = 1
                    # The cardname is the second item of the list
                    cardname = j[1]
                    # Initialize a list to store the high, med, and low prices
                    prices = [ ]

                # Otherwise the second item of the list is a price
                else:
                    priceStr = j[1][1:]

                    # Try making it a float
                    try:
                        price = float(priceStr)
                    # If it fails, it has a comma. So split it at the comma,
                    # and join the fragments, then float it.
                    except:
                        priceStr = priceStr.split(',')
                        priceStr = priceStr[0] + priceStr[1]
                        price = float(priceStr)
                    # Add the price to the list of prices
                    prices.append(price)
                    # Increment the counter
                    counter += 1

            except:

                print 'Making an exception for X'
                print j[1]
                # Need an exception for the Unstable card "X" because it is only 1 letter long
                if (j[1] == 'X'):

                    # Initialize a counter
                    counter = 1
                    # The cardname is the second item of the list
                    cardname = j[1]
                    # Initialize a list to store the high, med, and low prices
                    prices = [ ]

                # Otherwise the second item of the list is a price
                else:
                    priceStr = j[1][1:]

                    # Try making it a float
                    try:
                        price = float(priceStr)
                    # If it fails, it has a comma. So split it at the comma,
                    # and join the fragments, then float it.
                    except:
                        priceStr = priceStr.split(',')
                        priceStr = priceStr[0] + priceStr[1]
                        price = float(priceStr)
                    # Add the price to the list of prices
                    prices.append(price)
                    # Increment the counter
                    counter += 1

            # After the list has three prices
            if counter == 3:
                # If there were prices above $0.00
                if prices[0] != 0:
                    # Store the card and its prices in the PriceGuide
                    PriceGuide[cardname] = prices

    #print "Finished downloading prices from " + MTGset
    #print
    return PriceGuide


def getTCGPriceGuide( ):
    
        print

        # initialize timer
        import time
        start_time = time.time()

        # Get the complete current list of MTG sets
        MTGSetList = getSetList()

        # Get the price lists for all MTG sets
        ComprehensivePG = { }

        print "FETCHING CARD PRICES FROM TCGPLAYER.COM..."
        print
        
        for MTGset in MTGSetList:
            PriceGuide = getPriceGuideForSet(MTGset)
            print MTGset + ':', len(PriceGuide), 'cards'
            if len(PriceGuide) == 0:
                print MTGset, 'has no cards! Must have generated the wrong URL!'
            ComprehensivePG[MTGset] = PriceGuide
        print
        
        # Pickle the PriceGuide
        from util import getDateAndTime, getRunTime
        fn = 'PriceGuide TCGPlayer ' + getDateAndTime()[0:len(getDateAndTime())-1]
        print 'Saved TCGPlayer price guide to file:', fn
        fh = open(fn,'w')
        import pickle
        pickle.dump(ComprehensivePG,fh)
        fh.close()


        print 'Time to fetch TCGPlayer price guide:', getRunTime(start_time)
        print
        
        return fn
