from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Configuration Section
servo_pin = 18
min_pulse_width = 0.5 / 1000  # in seconds
max_pulse_width = 2.5 / 1000  # in seconds
total_degrees = 180
degrees_per_step = 12.8
rotation_delay = 1  # in seconds

# Set up PiGPIOFactory to control servo on a remote Pi (if needed)
# If using the local Pi, you can skip this line
pi_gpio_factory = PiGPIOFactory()

# Set up the Servo with custom pulse width values
servo = Servo(servo_pin, pin_factory=pi_gpio_factory, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)

# Function to rotate the servo to a specific angle
def rotate_servo(angle):
    # Map the angle from degrees (0 to 180) to servo values (-1 to 1)
    servo.value = (angle / 180.0) * 2.0 - 1.0
    time.sleep(rotation_delay)

# Function to rotate the servo continuously
def rotate_continuously():
    steps = int(total_degrees / degrees_per_step)

    while True:
        for step in range(steps):
            rotate_servo(step * degrees_per_step)

# Main function
if __name__ == "__main__":
    try:
        rotate_continuously()

    except KeyboardInterrupt:
        pass

    finally:
        servo.value = 0  # Set the servo back to the initial position
