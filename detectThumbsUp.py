import cv2
import pynput.keyboard
from pynput import keyboard
from HandTrackingModule import handDetector
import math

# INITIALIZE THE IMAGE CAPTURE FOR THE CAMERA
cap = cv2.VideoCapture(0)

# CREATE A HAND DETECTOR THAT WILL TRACK USER HANDS
hand_tracker = handDetector()


# CALLBACK FUNCTION FOR THE EVENT LISTENER
def on_press(key):
    try:
        if key == keyboard.Key.space or key == keyboard.Key.esc:
            cap.release()
            cv2.destroyAllWindows()
        else:
            return
    except:
        print("there was an error")


# CREATE AND START EVENT LISTENER
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()

# WHILE THE PROGRAM IS RUNNING, CONTINUOUSLY READ THE IMAGE
while True:

    # CAPTURE CONTENT FROM THE CAMERA INTO IMAGES
    success, image_capture = cap.read()

    try:
        # SCAN FOR THE HANDS IN THE IMAGE
        image_capture = hand_tracker.findHands(image_capture)
        finger_positions = hand_tracker.findPosition(image_capture)

        # CHECK TO SEE IF FINGERS ARE DETECTED
        try:
            # LOG FINGER DATA
            print(f"Thumb: {finger_positions[4]}\nPointer:{finger_positions[8]}")

            # FIND THUMB AND POINTER FINGER TIP POSITIONS
            pointer_pos = finger_positions[8]
            thumb_pos = finger_positions[4]

            # FIND IF THE OTHER FINGERS ARE BALLED INTO A FIST AND MAKE FLAG
            fist_flag = (math.dist(finger_positions[16][1:], finger_positions[20][1:]) < 90 and math.dist(
                finger_positions[16][1:], finger_positions[12][1:]) < 90 and math.dist(finger_positions[8][1:],
                                                                                       finger_positions[12][1:]))

            # IF THUMB IS LOWER THAN THE POINTER, THUMBS DOWN
            if thumb_pos[2] > pointer_pos[2] and (thumb_pos[2] - pointer_pos[2]) > 100 and fist_flag:
                cv2.putText(image_capture, "Thumbs down!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

            # IF THUMB IS HIGHER THAN THE POINTER, THUMBS UP
            elif thumb_pos[2] < pointer_pos[2] and (pointer_pos[2] - thumb_pos[2]) > 100 and fist_flag:
                cv2.putText(image_capture, "Thumbs up!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

        except IndexError:
            print("No fingers detected")

        # SHOW THE CAMERA INPUT
        cv2.imshow('Camera Input', image_capture)
        cv2.waitKey(1)

    # IF THE IMAGE IS DESTROYED DURING ITERATION, CAPTURE THE ERROR
    except cv2.error:
        break

# STOP THE LISTENER AFTER RUNNING
listener.stop()
print("Listener stopped")
