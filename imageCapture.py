from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


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

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = " PiShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/photoZeroPython/timelapse/gphoto/images/" + folder_name

def createSaveFolder():
    try: 
        os.makedirs(save_location)
    except:
        print "Failed to create the new directory, might already exist"
        os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)    # using trigger capture it is necessary to sleep for a bit to allow the camera to save the file internally
    gp(downloadCommand)
    gp (clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                newName = shot_time + ".JPG"
                newName = newName.replace(":",".")
                print newName
                os.rename(filename, newName)
                # os.rename(filename, (shot_time + ID + ".JPG"))  # this was the og version from the tutorial
                print "Renamed the JPG"
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print "Renamed the CR2"


killgphoto2process()
gp(clearCommand)
createSaveFolder()
captureImages()
renameFiles(picID)



