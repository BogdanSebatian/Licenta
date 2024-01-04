import RPi.GPIO as GPIO
import time

# Set the GPIO mode and the pin number
GPIO.setmode(GPIO.BCM)
button_pin = 17  # Replace with the actual GPIO pin you used

# Set up the GPIO pin as input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.LOW:
            print("Button pressed!")
            # Do something here

        # Add a small delay to debounce the button
        time.sleep(0.2)

except KeyboardInterrupt:
    # Clean up when the script is interrupted
    GPIO.cleanup()
