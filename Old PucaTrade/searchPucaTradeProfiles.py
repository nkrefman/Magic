#!/usr/bin/env python

def searchPucaTradeProfiles(username,password):

    # initialize timer
    import time
    start_time = time.time()

    # Reference: http://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
    # Reference: http://stackoverflow.com/questions/18265376/why-i-can-log-in-amazon-website-using-python-mechanize-but-not-requests-or-urll
    
    import mechanize
    import cookielib
    import urllib

    # Initialize mechanize browser
    br = mechanize.Browser()

    # Initialize Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Set browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Uncomment to turn on debugging messages
    # br.set_debug_http(True)
    # br.set_debug_redirects(True)
    # br.set_debug_responses(True)

    # User-Agent (The reference code called this part "cheating." Not sure why.)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/40.0.3')]
    
    # Open login page
    sign_in = br.open('https://pucatrade.com/login')

    # Uncomment to list the forms available on the webpage
    # for form in br.forms():
    #     print "Form name:", form.name
    #     print form

    # At https://pucatrade.com/login, the first form is the login form.
    # Select the first form
    br.select_form(nr=0)

    # Uncomment to list the controls available in the selected form
    # for control in br.form.controls:
    #     print control

    # Input the username and password into controls 0 and 1 of the form
    br.form.controls[0].value = username
    br.form.controls[1].value = password

    # Submit the form to log in
    logged_in = br.submit()

    # Loop over each user's page
    for userNumber in range(97500,99999):
        # Open the page (slow step)
        if userNumber >= 0:
            PucaTradeUser = br.open("https://pucatrade.com/profiles/show/" + str(userNumber))
            UserProfile = PucaTradeUser.readlines()
            if (userNumber ) % 100 == 0:
                print "Checked profiles 0 through " + str(userNumber)
            #print UserProfile
            listOfProfiles = [ ]
            # Loop over all accessible user profiles
            for line in UserProfile:
                if line.find('Selling') >= 0:
                    if line.find('Wolfsden') < 0:
                        print "Selling -------->" + str(userNumber)
                        listOfProfiles.append(userNumber)
                if line.find('selling') >= 0:
                    if line.find('WHexpedition') < 0:
                        print "selling -------->" + str(userNumber)
                        listOfProfiles.append(userNumber)
                if line.find('SELLING') >= 0:
                    print "SELLING -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('For sale') >= 0:
                    print "For sale -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('for sale') >= 0:
                    print "for sale -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('FOR SALE') >= 0:
                    print "FOR SALE -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('cents') >= 0:
                    print "cents -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('CENTS') >= 0:
                    print "CENTS -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('cash') >= 0:
                    print "cash -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('CASH') >= 0:
                    print "CASH -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('0.6') >= 0:
                    print "0.6 -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                if line.find('0.7') >= 0:
                    print "0.7 -------->" + str(userNumber)
                    listOfProfiles.append(userNumber)
                    
        ## # Find the line with 'Totals' (it also has the number of cards)
        ## if line.find('Totals') >= 0:
        ##     # Cut off the nonsense on either side
        ##     line = line.split('           <h3>Totals: <span>')[1]
        ##     line = line.split(' Cards')[0]
        ##     # Get rid of the comma
        ##     line = line.split(',')
        ##     # Save the number of cards as a float
        ##     numCards = float(''.join(line))

    ## # Calculate how many pages of cards I need to iterate over
    ## import math
    ## numPages = int(math.ceil(numCards/200))

    ## ListOfCards = [ ]
    ## countingCards = 0
    
    ## # Loop over the pages of cards I have to gather the list of cards
    ## for pageNumber in range(1,numPages+1):

    ##     # Open the current page of 200 cards
    ##     PageOfHaves = br.open("https://pucatrade.com/cards/" + str(pageNumber))
    ##     Haves_200CardsPerPage = PageOfHaves.readlines()

    ##     # Loop over each line to find the cards
    ##     for line in Haves_200CardsPerPage:
    ##         # Store the expansion name
    ##         if line.find('	    <td class="expansion"><img title="') >= 0:
    ##             countingCards += 1
    ##             line = line.split('	    <td class="expansion"><img title="')[1]
    ##             mtgExpansion = line.split('"')[0]
    ##         # Store the card name
    ##         if line.find(');" onMouseout="cardOut()">') >= 0:
    ##             line = line.split(');" onMouseout="cardOut()">')[1]
    ##             mtgCard = line.split('<')[0]
    ##         # Store the current value in Puca Points    
    ##         if line.find('<td class="pv hidem-sm">') >= 0:
    ##             line = line.split('<td class="pv hidem-sm">')[1]
    ##             PucaTradeValue = line.split('<')[0]

    ##             # Append the data to the list of cards
    ##             ListOfCards.append([mtgCard,mtgExpansion,PucaTradeValue])

    ## # Pickle the Haves list
    ## from util import getDateAndTime, getRunTime
    ## fn = 'Haves PucaTrade ' + getDateAndTime() + getRunTime(start_time)
    ## fh = open(fn,'w')
    ## import pickle
    ## pickle.dump(ListOfCards,fh)
    ## fh.close()
    
    import csv
    fn = "Puca Traders of Interest"
    with open(fn + ".csv", "wb") as file:
        writer = csv.writer(file)
        writer.writerows(listOfProfiles)

username = raw_input('Puca Trade Username:  ')
import getpass
password = getpass.getpass()

br = searchPucaTradeProfiles(username, password)

