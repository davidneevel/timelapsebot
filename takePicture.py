# from this tutorial: https://www.youtube.com/watch?v=1eAYxnSU2aw



from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import shutil
from PIL import Image
print "importred takePicture"
import oled
import os



# to kill the process that starts every time the camera turns on
def killgphoto2process():   
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the line that has the process we want to kill
    for line in out.splitlines():
        if 'gvfsd-gphoto2' in line:
            # Kill the process!
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
            print "killed subprocess"


clearCommand = ["--folder", "/store_00020001/DCIM", "-R", "--delete-all-files"]

# previously used the following for delete all, but when the camera moved from folder 100 to 101 it stopped working!
# clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
# Note! at one point this stopped working. The camera would fire but no image would be produced.
#  ran the command "gphoto2 --set-config capturetarget=1" and it works again.
downloadCommand = ["--get-all-files"]



def resizeImages(a,b): # going to resize images from a, save to b
    oled.display0("resizing images")
    print "resizeImages()"
    image_location = a
    resize_location = b
    os.chdir(image_location)
    lst = os.listdir(".")
    lst.sort()
    lstLen = len(lst)
    print lst

    for i in lst:
        oled.display1(str(i))
        # print "gonna resize it"
        img = Image.open(i)
        img = img.crop((603,600,603 + 4058,600 + 2706)) # this is the new line!
        imgResized = img.resize((1080,720))
        resizedName = resize_location + "/" + i
        print "resizing " + resizedName[-7:] + " / " + str(lstLen)
        imgResized.save(resizedName, "JPEG", optimize=True)
    oled.clear()


def captureImages():
    shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "new shot time = %r" % shot_time
    gp(triggerCommand)
    # sleep(1)    # using trigger capture it is necessary to sleep for a bit to allow the camera to save the file internally
    print "doing capture Image"
    return shot_time
    

def takePicture():
    killgphoto2process()
    return captureImages()


def downloadImages():
    oled.display0("downloading images")
    print "downloading"
    gp(downloadCommand)
    gp(clearCommand)
    oled.clear()


def renameFiles(i):
    oled.display0('renaming files')
    image_location = i
    
    print "image_location " + image_location
    # global resize_location
    os.chdir(image_location)  # go to where the images are
    lst = os.listdir(".")
    lst.sort()
    print lst
    a = 1 # the counter for images
    for i in lst:  # for each file in the dir

        if i[-4:] == ".JPG":
            picCount = "%03d" % a  # make the counter 3 decimal places and integrate
            newName = picCount + ".jpg"
            a += 1
            newName = newName.replace(":",".")
            newName = newName.replace(" ","_")
              
            os.rename(i, newName)
            print "Renamed %r to %r" %(i, newName)
              
            # oldLoc = image_location + "/" + newName  
            # newLoc = rename_location + "/" + newName
            
            oled.display1(newName)
    oled.clear()
            
    
def takePictures(n,d):
    shotDelay = d
    print "finna take %r pics" %n
    oled.display0("taking picture")
    totalWait = 0
    adjustedDelay = shotDelay + 0.0
    print "ADJUSTED DELAY = " + str(adjustedDelay)
    for i in range(0, n):
        shotStart = datetime.now()
        oled.display1("    " + str(i + 1) + "/" + str(n))
        print "photo " + str(i)
        
        
        # sleep(shotDelay)
          # initialize variable
        if i > 0:
            t = datetime.now()                                      # this does the timing instead of sleep
            while (t - shotEnd).seconds < adjustedDelay:     # previously shotDelay
                # print (t - shotEnd)
                t = datetime.now()
            
            interval = shotEnd - lastShotStart
            intinterval = interval.seconds + round(float(interval.microseconds)/1000000,3)
            print "interval = " + str(intinterval)
            totalWait += intinterval
            averageInterval = totalWait / i
            print "averageInterval = " + str(averageInterval)
            averageDifference = averageInterval - shotDelay
            adjustedDelay = shotDelay - averageDifference
            print "averageDifference = " + str(averageDifference)
            print "ADJUSTED DELAY = " + str(adjustedDelay)
        

        shot_time = takePicture()
        print "shot_time = " + str(shot_time)      
        lastShotStart = shotStart
        shotEnd = datetime.now()
       
    oled.clear()
    
  

def getPictures(i):
 
    
    os.chdir(i)
    downloadImages()
    gp(clearCommand)
    
    renameFiles(i)
    
    

def makeVid(a,b):
    oled.display0("making Vid")
    imageLocation = a
    shot_date = b
    saveLocation = imageLocation[:-8]   # get out of the ogs folder
    print saveLocation
    movName = saveLocation + "/" + shot_date + '.mp4'
    print "movName = %r" % movName
    imagesToUse = imageLocation + "/" + "%03d" + ".jpg"
    subprocess.call(["ffmpeg", "-f", "image2", "-r", "30", "-i", imagesToUse, \
    "-vcodec", "h264", "-y", movName])
    oled.clear()
    return(movName)

def makeGif(a, b):
    oled.display0("making Gif")
    imageLocation = a
    shot_date = b
    imagesToUse = imageLocation + "/" + "%03d" + ".jpg"
    saveLocation = imageLocation[:-8]   # get out of the resize folder
    gifName = saveLocation + "/" + shot_date + '.gif'
    subprocess.call(["ffmpeg", "-framerate", "10", "-i", imagesToUse, "-vf", "scale=iw/2:-1", gifName])
    oled.clear()    




if __name__ == '__main__':
    print "doing the thing"
    # print "takePicture()"
    # takePicture()
    # print shot_time
    a = '/tlPython/timelapse/images/2018-11-13/2/ogs'
    b = '/tlPython/timelapse/images/2018-11-13/2/resized'
    # resizeImages(a,b)
    makeVid(b,"2018-11-13")
    makeGif(b,"2018-11-13")
