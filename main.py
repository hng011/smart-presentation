import cv2
import pyautogui
from feature_modules.HandDetector import *
from feature_modules.ListOpenedFingers import *

def main():
    cap=cv2.VideoCapture(0)
    WIDTH_CAM,HEIGHT_CAM=920, 640
    cap.set(3, WIDTH_CAM)
    cap.set(4, HEIGHT_CAM)

    DELAY=15
    status_delay=False
    delay_counter=0

    while cap.isOpened():
        success, frame=cap.read()
        
        frame_flipped=cv2.flip(frame, 1)
        landmark_list, detector, wrist_position, hand_side=detect_hand(image=frame_flipped, draw_landmarks=True)
        list_point=list_opened_fingers(landmark_list=landmark_list, subtractor=2, hand_side=hand_side)
        
        if wrist_position and status_delay==False:
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