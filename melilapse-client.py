from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import cv2


def CheckDaytime():
    return True

def CheckNighttime():
    return False

def remoteUpload():
    return True

def takePicture():
    cap = cv2.VideoCapture(int(config['CameraID']))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(config['FrameWidth']))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config['FrameHeight']))
    r, frame = cap.read()
    if r:
        if True:
            cv2.imwrite(str(datetime.now().timestamp())+".jpg",frame)
            #save locally
        if False:
            pass #Save Remotely

def main():
    print("Starting Melilapse")
    takePicture()
    print("Ending Melilapse")

load_dotenv()
config = dotenv_values(".env")
if __name__ == "__main__":
    main()