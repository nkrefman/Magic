#!/usr/bin/env python

def getDateAndTime( ):

    import time
    DateAndTime = time.strftime("%Y-%m-%d %Ih%Mm%Ss%p ") # ex. output: '2015-08-26 03:38:35PM '

    return DateAndTime

def getRunTime(start_time):
    
    import time
    runSecs = round((time.time() - start_time),2)
    m, s = divmod(runSecs, 60)
    h, m = divmod(m, 60)
    runTime = "RT%dh%02dm%02ds" %  (h, m, s)

    return runTime
