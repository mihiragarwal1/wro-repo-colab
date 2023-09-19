import Jetson.GPIO as GPIO
import time

# Set GPIO mode to BOARD
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pin
pin = 18

# Set the pin as an output
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
