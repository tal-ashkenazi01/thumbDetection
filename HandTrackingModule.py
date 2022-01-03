import cv2
import mediapipe as mp
import time


# Create a class for the functions and values
class handDetector():
    # The parameters passed to the constructor are the basic parameters required for the hand (from the model itself)
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initializing the same code to initialize and draw the hand landmarks and coordinates
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils

    # The class method that finds the hands and by default will draw the hands onto the screen
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)

        return img

    # The function involved with returning the coordinates of the hand landmarks
    def findPosition(self, img, handNo=0, draw=True):

        # The list of coordinates that will be returned when the function exits
        landmarkList = []
        # Check for multiple hands
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                height, width, channels = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                landmarkList.append([id, cx, cy])

        return landmarkList


# Whatever is written here is essentially what the module can do when it is run on its own, not through other code
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        print(lmList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
