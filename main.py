import cv2
import numpy as np
import pyautogui
from rich.console import Console

console = Console()
cap = cv2.VideoCapture(0)

# Testing Zone


if not cap.isOpened():
    console.print("Error: Couldn't open winCap", style="bold red")
    exit()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Region to capture

    roc = frame[100:300, 100:300]
    #                                            (R,G,B)
    cv2.rectangle(frame, (100, 100), (300, 300), (255, 0, 0), 2)

    cv2.imshow("CamWin", frame)


    # Fail Safe Mechanism 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Fail Safe Mechanism
    screen_width, screen_heigh = pyautogui.size()
    cursor_x, cursor_y = pyautogui.position()
    if cursor_x >= screen_width - 1 and cursor_y <= 1:
        console.print("Fail Safe initiated!", style="bold red blink")
        break


cap.release()
cv2.destroyAllWindows()
