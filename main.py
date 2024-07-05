import cv2
import cvzone
import pickle
import numpy as np

cap=cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
        posList=pickle.load(f)

width,height= 107,48
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))


def checkParkingSpace(imgPro):
    spaceCounter=0
    for pos in posList:
        x,y=pos

        imgCrop=imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)
        count=cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-5), scale=1.5, thickness=2, offset=0,colorR=(0,0,255))

        if count<800:
            color=(0,255,0)
            thickness=5
            spaceCounter+=1
            cvzone.putTextRect(img,str(count),(x,y+height-5), scale=1.5, thickness=2, offset=0,colorR=color)

        else:
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)
    cvzone.putTextRect(img,f'Free: {spaceCounter} of {len(posList)}',(100,50), scale=3, thickness=5, offset=20,colorR=(0,205,0))



while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success,img=cap.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgThrushold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,21,16)
    imgMedian=cv2.medianBlur(imgThrushold,5)
    kernel=np.ones((3,3),np.uint8)
    imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)
    checkParkingSpace(imgDilate)
    out.write(img)
    cv2.imshow("Image",img)
    # cv2.imwrite("OutputVideo.mp4",img)
    cv2.waitKey(10)

