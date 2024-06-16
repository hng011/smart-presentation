from feature_modules.Detector import HandDetector
from feature_modules import np, cv2 

"""
    Instantiating the HandDetector class
"""

hand_detector = HandDetector(max_num_hands=1, 
                             min_detection_confidence=0.9)
mp_hands = hand_detector.mphands
mp_draw = hand_detector.draw
hands = hand_detector.hands

def detect_hand(image: np.ndarray=None, 
                draw_landmarks: bool=False, 
                show_score: bool=False) -> tuple:
    h, w, _ = image.shape
    res = hands.process(cv2.cvtColor(image, 
                                   cv2.COLOR_BGR2RGB))
    multi_hl = res.multi_hand_landmarks
    multi_hn = res.multi_handedness
    position = []
    wrist_position = ()
    hand_side = None

    if multi_hl:
        for data in multi_hn:
            hand_side = data.classification[0].label
            cfd_score = data.classification[0].score
        for hand_marks in multi_hl:
            for i, lm in enumerate(hand_marks.landmark):
                # Converting from ratio to pixel?
                index, cx, cy = i, int(lm.x*w), int(lm.y*h) 
                
                position.append([index, cx, cy])
                if draw_landmarks:
                    cv2.rectangle(image, (cx, cy), 
                                  (cx+5, cy+10), 
                                  (255,0,255), 5)
                    mp_draw.draw_landmarks(image, 
                                           hand_marks, 
                                           # Draw landmarks on frame
                                           mp_hands.HAND_CONNECTIONS) 
                    
                #Detecting wrist
                if i == 0: 
                    wrist_position = (cx, cy)
                    cv2.putText(image, 
                                f"{hand_side} hand", 
                                (cx-50, cy+50), 
                                cv2.FONT_HERSHEY_PLAIN, 1, 
                                (255,0,0), 2)
                    # Confident score display
                    cv2.putText(image, 
                                f"{cfd_score:.2f}%", 
                                (cx-25, cy+70), 
                                cv2.FONT_HERSHEY_PLAIN, 1, 
                                (255,0,0), 2)
                                            
        if show_score:
            print(f"{hand_side} hand detected | score {cfd_score}")
    else:
        print("No Hand Detected")
    
    return position, image, wrist_position, hand_side