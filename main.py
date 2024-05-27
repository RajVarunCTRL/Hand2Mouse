import cv2
import pyautogui
from pynput.mouse import Button, Controller
from rich.console import Console
import mediapipe as mp
import util

# Getting the screen width and height. Global.
screen_width, screen_height = pyautogui.size()


def findFingerTip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]

    return None


def moveMouse(indexFingerTip):
    if indexFingerTip is not None:
        x = int(indexFingerTip.x * screen_width)
        y = int(indexFingerTip.y * screen_height)
        pyautogui.moveTo(x, y)


# Detecting Gestures

# Check for leftclick fucntion.
def isLeftClick(landmark_list, thumbIndexDist):
    return util.angleGet(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 < thumbIndexDist and util.angleGet(
        landmark_list[9], landmark_list[10], landmark_list[12]) < 90


# Cehck for rightclick function.
def isRightClick(landmark_list, thumbIndexDist):
    return util.angleGet(landmark_list[9], landmark_list[10],
                         landmark_list[12]) < 50 < thumbIndexDist and util.angleGet(
        landmark_list[5], landmark_list[6], landmark_list[8]) > 90


def isDoubleClick(landmark_list, thumbIndexDist):
    return util.angleGet(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 < thumbIndexDist and util.angleGet(
        landmark_list[9], landmark_list[10], landmark_list[12]) > 50


def detectGestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        # test
        indexFingerTip = findFingerTip(processed)
        thumbIndexDist = util.getDistance([landmarks_list[4], landmarks_list[5]])

        # Mouse ( needs to be optimized )

        if thumbIndexDist < 50 and util.angleGet(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            moveMouse(indexFingerTip)

        # Left Clickedey
        elif isLeftClick(landmarks_list, thumbIndexDist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "LMB", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 255, 0), 5)

        elif isDoubleClick(landmarks_list, thumbIndexDist):
            pyautogui.doubleClick()
            cv2.putText(frame, "DBDB", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 0, 0), 5)
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "RMB", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 0, 0), 5)


console = Console()
cap = cv2.VideoCapture(0)
mouse = Controller()

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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # Frame Size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)  # Frame size

actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f'Actual frame size: {actual_width}x{actual_height}')  # This depends on the MP of your camera...

if not cap.isOpened():
    console.print("Error: Couldn't open winCap", style="bold red")
    exit()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frameRBG = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    processed = hands.process(frameRBG)

    landmarks_list = []

    # Optimized Code.
    if processed.multi_hand_landmarks:
        for hand_landmarks in processed.multi_hand_landmarks:
            draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

            # Extract coords
            for lm in hand_landmarks.landmark:
                # testing
                # print("lm.x:", lm.x)
                # print("lm.y:", lm.y)
                # x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0]) # For Pixel Precision
                landmarks_list.append((lm.x, lm.y))
                # print(lm.x, lm.y) # Prints all the coords of the landmarks

    # Show image.
    cv2.imshow("CamWin", frame)

    # Implement Media Pipe for hand gestures
    detectGestures(frame, landmarks_list, processed)

    # Fail Safe Mechanism 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        console.print("Fail-Safe init", style="bold red blink")
        break
    # Fail Safe Mechanism
    cursor_x, cursor_y = pyautogui.position()
    if cursor_x >= screen_width - 1 and cursor_y <= 1:
        console.print("Fail-Safe init!", style="bold red blink")
        break

cap.release()
cv2.destroyAllWindows()
