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
    ret, img = cap.read() #640 x 480
    #Determine dimensions of video 
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        l_elbow = detector.findAngle(img, 11, 13, 15)
        l_shoulder = detector.findAngle(img, 13, 11, 23)
        l_wrist = detector.findAngle(img, 19,15,13)

        
        #Percentage of success of BicepCurl
        per = np.interp(l_elbow, (90, 160), (0, 100))
        
        #Bar to show bicepCurl progress
        bar = np.interp(l_elbow, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if l_elbow >20 and l_shoulder > 60 and l_wrist > 100:
            form = 1
    
        #Check for full range of motion for the bicepCurl
        if form == 1:
            if per == 0:
                if l_elbow <= 120 and l_wrist >100 and l_shoulder >60:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if l_elbow >15 and l_shoulder > 40 and l_wrist > 100:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0
                
                    
    
        print(count)
        
        #Draw Bar
        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)


        #bicepCurl counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

        
    cv2.imshow('Bicep Curl counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    k = cv2.waitKey(30) & 0xff  # Esc for quiting the app
    if k==27:
            break
    elif k==ord('r'):       # Reset the counter on pressing 'r' on the Keyboard
            left_counter = 0
            right_counter = 0

        
cap.release()
cv2.destroyAllWindows()