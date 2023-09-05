import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C communication with PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# Set PWM frequency (Hz)
pca.frequency = 50  # Typical for servos and ESCs, adjust as needed

# Set ESC and servo channels
esc_channel = 0  # Adjust to the appropriate channel
servo_channel = 1  # Adjust to the appropriate channel

# ESC configuration (adjust these values for your ESC)
esc_min_pulse = 1000  # Minimum pulse width for the ESC (microseconds)
esc_max_pulse = 2000  # Maximum pulse width for the ESC (microseconds)

# Servo configuration (adjust these values for your servo)
servo_min_pulse = 1000  # Minimum pulse width for the servo (microseconds)
servo_max_pulse = 2000  # Maximum pulse width for the servo (microseconds)

# Function to set ESC speed
def set_esc_speed(pulse_width):
    pca.channels[esc_channel].duty_cycle = int(pulse_width / 20 * 0xFFFF)

# Function to set servo angle
def set_servo_angle(angle):
    angle = max(min(angle, 180), 0)  # Ensure angle is within 0-180 degrees
    pulse_width = servo_min_pulse + (servo_max_pulse - servo_min_pulse) * angle / 180
    pca.channels[servo_channel].duty_cycle = int(pulse_width / 20 * 0xFFFF)

try:
    while True:
        # Arm the ESC (set it to minimum throttle)
        set_esc_speed(esc_min_pulse)
        time.sleep(2)

        # Increase ESC speed gradually
        for pulse in range(esc_min_pulse, esc_max_pulse, 10):
            set_esc_speed(pulse)
            time.sleep(0.1)

        # Set servo to 90 degrees
        set_servo_angle(90)
        time.sleep(2)

        # Set servo to 0 degrees
        set_servo_angle(0)
        time.sleep(2)

except KeyboardInterrupt:
    # Stop the ESC and servo
    set_esc_speed(esc_min_pulse)
    set_servo_angle(90)
    time.sleep(1)

    # Turn off all PWM channels
    for i in range(16):
        pca.channels[i].duty_cycle = 0

    print("PWM channels turned off.")
