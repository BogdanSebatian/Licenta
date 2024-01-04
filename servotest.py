from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class DualServoController:
    def __init__(self, pin1, pin2, min_pulse_width, max_pulse_width, initial_position1=0, initial_position2=0):
        self.factory = PiGPIOFactory()
        self.servo1 = Servo(pin1, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.servo2 = Servo(pin2, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.start_time = time.time()
        self.initial_position1 = initial_position1
        self.initial_position2 = initial_position2

    def map_position(self, degrees):
        # Map degrees to servo values (between -1 and 1)
        return (degrees + 90) / 180.0 * 2 - 1

    def control_servos(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 4 and elapsed_time < 4.5:
            # Rotate servo 1 by 60 degrees
            self.servo1.value = self.map_position(self.initial_position1 + 60)
        elif elapsed_time >= 7 and elapsed_time < 7.5:
            # Rotate servo 1 by 100 degrees
            self.servo1.value = self.map_position(self.initial_position1 + 100)
        else:
            # Return servo 1 to the start position
            self.servo1.value = self.map_position(self.initial_position1)

        # Rotate servo 2 continuously
        self.servo2.value = (elapsed_time % 10) / 10 * 2 - 1

        # Check if 10 seconds have passed, and reset the timer
        if elapsed_time >= 10:
            self.start_time = time.time()

def main():
    dual_servo_controller = DualServoController(13, 18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, initial_position1=-90, initial_position2=-90)

    try:
        while True:
            dual_servo_controller.control_servos()
            # Add more logic here if needed
            time.sleep(0.1)  # Adjust the sleep duration based on your needs
    except KeyboardInterrupt:
        dual_servo_controller.servo1.close()
        dual_servo_controller.servo2.close()

if __name__ == "__main__":
    main()
