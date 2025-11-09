#include <Servo.h>

const int SERVO_PIN_1 = 9;   // Back left leg
const int SERVO_PIN_2 = 7;   // Back right leg (facing opposite)

Servo motor1;
Servo motor2;

int currentAngle = 90;   // Start centred

void setup() {
  Serial.begin(9600);

  // Calibration (move both to neutral 90°)
  motor1.attach(SERVO_PIN_1);
  motor2.attach(SERVO_PIN_2);

  motor1.write(90);
  motor2.write(90);
  delay(600);

  motor1.detach();
  motor2.detach();

  Serial.println("Arduino Ready - Starting Neutral (FIST assumed)");
}

void moveServos(int angle1, int angle2) {
  motor1.attach(SERVO_PIN_1);
  motor2.attach(SERVO_PIN_2);

  motor1.write(angle1);
  motor2.write(angle2);

  delay(400);

  motor1.detach();
  motor2.detach();
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // FIST → move to +90° (motor1 = 180°, motor2 = 0°)
    if (cmd == "FIST") {
      if (currentAngle != 180) {
        moveServos(180, 0);
        currentAngle = 180;
        Serial.println("Moved to +90° (FIST → motor1=180°, motor2=0°)");
      } else {
        Serial.println("Already at +90°");
      }
    }

    // PALM → move to -90° (motor1 = 0°, motor2 = 180°)
    else if (cmd == "PALM") {
      if (currentAngle != 0) {
        moveServos(0, 180);
        currentAngle = 0;
        Serial.println("Moved to -90° (PALM → motor1=0°, motor2=180°)");
      } else {
        Serial.println("Already at -90°");
      }
    }

    // Ignore other gestures
    else {
      Serial.print("Received: ");
      Serial.println(cmd);
    }
  }
}
