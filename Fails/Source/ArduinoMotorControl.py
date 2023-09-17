import serial
import time

# Serial port configuration
serial_port = '/dev/ttyACM0'  # Adjust the port accordingly
baud_rate = 9600

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_control(power_percent):
    command = f"{power_percent}\n"
    ser.write(command.encode())

def main():
    try:
        ser.flushInput()

        while True:
            power_percent = int(input("Enter power output percentage (0-100): "))
            
            # Constrain power percentage to a valid range
            power_percent = max(0, min(100, power_percent))

            send_control(power_percent)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
