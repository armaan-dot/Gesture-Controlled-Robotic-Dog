import cv2
import mediapipe as mp
import serial
import time

# Setup serial communication with Arduino
arduino = serial.Serial('COM9', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Give Arduino time to reset

# Mediapipe hands setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

def finger_status(hand_landmarks, hand_label='Right'):
    """Return a list of 5 booleans: True if finger is up."""
    tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    fingers = []
    if hand_label == 'Right':
        fingers.append(hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x)
    else:
        fingers.append(hand_landmarks.landmark[tips[0]].x > hand_landmarks.landmark[tips[0]-1].x)
    for id in range(1, 5):
        fingers.append(hand_landmarks.landmark[tips[id]].y < hand_landmarks.landmark[tips[id]-2].y)
    return fingers

def classify_hand(fingers):
    """Return gesture name based on finger states"""
    if fingers == [False, False, False, False, False]:
        return "FIST"
    elif fingers == [True, True, True, True, True]:
        return "PALM"
    elif fingers == [True, False, False, False, False]:
        return "THUMB_UP"
    elif fingers[1] and fingers[2] and not fingers[0] and not fingers[3] and not fingers[4]:
        return "PEACE"
    else:
        return "UNKNOWN"

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)
            gesture = "NO_HAND"
            
            if result.multi_hand_landmarks:
                for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks,
                                                           result.multi_handedness):
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    hand_label = hand_handedness.classification[0].label
                    fingers = finger_status(hand_landmarks, hand_label)
                    gesture = classify_hand(fingers)
            
            # Send gesture to Arduino
            arduino.write((gesture + '\n').encode('utf-8'))
            
            # Display gesture
            cv2.putText(frame, gesture, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            cv2.imshow("Hand Gesture Detection", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                arduino.write("ERROR\n".encode('utf-8'))
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        arduino.close()
