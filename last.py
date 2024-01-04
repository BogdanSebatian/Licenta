from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class ServoController:
    def __init__(self, pin, min_pulse_width, max_pulse_width, initial_position=0):
        self.factory = PiGPIOFactory()
        self.servo = Servo(pin, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, pin_factory=self.factory)
        self.initial_position = initial_position
        self.servo.value = self.map_position(self.initial_position)

    def map_position(self, degrees):
        # Map degrees to servo values (between -1 and 1)
        return (degrees + 90) / 180.0 * 2 - 1

    def set_position(self, degrees):
        self.servo.value = self.map_position(degrees)

    def move_to_initial_position(self):
        self.set_position(self.initial_position)

def rotate_servo_continuous(servo, total_degrees, degrees_per_step, rotation_delay):
    steps = int(total_degrees / degrees_per_step)

    for _ in range(steps):
        servo.value = (degrees_per_step / 180.0) * 2.0 - 1.0
        time.sleep(rotation_delay)

def main():
    servo_controller1 = ServoController(13, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, initial_position=-90)
    servo_controller2 = ServoController(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, initial_position=-90)

    try:
        while True:
            servo_controller1.set_position(-30)
            time.sleep(4)
            servo_controller1.set_position(30)
            time.sleep(0.5)
            servo_controller1.move_to_initial_position()

            rotate_servo_continuous(servo_controller2.servo, total_degrees=12.8 * 14, degrees_per_step=12.8, rotation_delay=1)
            servo_controller2.move_to_initial_position()

            time.sleep(0.1)  # Adjust the sleep duration based on your needs

    except KeyboardInterrupt:
        servo_controller1.servo.close()
        servo_controller2.servo.close()

if __name__ == "__main__":
    main()
