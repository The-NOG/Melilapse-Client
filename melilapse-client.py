#!/usr/bin/env python
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
from astral.geocoder import database, lookup
from astral.sun import sun
import pytz
import cv2


def checkDaytime():
    s = sun(config['ClosestCity'].observer,date=config['dt'])
    if ((s['dawn'] < config['dt']) and (s['dusk'] > config['dt'])):
        return True
    else:
        return False

def checkGoldenHour():
    return False

def remoteUpload():
    return True

def generateName(goldenHour = False):
    """Generates jpg file name for localoutput

    Args:
        goldenHour (bool, optional): Bool of if it's the goldenhour for tagging. Defaults to False.

    Returns:
        str: full path of output file
    """
    dir = config['LocalOutput']
    timestamp = str(datetime.now().timestamp())
    if(goldenHour):
        tag = "*"
    else:
        tag = ""
    file = ".jpg"
    return dir+timestamp+tag+file


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