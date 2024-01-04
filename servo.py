from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class DualServoController:
    def __init__(self, pin1, pin2, min_pulse_width, max_pulse_width, initial_position=-90):
        self.factory = PiGPIOFactory()

        # Servo 1 setup
        self.servo1 = Servo(pin1, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.initial_position = initial_position

        # Servo 2 setup
        self.servo2 = Servo(pin2, pin_factory=self.factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)
        self.servo2.value = self.map_position(0)  # Set the initial position for servo2 to zero
  # Set the initial position for servo2

    def map_position(self, degrees):
        # Map degrees to servo values (between -1 and 1)
        return (degrees + 90) / 180.0 * 2.0 - 1.0

    def rotate_servo1(self, angle):
        self.servo1.value = self.map_position(angle)
        time.sleep(1)  # Adjust this delay if needed

    def rotate_servo2(self, angle):
        servo2_value = self.map_position(angle)

        # Ensure the servo value is within the valid range
        servo2_value = max(-1, min(1, servo2_value))

        self.servo2.value = servo2_value
        time.sleep(1)  # Adjust this delay if needed


    def rotate_servo2_continuously(self):
        total_degrees = 180
        degrees_per_step = 12.8
        steps = int(total_degrees / degrees_per_step)

        while True:
            for step in range(steps):
                self.rotate_servo2(step * degrees_per_step)

    def control_servo1(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= 4 and elapsed_time < 4.5:
            # Rotate servo 1 to 60 degrees
            self.rotate_servo1(self.initial_position + 60)
        elif elapsed_time >= 7 and elapsed_time < 7.5:
            # Rotate servo 1 to 100 degrees
            self.rotate_servo1(self.initial_position + 100)
        else:
            # Return servo 1 to the start position
            self.rotate_servo1(self.initial_position)

        # Check if 10 seconds have passed, and reset the timer
        if elapsed_time >= 10:
            self.start_time = time.time()

    def run(self):
        try:
            self.start_time = time.time()
            while True:
                self.control_servo1()
                self.rotate_servo2_continuously()
                time.sleep(0.1)  # Adjust the sleep duration based on your needs
        except KeyboardInterrupt:
            self.servo1.close()
            self.servo2.close()

if __name__ == "__main__":
    dual_servo_controller = DualServoController(13, 18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, initial_position=-90)

    try:
        dual_servo_controller.run()

    except KeyboardInterrupt:
        pass

    finally:
        dual_servo_controller.servo1.value = 0  # Set servo 1 back to the initial position
        dual_servo_controller.servo2.value = 0  # Set servo 2 back to the initial position
