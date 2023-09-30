from machine import Pin, Timer

class Led():
    def __init__(self, pin):
        self.led = Pin(13, Pin.OUT)
        self.timer = Timer()
        
    def turn_on(self):
        self.led.value(True)
        
    def turn_off(self):
        self.led.value(False)
        
    def blink(self, frequency=2.5):
        self.timer.init(freq=frequency, mode=Timer.PERIODIC, callback=self._blink_helper)

    def stop_blinking(self):
        self.timer.deinit()
        self.led.value(False)

    def _blink_helper(self, timer):
        self.led.toggle()
