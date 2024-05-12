from feature_modules.Detector import HandDetector
from feature_modules import np, cv2 

"""
    Instantiating the HandDetector class
"""

hand_detector = HandDetector(max_num_hands=1, min_detection_confidence=0.8)
mp_hands = hand_detector.mphands
mp_draw = hand_detector.draw
hands = hand_detector.hands

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