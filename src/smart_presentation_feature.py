import cv2
import pyautogui
from feature_modules.HandDetector import *
from feature_modules.ListOpenedFingers import *

class Camera:
    def __init__(self, name: str="webcam",
                 box_size: tuple=None, # W x H
                 cam_type: int=0,
                 detector_delay: int=25,
                 flip_cam_h: bool=True):
    
        self.name = name
        self.box_size = box_size
        self.cam_type = cam_type
        self.detector_delay = detector_delay 
        self.flip_cam_h = flip_cam_h
        
    def start_cam(self):
        
        cap = cv2.VideoCapture(self.cam_type)
        if self.box_size:
             cap.set(3 ,round(self.box_size[0]))
             cap.set(4 ,round(self.box_size[1]))
                         
        WIDTH_CAM = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        HEIGHT_CAM = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        
        status_delay = False
        delay_counter = 0
        task_log = None
        TH = (HEIGHT_CAM // 2) - 10
        
        # START CAM LOOP
        while cap.isOpened():
            s, frame = cap.read()
            print(WIDTH_CAM, HEIGHT_CAM)
            
            cv2.line(frame, (0, TH),
                     (WIDTH_CAM, TH),
                     (0,0,255), 6)
            
            # Wanna flip the cam?
            frame = cv2.flip(frame, 1) if self.flip_cam_h else frame
            
            landmark_list, frame, wrist_pos, hand_side = detect_hand(image=frame,
                                                                     draw_landmarks=True)
            
            list_point = list_opened_fingers(landmark_list=landmark_list, 
                                             subtractor=2, 
                                             hand_side=hand_side)
            
            # LOG
            print(list_point)
            print(hand_side)
            
            if (wrist_pos and not status_delay) and wrist_pos[1] < TH:
                task_log = None
                if list_point == [0,0,1,1,1]:
                    status_delay = True
                    task_log = "Right Button Clicked"
                    print(task_log)
                    pyautogui.press("right")
                
                if list_point == [1,1,1,0,0]:
                    status_delay = True
                    task_log = "Left Button Clicked"
                    print(task_log)
                    pyautogui.press("left")
            
            if status_delay: delay_counter +=1
            if delay_counter == self.detector_delay:
                delay_counter = 0
                status_delay = False
            
            try:
                import win32gui
                fs_win = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                fs_win_rep = fs_win.replace(" ","").split("-")[-1]
            except:
                print("You're using Windows OS")
                
            cv2.putText(frame,
                        f"Current Window: {fs_win_rep}",
                        (5, TH+30),
                        cv2.FONT_HERSHEY_PLAIN, 1,
                        (0,255,0), 2)
            
            # Log Curr Window
            print("curr window:",fs_win)
                    
            cv2.putText(frame,
                f"Task Log: {task_log}",
                (5, TH+50),
                cv2.FONT_HERSHEY_PLAIN, 1,
                (0,255,0), 2)
            
            try:
                cv2.setWindowProperty(self.name, 
                                      cv2.WND_PROP_TOPMOST, 1)
            except:
                print("Something went wrong, can't make the window stick on top :(")

            # Start cam
            cv2.imshow(self.name, frame)
            
            # exit
            if cv2.waitKey(1)==ord("q") or cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1: 
                cap.release(); cv2.destroyAllWindows()
                break ## pressing q for exit
            
if __name__ == "__main__":
    cam = Camera()
    cam.start_cam()