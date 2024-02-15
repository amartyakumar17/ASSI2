import py_compile
import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)

mpDraw = mp.solutions.drawing_utils
#mp_drawing_styles = mp.solutions.drawing_styles
mpHands = mp.solutions.hands
hands = mpHands.Hands()
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read() 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                h , w , c = img.shape
                cx, cy =int(lm.x *w) , int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                
            #print(lmList)
            mpDraw.draw_landmarks(img, handLms ,mpHands.HAND_CONNECTIONS)  

            if lmList:
                x1, y1 = lmList[4][1] , lmList[4][2]
                x2, y2 = lmList[8][1] , lmList[8][2]

                cv2.circle(img, (x1, y1), 10, (2,6,233), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (2,6,233), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (34,16,123),4)

                length = math.hypot((x2-x2), (y2-y1))
                #print(length)

                volRange = volume.GetVolumeRange()
                minVol = volRange[0]
                maxVol = volRange[1]
                vol = 0
                VolBar = 400
                vol = np.interp(length, [50,300], [minVol, maxVol])
                volBar = np.interp(length, [50,300], [400, 150])
                volume.SetMasterVolumeLevel(vol,None)
                if length >=0 :
                    #cv2.circle(img, (cx, cy), 15,(0, 255,0), cv2.Filled)
                   cv2.rectangle(img, (50, 150), (85, 400), (0, 200, 0), 3)
                   cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 200, 0), cv2.FILLED)
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)

