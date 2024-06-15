from feature_modules import mp

class HandDetector:
    def __init__(self, 
                 max_num_hands: int=1, 
                 min_detection_confidence: float=0.8):
        self.mphands = mp.solutions.hands
        self.draw = mp.solutions.drawing_utils
        self.hands = self.mphands.Hands(
                        max_num_hands=max_num_hands,
                        min_detection_confidence=min_detection_confidence
                    )