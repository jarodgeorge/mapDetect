import os
import numpy as np
import pyautogui
import imutils
import cv2
from twilio.rest import Client
import time
os.environ['DISPLAY'] = ':0'

# set twilio sid and auth token in your environment variables
def textMe():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body="Item found!",
                     from_=os.environ['TWILIO_PHONE_NUMBER'],
                     to=os.environ['MY_PHONE_NUMBER']
                 )

    print(message.sid)
    
def takeScreenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("images/recent.png", image)
    # show image for debug
    # image = cv2.imread("straight_to_disk.png")
    # cv2.imshow("Screenshot", imutils.resize(image, width=600))
    # cv2.waitKey(0)
    
def parseColors(texts):
    #BRG
    boundaries = ([4,175,205],[12,185,230])
    def mouseRGB(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
            colorsB = image[y,x,0]
            colorsG = image[y,x,1]
            colorsR = image[y,x,2]
            colors = image[y,x]
            print("Red: ",colorsR)
            print("Green: ",colorsG)
            print("Blue: ",colorsB)
            print("BRG Format: ",colors)
            print("Coordinates of pixel: X: ",x,"Y: ",y)    

    image = cv2.imread("images/recent.png")
    image = image[46:228,1729:1914]
    lower = np.array(boundaries[0],dtype = "uint8")
    upper = np.array(boundaries[1],dtype = "uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    yellowPixels = np.count_nonzero(output)
    overlay = np.hstack([image, output])
    imutils.resize(overlay, width=1920)
    print("Pixel Count", yellowPixels)
    if(yellowPixels>=6):
        cv2.imwrite("images/positive.png", overlay)
        print(True)
        textMe()
        texts[0]+=1
        time.sleep(180)

    else:
        print(False)

    # debug for testing rgb values
    # cv2.namedWindow('mouseRGB')
    # cv2.setMouseCallback('mouseRGB',mouseRGB)
    # while(1):
    #     cv2.imshow("mouseRGB",overlay)
    #     if cv2.waitKey(20) & 0xFF == 27:
    #         break
    # cv2.destroyAllWindows()



if __name__ == '__main__':
    
    texts = [0]

    while(1):
        takeScreenshot()
        parseColors(texts)
        # circuit breaker if left running 
        if texts[0]>=10:
            text[0] = 0
            time.sleep(300)
            break
        time.sleep(1)



