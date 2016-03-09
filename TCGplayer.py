#!/usr/bin/env python

def getSetList( ):

    import urllib

    # Get set names from tcgplayer.com

    tcgplayer = "http://magic.tcgplayer.com/all_magic_sets.asp"
    urlcontents = urllib.urlopen(tcgplayer)
    rawsets = urlcontents.readlines()

    # Initialize a list for storing sets
    MTGSetList = [ ]

    # Loop through lines of the webpage
    for x in rawsets:
        # Find lines that contain '/db/search_result.asp?Set_Name='
        if x.find('/db/search_result.asp?Set_Name=') > -1:
            # split them on quotation marks
            temp = x.split('\"')
            # Loop through each piece after splitting
            for y in temp:
                # Find the pieces that still contain '/db/search_result.asp?Set_Name='
                if y.find('/db/search_result.asp?Set_Name=') > -1:
                    # Some lines may also say 'http://magic.tcgplayer.com'
                    if y.find('http://magic.tcgplayer.com') == 0:
                        # Remove that to format them all the same
                        y = y[26:]
                    # Replace spaces with plus signs
                    y = y[31:]   
                    y = y.replace("%20", " ")
                    # Add the set to the list
                    MTGSetList.append(y)

    # Make a list of unique sets (some are listed redundantly)
    setofsets = set(MTGSetList)
    MTGSetList = list(setofsets)

    # Sort alphabetically
    MTGSetList.sort()

    return MTGSetList

def getPriceGuideForSet(MTGset):

    import urllib

    # Replace spaces with plus signs & generate the URL
    MTGsetURLFormatted = MTGset.replace(" ","+")
    PriceGuideURL = "http://magic.tcgplayer.com/db/search_result.asp?Set_Name=" + MTGsetURLFormatted
    
    print "Downloading prices for " + MTGset + " from " + PriceGuideURL

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
            if (False == is_number(j[1][1])) or (re.search('[a-zA-Z]', j[1])):

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

    print "Finished downloading prices from " + MTGset
    print
    #print PriceGuide
    return PriceGuide
