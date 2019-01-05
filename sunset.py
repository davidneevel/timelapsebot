from bs4 import BeautifulSoup
import urllib2
import datetime
from time import sleep
import oled

def getSunsetTime():
    quote_page = "https://www.timeanddate.com/sun/netherlands/amsterdam"

    # query the website and return the html to the variable 'page'
    page = urllib2.urlopen(quote_page)

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    today = datetime.datetime.date
    # print today

    # Take out the <div> of name and get its value
    classThrees = soup.find_all('span', attrs={'class': 'three'})
    sunsetFull =  classThrees[1]
    # print sunsetFull
    sunsetString = str(sunsetFull)

    sunset = sunsetString[20:25]  # take the appropriate chars out of sunset string
    print "sunset tonight at ", sunset

    return sunset


def getSunriseTime():
    quote_page = "https://www.timeanddate.com/sun/netherlands/amsterdam"

    # query the website and return the html to the variable 'page'
    page = urllib2.urlopen(quote_page)

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    today = datetime.datetime.date

    # Take out the <div> of name and get its value
    classThrees = soup.find_all('span', attrs={'class': 'three'})
    sunriseFull =  classThrees[0]
    # print sunsetFull
    sunriseString = str(sunriseFull)

    sunrise = sunriseString[20:25]  # take the appropriate chars out of sunset string
    print "sunrise is at ", sunrise
    return sunrise


def wait(targetTime):
    targetHour = targetTime.seconds // 3600
    targetMin = ((targetTime.seconds)//60)%60
    print "targetHour = ", targetHour
    print "targetMin = ", targetMin

    print "waiting for the %rth hour" % targetHour

    now = datetime.datetime.now()
    while now.hour != targetHour:
    #       print "waiting for the right hour"
        now = datetime.datetime.now()
        nowHour = now.hour
        nowMin = now.minute
        #oled.display1("now it's " + str(nowHour) + ":" + str(nowMin))
        sleep(60)
    print "hour matched!"
    print "waiting for the %rth minute" % targetMin
    prevNow = now
    while now.minute != targetMin:
        now = datetime.datetime.now()
        nowHour = now.hour
        nowMin = now.minute

        if prevNow != now:
            #oled.display1("now it's " + str(nowHour) + ":" + str(nowMin))
            if now.minute == targetMin:
                #oled.display1("bout to start")   
                print "bout to start"   
        sleep(15)
        prevNow = now
    print "it is time"


def getAllDay(offset, numPics):
    
    # offset = 90 # half the offset is before sunrise, half after
    offsetDelta = datetime.timedelta(minutes = (offset/2))
    print offsetDelta
    sunriseTime = getSunriseTime()
    sunriseHour = int(sunriseTime[0:2])
    sunriseMin = int(sunriseTime[3:5])
    sunsetTime = getSunsetTime()
    sunsetHour = int(sunsetTime[0:2])
    sunsetMin = int(sunsetTime[3:5])
    sunriseDelta = datetime.timedelta(hours = sunriseHour, minutes = sunriseMin)
    print "sunriseDelta = ", sunriseDelta
    sunsetDelta = datetime.timedelta(hours = sunsetHour, minutes = sunsetMin)
    print "sunsetDelta = ", sunsetDelta
    daylight = sunsetDelta - sunriseDelta
    print daylight
    daylightPlus = daylight.seconds + (offset * 60) #daylight plus full offset
    print "daylightPlus = ", daylightPlus
    interval = int(round(daylightPlus/numPics))
    print "interval = ", interval
    targetTime = sunriseDelta - offsetDelta
    print "targetTime =", targetTime
    wait(targetTime)
    msgL1 = "started shooting at " + str(targetTime)
    msgL2 = "sunrise was at " + str(zeroTime)
    msgL12 = msgL1 + "\n" + msgL2
    return(msgL12, interval)


def targetTime(a, b):  # a will be time in advance of the event to start shooting. b 1 for sunrise, 2 for sunset
    ''' this function gets the time of sunrise/set, subtracts the lead up time to 
    calculate the target time, then waits until that time.
    a is the time ahead of sunrise/set
    set b to 1 for sunrise, 2 for sunset
    '''
    oled.clear()
    oled.display0("GETTING START TIME")
    if b == 1:
        oled.display1("getting SUNRISE")
        print "calculating the time %r minutes before SUNRISE" % a
        zeroTime = getSunriseTime() # zero time is the time of the event, either sunset or rise
        oled.display1("sunrise:" + zeroTime)
        msgL2 = "sunrise was at " + str(zeroTime)
    elif b == 2:
        oled.display1("getting SUNSET")
        print "calculating the time %r minutes before SUNSET" % a
        zeroTime = getSunsetTime() 
        oled.display1("sunset:" + zeroTime)
        msgL2 = "sunset was at " + str(zeroTime)
    elif b == 3:
        oled.display1("going in 1")
        print "waiting for next minute"
        d = datetime.datetime.now() + datetime.timedelta(minutes=1)
        d = d.strftime("%H:%M")
        zeroTime = str(d)
        a = 1                                           # set offset to 1
        msgL2 = "started manually"
    
    else:
        print """error, b needs to either be 1 for sunrise or 2 for sunset or 3 for test
        for all day enter 4"""
        oled.display0("ERROR")
    zeroHour = int(zeroTime[0:2])
    zeroMin = int(zeroTime[3:5])
    zeroDelta = datetime.timedelta(hours = zeroHour,minutes = zeroMin)

    

    now = datetime.datetime.now()
    nowDelta = datetime.timedelta(minutes = now.minute, hours = now.hour)
    # print "nowDelta", nowDelta
    # print "now" , now
    offset = datetime.timedelta(minutes = a)
    # print "offset", offset

    targetTime = zeroDelta - offset
    wait(targetTime)

# following commmented out section was replaced by wait()
#     print "targetTime", targetTime
#     secondsTillTarget = (targetTime - nowDelta).seconds
#     # print "secondsTillTarget", secondsTillTarget
#     hoursTillTarget = secondsTillTarget // 3600
#     targetHour = targetTime.seconds // 3600
#     targetMin = ((targetTime.seconds)//60)%60


#     oled.display0("starting at " + str(targetHour) + ":" + str(targetMin))

#     print "waiting for the %rth hour" % targetHour
#     while now.hour != targetHour:
# #        print "waiting for the right hour"
#         now = datetime.datetime.now()
#         nowHour = now.hour
#         nowMin = now.minute
#         oled.display1("now it's " + str(nowHour) + ":" + str(nowMin))
#         sleep(60)
        

#     print "hour matched!"
#     print "waiting for the %rth minute" % targetMin
#     prevNow = now
#     while now.minute != targetMin:
#         now = datetime.datetime.now()
#         nowHour = now.hour
#         nowMin = now.minute

#         if prevNow != now:
#             oled.display1("now it's " + str(nowHour) + ":" + str(nowMin))
#             if now.minute == targetMin:
#                 oled.display1("bout to start")      
#         sleep(15)
#         prevNow = now

    print "it is time"
    msgL1 = "started shooting at " + str(targetTime)
    return msgL1 + "\n" + msgL2
    # end targetTime






if __name__ == '__main__':
    print "yes indeed"
    # today = datetime.datetime.now()
    # print today
    targetTime(1,3)
    # getSunriseTime()
