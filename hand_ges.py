import cv2
import mediapipe as mp
import math

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))

def main():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    my_hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    compareIndex = [[5, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
    gesture = [[True, True, True, True, True, "Hello"],
               [False, False, False, False, False, "nope"],
               [False, True, True, False, False, "yeah"]]

    while True:
        ret, img = cap.read()

        if not ret:
            print("fail to connect")
        else:
            height, width, channel = img.shape
            before = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            after = my_hands.process(before)

            if after.multi_hand_landmarks:
                for hand_landmarks in after.multi_hand_landmarks:
                    hands_open = [False] * 5  
                    for i in range(0, 5):
                        hands_open[i] = (dist(hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,
                                              hand_landmarks.landmark[compareIndex[i][0]].x,
                                              hand_landmarks.landmark[compareIndex[i][0]].y) <
                                         dist(hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,
                                              hand_landmarks.landmark[compareIndex[i][1]].x,
                                              hand_landmarks.landmark[compareIndex[i][1]].y))

                    for g in gesture:
                        if all(a == b for a, b in zip(g[:5], hands_open)): 
                            print(g[5])
                            break 

                    mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

        cv2.imshow("mediapipe", img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
