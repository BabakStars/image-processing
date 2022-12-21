import cv2
import numpy as npp
import mediapipe as mp
import pyfirmata
import time

arduino = pyfirmata.Arduino("COM12")

light1 = arduino.get_pin("d:8:o")
light2 = arduino.get_pin("d:9:o")
light3 = arduino.get_pin("d:10:o")

time.sleep(2.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(
                    image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        finger = []
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                finger.append(1)
            else:
                finger.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    finger.append(1)
                else:
                    finger.append(0)
            finger_counter = finger.count(1)
            if finger_counter == 0:
                light1.write(1)
                light2.write(1)
                light3.write(1)
            elif finger_counter == 1:
                light1.write(1)
                light2.write(0)
                light3.write(1)
            elif finger_counter == 2:
                light1.write(0)
                light2.write(0)
                light3.write(1)
            elif finger_counter == 3:
                light1.write(0)
                light2.write(0)
                light3.write(0)

        cv2.imshow("result", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

cap.release()
cv2.cv2.destroyAllWindows()
