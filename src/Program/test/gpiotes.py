import Jetson.GPIO as GPIO
import time

# Set the GPIO pin number for ESC control
esc_gpio_pin = 32

# Set the ESC pulse width values (in microseconds)
min_pulse = 1000  # Minimum throttle value (full reverse)
max_pulse = 2000  # Maximum throttle value (full forward)
neutral_pulse = 1500  # Neutral throttle value (stopped)

# Set the PWM frequency (in Hz)
pwm_frequency = 50  # 50 Hz is typical for ESCs

# Initialize the GPIO library
GPIO.setmode(GPIO.BOARD)
GPIO.setup(esc_gpio_pin, GPIO.OUT)

# Create a PWM instance for the ESC
esc_pwm = GPIO.PWM(esc_gpio_pin, pwm_frequency)

def set_throttle(throttle):
    pulse_width = min_pulse + (max_pulse - min_pulse) * throttle
    esc_pwm.ChangeDutyCycle(pulse_width / 10.0)  # Divide by 10 for 10% duty cycle

# Disarm the ESC
def disarm_esc():
    esc_pwm.stop() # Set throttle to neutral
    time.sleep(1)  # Wait for the ESC to recognize the neutral throttle
    print("ESC disarmed")
def arm_esc():
    set_throttle(0)  # Set throttle to minimum (full reverse)
    time.sleep(1)  # Wait for the ESC to recognize the min throttle
    print("ESC armed")

try:
    esc_pwm.start(0)  # Start PWM with 0% duty cycle
    arm_esc()  # Arm the ESC

    # Set throttle values (between 0 and 1)
    set_throttle(0.2)  # Example: Set throttle to 20%
    time.sleep(5)  # Run for 5 seconds

    set_throttle(0.5)  # Example: Set throttle to 50%
    time.sleep(5)  # Run for 5 seconds

    set_throttle(0.8)  # Example: Set throttle to 80%
    time.sleep(5)  # Run for 5 seconds

    # Disarm the ESC when done
    disarm_esc()

except KeyboardInterrupt:
    disarm_esc()  # Disarm the ESC on Ctrl+C

finally:
    esc_pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO settings