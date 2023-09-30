from machine import Pin
import time

led = Pin(13, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led.toggle()

while True:
    if button.value():
        led.toggle()
        time.sleep(0.5)
        print("pressed")