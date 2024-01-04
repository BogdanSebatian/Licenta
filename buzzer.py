import RPi.GPIO as GPIO
import time
import threading
import sys
from pynput import keyboard

# Set the GPIO mode and pin
GPIO.setmode(GPIO.BCM)
buzzer_pin = 22

# Define the notes and their corresponding frequencies
notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
}

# Function to play a note for a given duration
def play_note(note, duration):
    frequency = notes[note]
    if frequency > 0:
        GPIO.setup(buzzer_pin, GPIO.OUT)
        pwm = GPIO.PWM(buzzer_pin, frequency)
        pwm.start(50)  # 50% duty cycle
        time.sleep(duration)
        pwm.stop()
        GPIO.setup(buzzer_pin, GPIO.IN)  # Reset the GPIO pin

# Function to play a melody
def play_melody(melody, stop_event):
    for note, duration in melody:
        if stop_event.is_set():
            break
        play_note(note, duration)

# Define a simple melody (you can customize this)
melody = [
    ('E4', 0.5),
    ('D4', 0.5),
    ('C4', 0.5),
    ('D4', 0.5),
    ('E4', 0.5),
    ('E4', 0.5),
    ('E4', 1),
]

# Set up stop event
stop_event = threading.Event()

# Callback for key press events
def on_key_press(key):
    try:
        if key.char == 'P' or key.char == 'p':
            stop_event.clear()
            play_thread = threading.Thread(target=play_melody, args=(melody, stop_event))
            play_thread.start()
        elif key.char == 'S' or key.char == 's':
            stop_event.set()
    except AttributeError:
        pass

# Set up the keyboard listener
listener = keyboard.Listener(on_press=on_key_press)
listener.start()

try:
    listener.join()  # Wait for the listener thread to finish
finally:
    GPIO.cleanup()
    sys.exit()
