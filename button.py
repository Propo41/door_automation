from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_DOWN)

while True:
    print(button.value())
    if not button.value():
        print("pressed")
