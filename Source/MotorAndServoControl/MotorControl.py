import time
import adafruit_blinka as board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(27, 28)
pca = PCA9685(i2c)

pca.frequency = 50

esc_channel = 7
servo_channel = 0

esc_min_pulse = 1000
esc_max_pulse = 2000

servo_min_pulse = 1000
servo_max_pulse = 2000

def set_esc_speed(pulse_width):
    pca.channels[esc_channel].duty_cycle = int(pulse_width / 20 * 0xFFF)

def set_servo_angle(angle):
    angle = max(min(angle,180),0)
    pulse_width= servo_max_pulse+(servo_max_pulse-servo_min_pulse)*angle/180
    pca.channels[servo_channel].duty_cycle = int(pulse_width/20*0xFFF)

try:
    while True:
        set_esc_speed(esc_min_pulse)
        time.sleep(2)

        for pulse in range(esc_min_pulse,esc_max_pulse,10):
            set_esc_speed(pulse)
            time.sleep(0.1)

            set_servo_angle(90)
            time.sleep(2)

            set_servo_angle(0)
            time.sleep(2)

except KeyboardInterrupt:
    set_esc_speed(esc_min_pulse)
    set_servo_angle(0)
    time.sleep(1)

    for i in range(16):
        pca.channels[i].duty_cycle = 0

        print("OFF")