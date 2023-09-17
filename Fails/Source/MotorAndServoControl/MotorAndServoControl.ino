#include <Servo.h>

Servo servo;     // Create a servo object to control the servo
int escPin = 9;  // Digital pin for ESC control
int throttle = 1500;  // Neutral throttle value for ESC (adjust as needed)

void setup() {
  servo.attach(3);        // Attach servo to digital pin 3
  pinMode(escPin, OUTPUT);  // Set ESC pin as an output
  analogWrite(escPin, throttle);  // Send neutral signal to ESC
  servo.write(90);  // Set servo to mid position (90 degrees)
  
  Serial.begin(9600);  // Initialize serial communication
  delay(2000);         // Wait for ESC to initialize (may vary)
}

void loop() {
  if (Serial.available() > 0) {
    int powerPercent = Serial.parseInt();  // Read power output percentage from serial
    
    // Ensure the power percentage is within the valid range (0 to 100)
    powerPercent = constrain(powerPercent, 0, 100);
    
    // Convert power percentage to ESC throttle value (1000 to 2000)
    throttle = map(powerPercent, 0, 100, 1000, 2000);
    
    // Control servo based on power percentage
    int servoPosition = map(powerPercent, 0, 100, 0, 180);
    servo.write(servoPosition);  // Move the servo to the desired position
    
    // Send ESC throttle value
    analogWrite(escPin, throttle);
    
    Serial.print("Power Output: ");
    Serial.print(powerPercent);
    Serial.println("%");
  }
}
