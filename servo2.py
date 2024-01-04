from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from datetime import datetime

class DualServoController:
    def __init__(self, pin1, pin2, min_pulse_width, max_pulse_width, initial_position1=0, initial_position2=0):
        self.factory = PiGPIOFactory()
        self.servo1 = Servo(pin1, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.servo2 = Servo(pin2, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.start_time_servo1 = time.time()
        self.start_time_servo2 = time.time() 
        self.initial_position1 = initial_position1
        self.initial_position2 = initial_position2

    def map_position(self, degrees):
        return (degrees + 90) / 180.0 * 2 - 1

    def control_servo1(self, first_time, second_time):
        elapsed_time = time.time() - self.start_time_servo1

        if elapsed_time >= first_time and elapsed_time < first_time + 0.5:
            self.servo1.value = self.map_position(self.initial_position1 + 60)
        elif elapsed_time >= second_time and elapsed_time < second_time + 0.5:
            self.servo1.value = self.map_position(self.initial_position1 + 140)
        else:
            self.servo1.value = self.map_position(self.initial_position1)
            
        if elapsed_time >= 10:
            self.start_time_servo1 = time.time()

    def control_servo2(self, move_duration):
        elapsed_time = time.time() - self.start_time_servo2

        step_number = int(elapsed_time / move_duration)

        angle_per_step = 180 / 15 
        angle = step_number * angle_per_step

        self.servo2.value = self.map_position(self.initial_position2 + angle)

        if step_number >= 15:
            self.servo2.value = self.map_position(self.initial_position2)
            self.start_time_servo2 = time.time()

def main():
    dual_servo_controller = DualServoController(13, 18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, initial_position1=-90, initial_position2=-90)

    try:
        while True:
            dual_servo_controller.control_servo1(4, 7)
            dual_servo_controller.control_servo2(1)
    except KeyboardInterrupt:
        dual_servo_controller.servo1.close()
        dual_servo_controller.servo2.close()

if __name__ == "__main__":
    main()
