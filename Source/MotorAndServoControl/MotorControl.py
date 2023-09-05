import Jetson.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for ESC control
esc_gpio_pin = 18  # Change this to the appropriate GPIO pin number

# Set up the GPIO pin for output
GPIO.setup(esc_gpio_pin, GPIO.OUT)

# Create a PWM object for the ESC control
pwm = GPIO.PWM(esc_gpio_pin, 50)  # 50 Hz PWM signal (standard for ESC)

# Start the PWM signal with 0% duty cycle (throttle off)
pwm.start(0)

try:
    while True:
        # Set different duty cycles to control the ESC
        pwm.ChangeDutyCycle(10)  # 10% throttle (minimum)
        time.sleep(2)  # Keep the throttle at 10% for 2 seconds
        
        pwm.ChangeDutyCycle(50)  # 50% throttle (midway)
        time.sleep(2)  # Keep the throttle at 50% for 2 seconds
        
        pwm.ChangeDutyCycle(90)  # 90% throttle (maximum)
        time.sleep(2)  # Keep the throttle at 90% for 2 seconds

except KeyboardInterrupt:
    # Stop the PWM signal and clean up GPIO
    pwm.stop()
    GPIO.cleanup()
