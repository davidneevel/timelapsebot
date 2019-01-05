import subprocess
import os

'''
gittest
this is the script that works in the command line to make a video of a series of images

ffmpeg -f image2 -r 30 -i image%01d.png -vcodec mpeg4 -y movie.mp4

nb the "image%01d.png" bit means it will use images with names beginning with "image"
followed by a number 01 digits long. Change image and 01 accordingly 

'''



def makevid(loc,date):
    os.chdir(loc)
    # rawMovName = loc + "/" + date + 'raw.mp4'
    saveLocation = loc[:-7]   # get out of the resize folder
    movName = saveLocation + "/" + date + '.mp4'
    print "movName = %r" % movName
    imagesToUse = loc + "/" + date + "_" + "%03d" + ".JPG"
    subprocess.call(["ffmpeg", "-f", "image2", "-r", "30", "-i", imagesToUse, \
    "-vcodec", "mpeg4", "-y", movName])
    # subprocess.call(["MP4Box", "-fps", "24", "-add", "movie2.mp4", movName]) # re-wraps video into something playable (commented out because it doesn't seem to be necessary)



def makeGif(loc,date):

 

    imagesToUse = loc + "/" + date + "_" + "%03d" + ".JPG"
    saveLocation = loc[:-7]   # get out of the resize folder
    gifName = saveLocation + "/" + date + '.gif'
    subprocess.call(["ffmpeg", "-framerate", "2", "-i", imagesToUse, "-vf", "scale=iw/2:-1", gifName])
    
    



if __name__ == '__main__':
    makevid()
    

