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

def generateName(goldenhour = False):
    dir = config['LocalOutput']
    timestamp = str(datetime.now().timestamp())
    if(goldenhour):
        tag = "*"
    else:
        tag = ""
    file = ".jpg"
    return dir+timestamp+tag+file


def takePicture():
    cap = cv2.VideoCapture(int(config['CameraID']))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(config['FrameWidth']))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config['FrameHeight']))
    r, frame = cap.read()
    if r:
        if bool(config['EnableLocal']):
            cv2.imwrite(generateName(),frame)
            #save locally
        if bool(config['EnableRemote']):
            remoteUpload()

def main():
    print("Starting Melilapse")
    takePicture()
    print("Ending Melilapse")

load_dotenv()
config = dotenv_values(".env")
if __name__ == "__main__":
    main()