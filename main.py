import cv2
import numpy as np
import pyautogui
import mediapipe as mp
import re

# INITIALIZATION
mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands( # Instantiating
    max_num_hands=1,
    min_detection_confidence=0.8
)


def detect_hand(image: np.ndarray=None, draw_landmarks: bool=False, show_score: bool=False) -> tuple:
    h, w, _=image.shape
    res=hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    multi_hl=res.multi_hand_landmarks
    multi_hn=res.multi_handedness
    position=[]
    wrist_position=()
    hand_side=None

    if multi_hl:
        for data in multi_hn:
            hand_side=data.classification[0].label
            cfd_score=data.classification[0].score
        for hand_marks in multi_hl:
            for i, lm in enumerate(hand_marks.landmark):
                index, cx, cy=i, int(lm.x*w), int(lm.y*h) # Converting from ratio to pixel?

                position.append([index, cx, cy])
                if draw_landmarks:
                    cv2.rectangle(image, (cx, cy), (cx+10, cy+15), (255,0,255), 25)
                    mp_draw.draw_landmarks(image, hand_marks, mp_hands.HAND_CONNECTIONS) # Draw landmarks on frame
                    
                if i==0: #Detecting wrist
                    wrist_position = (cx, cy)
                    cv2.putText(image, 
                                f"{hand_side} hand", 
                                (cx-50, cy+50), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
                    # Confident score display
                    cv2.putText(image, 
                                f"{cfd_score:.2f}%", 
                                (cx-25, cy+90), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
                                            
        if show_score:
            print(f"{hand_side} hand detected | score {cfd_score}")
    else:
        print("No Hand Detected")
    
    return position, image, wrist_position, hand_side


def list_fingers_open(landmark_list: list, subtractor: int=2, hand_side: str=None) -> list:
    list_fingers_open=[]
    finger_points=[4,8,12,16,20]

    if landmark_list:
        for point in finger_points:
            if point == 4:
                if re.search(r".*[Rr]ight.*", str(hand_side)):
                    # landmark_list[point][1] -> width | landmark_list[point][2] -> height 
                    list_fingers_open.append(1 if landmark_list[point][1] < landmark_list[point-subtractor+1][1] else 0)
                else:
                    list_fingers_open.append(1 if landmark_list[point][1] > landmark_list[point-subtractor+1][1] else 0)
            else:
                list_fingers_open.append(1 if landmark_list[point][2] < landmark_list[point-subtractor][2] else 0)

    return list_fingers_open


def main():
    cap=cv2.VideoCapture(0)
    WIDTH_CAM,HEIGHT_CAM=920, 640
    cap.set(3, WIDTH_CAM)
    cap.set(4, HEIGHT_CAM)
    # cap.set(10, 100) # Brightness
    
    GESTURE_TRESHOLD=400
    DELAY=15
    status_delay=False
    delay_counter=0

    while cap.isOpened():
        success, frame=cap.read()
        
        # Line Threshold
        cv2.line(frame, (0, GESTURE_TRESHOLD), (WIDTH_CAM, GESTURE_TRESHOLD), (255,0,0), 3)
        frame_flipped=cv2.flip(frame, 1)
        landmark_list, detector, wrist_position, hand_side=detect_hand(image=frame_flipped, draw_landmarks=True)
        list_point=list_fingers_open(landmark_list=landmark_list, subtractor=2, hand_side=hand_side)
        
        if wrist_position and status_delay==False and wrist_position[1] < GESTURE_TRESHOLD:
            print(list_point)
            status_delay=True
            if list_point == [0,0,1,1,1]:
                print("|||>> Last three fingers opened | RIGHT BUTTON PRESSED")
                pyautogui.press("right")
            
            if list_point == [1,1,1,0,0]:
                print("|||>> First three fingers opened | LEFT BUTTON PRESSED")
                pyautogui.press("left")
        
        if status_delay:
            delay_counter += 1 
        if delay_counter==DELAY:
            delay_counter=0
            status_delay=False

        cv2.imshow("webcam", detector)

        if cv2.waitKey(1)==ord("q"): break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()