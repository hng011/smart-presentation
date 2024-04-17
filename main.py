import cv2
import numpy as np
import pyautogui
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands( # Instantiating
    max_num_hands=1,
    min_detection_confidence=0.8
)


def detect_hand(image: np.ndarray=None, draw_landmarks: bool=True) -> tuple:
    h, w, _=image.shape
    res=hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    multi_hl=res.multi_hand_landmarks
    multi_hn=res.multi_handedness
    position=[]
    if multi_hl:
        for data in multi_hn:
            hand_side=data.classification[0].label
            cfd_score=data.classification[0].score
        for hand_marks in multi_hl:
            for i, lm in enumerate(hand_marks.landmark):
                index, cx, cy=i, int(lm.x*w), int(lm.y*h) # Converting from ratio to pixel?
                # print(i,cx,cy) 
                position.append([index, cx, cy])
                if draw_landmarks:
                    cv2.rectangle(image, (cx, cy), (cx+10, cy+15), (255,0,255), 25)
                    mp_draw.draw_landmarks(image, hand_marks, mp_hands.HAND_CONNECTIONS) # Draw landmarks on frame
                    
                if i==0: #wrist
                    cv2.putText(image, 
                                f"{hand_side} hand", 
                                (cx-50, cy+50), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
                    # Confident score
                    cv2.putText(image, 
                                f"{cfd_score:.2f}%", 
                                (cx-25, cy+90), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
                                            
        
        print(f"{hand_side} hand detected | score {cfd_score}")
    else:
        print("No Hand Detected")
    
    return position, frame_flipped

if __name__=="__main__":
    cap=cv2.VideoCapture(0)
    WIDTH_CAM,HEIGHT_CAM=920, 640
    cap.set(3, WIDTH_CAM)
    cap.set(4, HEIGHT_CAM)
    # cap.set(10, 100) # Brightness

    while cap.isOpened():
        success, frame=cap.read()

        frame_flipped=cv2.flip(frame, 1)

        position, detector=detect_hand(image=frame_flipped, draw_landmarks=True)
        print(position)

        cv2.imshow("webcam", detector)

        if cv2.waitKey(1)==ord("q"): break
    
    cap.release()
    cv2.destroyAllWindows()