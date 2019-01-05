mode = 2 # 1 is sunrise, 2 is sunset, 3 is in one min

import takePicture as tp
import makeVid as mv
import makeVid
from time import sleep
from datetime import datetime
import os
import oled
import sunset
import twitter

numPics = 300
# note can't upload a video with less than ~15 frames to twitter
shotDelay = 7 # time between shots in sec
sunriseLeadTime = 20
sunsetLeadTime = 10
allDayLeadTime = 10 # this amount before sunrise and after sunset.
if mode == 1:
    leadTime = sunriseLeadTime
if mode == 2: 
    leadTime = sunsetLeadTime
if mode == 4: 
    leadTime = allDayLeadTime




    
def makeFolders():
    try:
        os.makedirs(date_folder)
        print "made folder %r" % date_folder
        
    except:
        print "Failed to create the new save folder, might already exist"
        os.chdir(date_folder)

    global folderNumber
    os.chdir(date_folder)
    numFolders = len(os.listdir("."))  # count how many folders already exist
    folderNumber = str(numFolders + 1) # up the count by one
    os.mkdir(folderNumber)              # and make the folder
   
    global image_location
    image_location = date_folder + "/" + folderNumber + "/ogs"
    print "image location = " + image_location
    print "made folder number %r" % folderNumber
    global resize_location
    resize_location = date_folder + "/" + folderNumber + "/resized"
    rename_location = date_folder + "/" + folderNumber + "/renamed"
    os.mkdir(rename_location)
    os.mkdir(resize_location)
    os.mkdir(image_location)


def now():
    n = datetime.now().strftime("%H:%M")
    return n


if mode < 4:
    msg12 = sunset.targetTime(leadTime, mode) # this returns the first two lines of msg
if mode == 4:
    allDayRet = sunset.getAllDay(leadTime, numPics)
    msg12 = allDayRet[0]
    shotDelay = allDayRet[1]

# moved the following to after the targetTime so the folders will have the correct date if i start it the night before
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_folder = "/tlPython/timelapse/images/" + shot_date

makeFolders()
endTime = tp.takePictures(numPics, shotDelay)
tp.getPictures(image_location)
msgL3 = "stopped shooting at " + now()
tp.resizeImages(image_location, resize_location) # resize from a to b
movName = tp.makeVid(resize_location, shot_date) # where to find source images
tp.makeGif(resize_location, shot_date)
print "movName = " + str(movName)

msgL4 = "processing finished  " + now()

msg = msg12 + "\n" + msgL3 + "\n" + msgL4 + "\n" + str(numPics) + " pictures taken"

twitter.tweet(msg, movName)

# os.chdir(date_folder)
os.chdir(date_folder + "/" + folderNumber)
f = open("stats.txt", "w+")
f.write(msg)
f.close()

oled.clear()

