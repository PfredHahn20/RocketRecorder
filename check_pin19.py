from gpiozero import LED, Button, Buzzer
import time
import subprocess
import sys
import os
import signal

log_file = open("/home/pi/logs/check_pin19.log", "w")
sys.stdout = log_file
sys.stderr = log_file

# Setup
switch = Button(19, pull_up=True)
led_init = LED(26)
led_rec = LED(20)
buzzer = Buzzer(13)

def flash_led():
        for _ in range(20):
                led_init.on()
                led_rec.off()
                time.sleep(0.05)
                led_init.off()
                led_rec.on()
                time.sleep(0.05)
                led_rec.off()

def chirp_buzzer(times):
    for _ in range(times):
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
        time.sleep(0.1)

def start_gpio_control():
        flash_led()
        chirp_buzzer(3)
        print("Starting gpio_control.py")
        return subprocess.Popen(["python3", "/home/pi/gpio_control.py"], preexec_fn=os.setsid)

try:
        print("Starting check_pin19.py script")
        while True:
                switch_state = switch.is_pressed
                print(f"Switch state: {'ON' if switch_state else 'OFF'}")
                if switch_state:
                        print("Switch is ON, starting gpio_control.py")
                        start_gpio_control()
                        log_file.close()
                        break
                time.sleep(1)
except KeyboardInterrupt:
        print("Script interrupted by user")
        log_file.close()
