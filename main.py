import cv2
import numpy as np
import pyautogui
from rich.console import Console

console = Console()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Region to capture
    roc = frame[100:300, 100:300]
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)

    # Fail Safe Mechanism
    screen_width, screen_heigh = pyautogui.size()
    cursor_x, cursor_y = pyautogui.position()
    if cursor_x >= screen_width - 1 and cursor_y <= 1:
        console.print("Fail Safe initiated!", style="bold red blink")
        break


cap.release()
cv2.destroyAllWindows()
