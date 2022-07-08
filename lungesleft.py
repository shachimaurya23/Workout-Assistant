import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm



cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"


while cap.isOpened():
    ret, img = cap.read()
    #Determine dimensions of video
    width  = cap.get(3)  
    height = cap.get(4)  
 
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        l_knee = detector.findAngle(img, 23,25,27)
        l_ankle = detector.findAngle(img, 25,27,31)
        l_hip = detector.findAngle(img, 11, 23,25)
        
        #Percentage of success of lunges
        per = np.interp(l_knee, (90, 160), (0, 100))
        
        #Bar to show lunges progress
        bar = np.interp(l_knee, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if l_knee > 160 and l_ankle > 40 and l_hip > 160:
            form = 1
    
        #Check for full range of motion for the lunges
        if form == 1:
            if per == 0:
                if l_knee <= 100 and l_hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if l_knee > 160 and l_ankle > 40 and l_hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                       
                
                    
    
        print(count)
        
        #Draw Bar
        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)


        #lunges counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

        
    cv2.imshow('lunges counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    
        
cap.release()
cv2.destroyAllWindows()