from dotenv import load_dotenv, dotenv_values
from datetime import datetime
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
        if bool(config['EnableLocal']):
            cv2.imwrite(generateName(),frame)
            #save locally
        if bool(config['EnableRemote']):
            remoteUpload()
    else:
        print('Failed to take picture!')

def validateConfig():
    configValid = True
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