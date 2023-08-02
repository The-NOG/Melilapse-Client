#!/usr/bin/env python
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
from astral.geocoder import database, lookup
from astral.sun import sun
import pytz
import cv2

def testScratchFile(file:str) -> bool:
    if(readScratchFile(file) == -1):
        return writeScratchFile(file,0)
    else:
        return True

def readScratchFile(file:str) -> int:
    try:
        with open(file) as f:
            content = f.read().splitlines()
        return int(content[0])
    except Exception as e:
        return -1

def writeScratchFile(file:str,iter:int =0) -> bool:
    try:
        with open(file,"w+") as f:
            f.write(str(iter))
        return True
    except Exception as e:
        return False
    

def checkDaytime():
    s = sun(config['ClosestCity'].observer,date=config['dt'])
    if ((s['dawn'] < config['dt']) and (s['dusk'] > config['dt'])):
        return True
    else:
        return False

def remoteUpload():
    return True

def generateName():
    """Generates jpg file name for localoutput

    Returns:
        str: full path of output file
    """
    dir = config['LocalOutput']
    file = ".jpg"
    if(config['FileNameType'] == "timestamp"):
        timestamp = str(datetime.now().timestamp())
        return dir+timestamp+file
    elif(config['FileNameType'] == 'iteration'):
        iter = readScratchFile(config['ScratchFile'])
        filename = dir
        if(config['IncludeCameraName']):
            filename = filename + config['CameraName'] + "-"
        if (config['IncludeDate']):
            now = datetime.now()
            filename = filename + now.strftime("%d%m%Y") + "-"
        filename = filename + str(iter) + file
        writeScratchFile(config['ScratchFile'],iter+1)
        return filename


def takePicture():
    """Takes a picture
    """
    frameNumber = 0
    cap = cv2.VideoCapture(int(config['CameraID']))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(config['FrameWidth']))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config['FrameHeight']))
    print('Taking Picture')
    while True:
        r, frame = cap.read()
        if r:
            if(frameNumber == 15):
                if config['EnableLocal']:
                    cv2.imwrite(generateName(),frame)
                    #save locally
                if config['EnableRemote']:
                    remoteUpload()
                cap.release()
                break
        else:
            print('Failed to take picture!')
            cap.release()
            break
        frameNumber = frameNumber + 1

def validateConfig():
    configValid = True
    #Basic Config
    if config['Enabled'] == 'True':
        config['Enabled'] = True
    elif config['Enabled'] == 'False':
        config['Enabled'] = False
    else:
        print("Enabled appears invalid")
        return False
    #validate Location
    try:
        configCity = lookup(config["ClosestCity"], database())
        config["ClosestCity"] = configCity
        config["tz"] = pytz.timezone(configCity.timezone)
        config['dt'] = datetime.now(config['tz'])
    except KeyError as e:
        print("City not recognized")
        return False
    #validate Camera Settings
    try:
        int(config['CameraID'])
    except ValueError as identifier:
        print('CameraID is Invalid')
        return False
    #validate Timelapse Settings

    #Validate Local Output settings
    if config['EnableLocal'] == 'True':
        config['EnableLocal'] = True
    elif config['EnableLocal'] == 'False':
        config['EnableLocal'] = False
    else:
        print("EnableLocal is invalid")
        return False
    #Validate Remote Output Settings
    if config['EnableRemote'] == 'True':
        config['EnableRemote'] = True
    elif config['EnableRemote'] == 'False':
        config['EnableRemote'] = False
    else:
        print("EnableRemote is invalid")
        return False
    if config["camername"]:
        pass
    else:
        print("Missing Camera name")
        return False
    if config['FileNameType'] not in ["iteration","timestamp"]:
        print("Invalid Filename Type")
        return False
    if config['FileNameType'] == 'iteration':
        if (testScratchFile(config['ScratchFile']) == False):
            print("Scratch file failure")
            return False
        if config["IncludeCameraName"] == 'True':
            config["IncludeCameraName"] = True
        elif config["IncludeCameraName"] == 'False':
            config["IncludeCameraName"] = False
        else:
            print("IncludeCameraName is invalid")
            return False
        if config['IncludeDate'] == 'True':
            config['IncludeDate'] = True
        elif config['IncludeDate'] =='False':
            config['IncludeDate'] = False
        else:
            print('IncludeDate is invalid')
            return False
    return configValid

def main():
    """What is life
    """
    print("Starting Melilapse")
    print("Validating Config")
    #test and parse config.
    if(validateConfig()):
        print("Config appears Valid")
        #Check if the config has enabled melilapse client
        if(config['Enabled']):
            #TODO: Use config to check when pictures should be taken
            if(checkDaytime()):
                print("Suns out, shots out!")
                #Take the damn picture and output where needed
                takePicture()
            else:
                #TODO: Update this when ^ TODO is done
                print("No pictures at night")
        else:
            print("Melilapse is disabled!")
    else:
        #do nothing if config invalid
        print("Invalid Config")
    print("Ending Melilapse")

load_dotenv()
config = dotenv_values(".env")
if __name__ == "__main__":
    main()