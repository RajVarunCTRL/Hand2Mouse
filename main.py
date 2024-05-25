import cv2
import numpy as np
import pyautogui
from rich.console import Console
import mediapipe as mp


console = Console()
cap = cv2.VideoCapture(0)

# Testing Zone
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    console.print("Error: Couldn't open winCap", style="bold red")
    exit()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 2)

    # Region to capture

    roc = frame[100:500, 100:500]
    #                                            (R,G,B)
    cv2.rectangle(frame, (100, 100), (500, 500), (0, 255, 0), 2)

    cv2.imshow("CamWin", frame)

    # ROC pre processing

    # grayscaling = cv2.cvtColor(roc, cv2.COLOR_BGR2GRAY)
    # gau = cv2.GaussianBlur(grayscaling, (5, 5), 0)
    #
    # _, thresh = cv2.threshold(gau, 60, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Thresholded", thresh)

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
