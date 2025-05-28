import mediapipe as mp
import numpy as np
from math import degrees, acos

mp_hands = mp.solutions.hands

def _landmark_xy(landmark, width, height):
    return int(landmark.x * width), int(landmark.y * height)

def _get_triplet(hand_landmarks, ids, width, height):
    return [_landmark_xy(hand_landmarks.landmark[i], width, height) for i in ids]

def _angle_from_points(points):
    p1, p2, p3 = [np.array(pt) for pt in points]
    l1 = np.linalg.norm(p2 - p3)
    l2 = np.linalg.norm(p1 - p3)
    l3 = np.linalg.norm(p1 - p2)
    if l1 and l3:
        num_den = (l1**2 + l3**2 - l2**2) / (2 * l1 * l3)
        if -1 < num_den < 1:
            return round(degrees(abs(acos(num_den))))
    return 0

def obtenerAngulos(results, width, height):
    for hand_landmarks in results.multi_hand_landmarks:
        lado_mano = (
            "Derecha"
            if hand_landmarks.landmark[17].x > hand_landmarks.landmark[5].x
            else "Izquierda"
        )
        finger_ids = {
            "pinky": [
                mp_hands.HandLandmark.PINKY_TIP,
                mp_hands.HandLandmark.PINKY_PIP,
                mp_hands.HandLandmark.PINKY_MCP,
            ],
            "ring": [
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_PIP,
                mp_hands.HandLandmark.RING_FINGER_MCP,
            ],
            "middle": [
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
            ],
            "index": [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.INDEX_FINGER_PIP,
                mp_hands.HandLandmark.INDEX_FINGER_MCP,
            ],
            "thumb_outer": [
                mp_hands.HandLandmark.THUMB_TIP,
                mp_hands.HandLandmark.THUMB_IP,
                mp_hands.HandLandmark.THUMB_MCP,
            ],
            "thumb_inner": [
                mp_hands.HandLandmark.THUMB_TIP,
                mp_hands.HandLandmark.THUMB_MCP,
                mp_hands.HandLandmark.WRIST,
            ],
        }

        angulosid = [
            _angle_from_points(_get_triplet(hand_landmarks, finger_ids["pinky"], width, height)),
            _angle_from_points(_get_triplet(hand_landmarks, finger_ids["ring"], width, height)),
            _angle_from_points(_get_triplet(hand_landmarks, finger_ids["middle"], width, height)),
            _angle_from_points(_get_triplet(hand_landmarks, finger_ids["index"], width, height)),
            _angle_from_points(_get_triplet(hand_landmarks, finger_ids["thumb_outer"], width, height)),
            _angle_from_points(_get_triplet(hand_landmarks, finger_ids["thumb_inner"], width, height)),
        ]
        pinky_tip = _landmark_xy(
            hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP], width, height
        )
        return [angulosid, pinky_tip, lado_mano]