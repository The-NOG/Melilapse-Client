from dotenv import load_dotenv, dotenv_values
from datetime import datetime
from astral.geocoder import database, lookup
import cv2


def checkDaytime():
    return True

def checkNighttime():
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
    cap = cv2.VideoCapture(int(config['CameraID']))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(config['FrameWidth']))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config['FrameHeight']))
    print('Taking Picture')
    r, frame = cap.read()
    if r:
        if config['EnableLocal']:
            cv2.imwrite(generateName(),frame)
            #save locally
        if config['EnableRemote']:
            remoteUpload()
    else:
        print('Failed to take picture!')

def validateConfig():
    configValid = True
    #validate Location
    try:
        configCity = lookup(config["Charleston"], database())
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
    if(validateConfig()):
        print("Config appears Valid")
        takePicture()
    else:
        print("Invalid Config")
    print("Ending Melilapse")

load_dotenv()
config = dotenv_values(".env")
if __name__ == "__main__":
    main()