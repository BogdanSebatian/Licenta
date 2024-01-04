from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class ServoController:
    def __init__(self, pin, min_pulse_width, max_pulse_width, initial_position=0):
        self.factory = PiGPIOFactory()
        self.servo = Servo(pin, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.start_time = time.time()
        self.initial_position = initial_position
        self.servo.value = self.map_position(self.initial_position)
    
    def map_position(self, degrees):
        # Map degrees to servo values (between -1 and 1)
        return (degrees + 90) / 180.0 * 2 - 1

    def control_servo(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 4 and elapsed_time < 4.5:
            # Rotate servo 30 degrees
            self.servo.value = self.map_position(self.initial_position + 60)
        elif elapsed_time >= 7 and elapsed_time < 7.5:
            # Rotate servo 60 degrees
            self.servo.value = self.map_position(self.initial_position + 100)
        else:
            # Return servo to the start position
            self.servo.value = self.map_position(self.initial_position)

        # Check if 10 seconds have passed, and reset the timer
        if elapsed_time >= 10:
            self.start_time = time.time()

def main():
    servo_controller = ServoController(13, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, initial_position=-90)

    try:
        while True:
            servo_controller.control_servo()
            # Add more logic here if needed
            time.sleep(0.1)  # Adjust the sleep duration based on your needs
    except KeyboardInterrupt:
        servo_controller.servo.close()

if __name__ == "__main__":
    main()
