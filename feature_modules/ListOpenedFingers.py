def list_opened_fingers(landmark_list: list, subtractor: int=2, hand_side: str=None) -> list:
    list_fingers_open=[]
    finger_points=[4,8,12,16,20]

    if landmark_list:
        for point in finger_points:
            if point == 4:
                if  str(hand_side).lower() == "right":
                    # landmark_list[point][1] -> width | landmark_list[point][2] -> height 
                    list_fingers_open.append(1 if landmark_list[point][1] < landmark_list[point-subtractor+1][1] else 0)
                else:
                    list_fingers_open.append(1 if landmark_list[point][1] > landmark_list[point-subtractor+1][1] else 0)
            else:
                list_fingers_open.append(1 if landmark_list[point][2] < landmark_list[point-subtractor][2] else 0)

    return list_fingers_open