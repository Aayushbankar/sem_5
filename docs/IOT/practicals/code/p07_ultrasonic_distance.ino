// P07 — HC-SR04 ultrasonic distance with NewPing library
// TRIG -> GPIO 5, ECHO -> GPIO 18 (via 1k+2k divider to 3V3)
// Library: "NewPing by Tim Eckel" (Library Manager)

#include <NewPing.h>

#define TRIG_PIN 5
#define ECHO_PIN 18
#define MAX_DIST 400            // cm, HC-SR04 maximum range

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DIST);

void setup() {
  Serial.begin(115200);
  Serial.println("P07: Ultrasonic distance sensor started.");
}

void loop() {
  // returns distance in cm; 0 means out of range / no echo
  unsigned int dist = sonar.ping_cm();

  if (dist == 0) {
    Serial.println("Distance: out of range");
  } else {
    Serial.print("Distance: ");
    Serial.print(dist);
    Serial.println(" cm");
  }

  delay(500);                   // measure twice per second
}
