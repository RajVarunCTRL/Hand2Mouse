import cv2
import numpy as np
import pyautogui
from rich.console import Console
import mediapipe as mp

console = Console()
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
draw = mp.solutions.drawing_utils
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=1
)

# Max PROP CAP (WORKS :) )
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    console.print("Error: Couldn't open winCap", style="bold red")
    exit()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frameRBG = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    processed = hands.process(frameRBG)

    landmarks_list = []

    # if processed.multi_hand_landmarks:
    #     hand_landmarks = processed.multi_hand_landmarks[0]
    #     draw.draw_landmarks(frame,hand_landmarks,mpHands.HAND_CONNECTIONS)
    #
    #     for lm in hand_landmarks.landmark:
    #         landmarks_list.append((lm.x, lm.y))
    #
    #     print(landmarks_list)



# Optimzed for the above code
    if processed.multi_hand_landmarks:
        for hand_landmarks in processed.multi_hand_landmarks:
            draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

            #Extarct coords
            for lm in hand_landmarks.landmark:
                # testing
                # print("lm.x:", lm.x)
                # print("lm.y:", lm.y)
                # x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0]) # For Pixel Precision
                landmarks_list.append((lm.x, lm.y))
                print(lm.x, lm.y)


    cv2.imshow("CamWin", frame)

    # Implement Media Pipe for hand gestures

    # Fail Safe Mechanism 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        console.print("Fail-Safe init", style="bold red blink")
        break
    # Fail Safe Mechanism
    screen_width, screen_heigh = pyautogui.size()
    cursor_x, cursor_y = pyautogui.position()
    if cursor_x >= screen_width - 1 and cursor_y <= 1:
        console.print("Fail-Safe init!", style="bold red blink")
        break

cap.release()
cv2.destroyAllWindows()
