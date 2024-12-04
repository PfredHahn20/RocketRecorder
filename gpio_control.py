from gpiozero import Button, LED, Buzzer
from signal import pause
import time
import os
import subprocess
import sys

log_file = open("/home/pi/logs/gpio_control.log", "w")
sys.stdout = log_file
sys.stderr = log_file

button = Button(21, pull_up=True)
led_init = LED(26)
led_rec = LED(20)
buzzer = Buzzer(13)

button_pressed_time=None
recording = False
hold_time = 3

def chirp_buzzer(times):
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
        time.sleep(0.1)


def button_pressed():
        global button_pressed_time
        print("Button pressed...please continue holding")
        button_pressed_time = time.time()
        led_init.on()
        time.sleep(hold_time)
        led_init.blink(on_time=0.25, off_time=0.25)
        chirp_buzzer(1)
        print("Hold time passed, start recording sequenece...")
        start_recording()

def button_released():
        global button_pressed_time
        print("Button Released")
        button_pressed_time = None

def start_recording():
        global recording
        if not recording:
                recording = True
                led_rec.on()
                led_init.off()
                print("Starting recording process...")
                try:
                        subprocess.Popen(["/home/pi/start_recording.sh"])
                        print("Initialized...Recording Started")
                except Exception as e:
                        print(f"Failed to start recording process: {e}")
                        recording = False

def stop_recording():
        global recording
        if recording:
                recording = False
                led_rec.off()
                led_init.off()
                print("Ending recording process...")
                try:
                        subprocess.Popen(["/home/pi/stop_recording.sh"])
                        print("Recording Stopped")
                except Exception as e:
                        print(f"Failed to stop recording process: {e}")

def button_held():
        global recording
        if recording:
                print("Button held for 3 seconds during recording...stopping recording sequence...")
                stop_recording()
                chirp_buzzer()

button.when_pressed = button_pressed
button.when_released = button_released
button.when_held = button_held

print("Script is running, waiting for user input...")

try:
        pause()
except Exception as e:
        print(f"An error has occured: {e}")
finally:
        print("Logging Ended")
        log_file.close()
