# Gesture-Controlled Robotic Dog 🐶✋🤖

This project is a small robotic dog that reacts to hand gestures detected through a webcam.  
Using **Python**, **OpenCV**, and **MediaPipe**, the system recognises specific hand shapes and sends serial commands to an **Arduino**, which controls three servo motors responsible for the dog’s back legs and tail.

---

## 🎮 Gesture Controls

| Hand Gesture | Action Triggered | Robot Behaviour |
|--------------|-----------------|----------------|
| ✊ **Fist** | Sit | Back leg servos move to the seated angle. |
| ✋ **Open Palm** | Stand | Back legs extend to a standing position. |
| ✌️ **Peace Sign** | Wag Tail | Tail servo oscillates continuously to simulate wagging. |

The robot always starts from a neutral leg position to ensure consistent mechanical alignment every time the system is powered on.

---

## 🧠 System Overview

1. **Python Script**
   - Captures video from the webcam.
   - Uses MediaPipe to detect hand landmarks.
   - Classifies gesture into *FIST*, *PALM*, or *PEACE*.
   - Sends a corresponding command string to the Arduino via serial.

2. **Arduino**
   - Reads serial commands.
   - Moves the two back leg servos to sit or stand positions depending on the gesture.
   - Controls a third servo (tail) that wags when the peace sign is detected.

---

## 🔧 Hardware Requirements

- Arduino Uno / Nano
- 3 × SG90 or MG90S Servos
- USB cable for serial communication
- Standard webcam
- External servo power supply recommended (5V, 2A)

**Wiring Note:**  
Never power multiple servos directly from Arduino 5V pin. Use an external regulated 5V supply and **common ground**.

---

## 🧰 Software Requirements

| Component | Version / Library |
|----------|------------------|
| Python 3.x | Recommended 3.8+ |
| OpenCV | `pip install opencv-python` |
| MediaPipe | `pip install mediapipe` |
| PySerial | `pip install pyserial` |
| Arduino IDE | Latest |
| Arduino Servo Library | `#include <Servo.h>` |

---

## 🖥️ Running the System

### 1. Upload Arduino Code
Upload the provided `.ino` file to your Arduino.  
Ensure the correct servo pins match:
Back Left Leg → D9
Back Right Leg → D7
Tail Servo → D6 
