import cv2
import pyautogui
import win32gui
from feature_modules.HandDetector import *
from feature_modules.ListOpenedFingers import *

def main():
    WINDOW_NAME="webcam"; cap=cv2.VideoCapture(0)
    WIDTH_CAM,HEIGHT_CAM=350, 250
    cap.set(3, WIDTH_CAM); cap.set(4, HEIGHT_CAM)

    DELAY=20; status_delay=False
    delay_counter=0; btn_log=None
    G_THRESHOLD=(HEIGHT_CAM//2)+30
    
    while cap.isOpened():
        success, frame=cap.read()
      
        cv2.line(frame, (0, G_THRESHOLD), 
                 (WIDTH_CAM, G_THRESHOLD), 
                 (0,0,255), 6)
        
        frame_flipped=cv2.flip(frame, 1)
        landmark_list, detector, wrist_position, hand_side=detect_hand(image=frame_flipped, 
                                                                       draw_landmarks=True)
        list_point=list_opened_fingers(landmark_list=landmark_list, 
                                       subtractor=2, 
                                       hand_side=hand_side)
        print(list_point)
        print(hand_side)
        if (wrist_position and status_delay==False) and wrist_position[1] < G_THRESHOLD:
            btn_log="None"
            if list_point == [0,0,1,1,1]:
                status_delay=True
                btn_log = "RIGHT BUTTON CLICKED ->" 
                print(btn_log)
                pyautogui.press("right")
            
            if list_point == [1,1,1,0,0]:
                status_delay=True
                btn_log = "LEFT BUTTON CLICKED <-" 
                print(btn_log)
                pyautogui.press("left")
        
        if status_delay:
            delay_counter += 1 
        if delay_counter==DELAY:
            delay_counter=0
            status_delay=False

        fs_wnd=win32gui.GetWindowText(win32gui.GetForegroundWindow())
        fs_wnd=fs_wnd.replace(" ", "").split("-")[-1]
        cv2.putText(detector, 
                    f"current window: {fs_wnd}", 
                    (5, HEIGHT_CAM), 
                    cv2.FONT_HERSHEY_PLAIN, 1, 
                    (0,255,0), 2)
        
        print("curr window: ",fs_wnd)
        cv2.putText(detector, 
                    f"log: {btn_log}", 
                    (5, HEIGHT_CAM+20), 
                    cv2.FONT_HERSHEY_PLAIN, 1, 
                    (0,255,0), 2)
        cv2.imshow(WINDOW_NAME, detector)
        
        # Window stick on top
        cv2.setWindowProperty(WINDOW_NAME, 
                              cv2.WND_PROP_TOPMOST, 1)

        if cv2.waitKey(1)==ord("q") or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1: 
            cap.release()
            cv2.destroyAllWindows()
            break ## pressing q for exit
    
if __name__=="__main__":
    main()
    