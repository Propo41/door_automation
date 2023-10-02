from machine import Pin, Timer
import time
from buzzer import Buzzer
import constants
from led import Led
from log import Logger
from mfrc522 import MFRC522

is_door_open = False
is_loading = False

button_open = Pin(11, Pin.IN, Pin.PULL_DOWN)
button_close = Pin(15, Pin.IN, Pin.PULL_DOWN)
button_reset = Pin(14, Pin.IN, Pin.PULL_DOWN)

led_power = Led(25)
led_loading = Led(13)
led_door_open = Led(13)

timer = Timer()
alarm = Buzzer(0)
logger = Logger()

rfid_reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=7, cs=5, rst=18)

def scan_rfid():
    rfid_reader.init()
    (card_status, tag_type) = rfid_reader.request(rfid_reader.REQIDL)
    if card_status == rfid_reader.OK:
        (card_status, card_id) = rfid_reader.SelectTagSN()
        if card_status == rfid_reader.OK:
            rfid_card = int.from_bytes(bytes(card_id),"little", False)  # type: ignore
            print("Detected Card : "+ str(rfid_card))
            return str(rfid_card)
    return False

 
def open_door():
    global is_loading
    global is_door_open
    
    if (is_door_open == False):
        logger.log("Door opening..")
        is_loading = True
        led_loading.blink()
        time.sleep(1)
                    
        # todo: rotate motor
                    
        led_loading.stop_blinking()
        led_door_open.turn_on()
        is_loading = False
        alarm.alert(constants.DOOR_UNLOCKED)
        is_door_open = True
        time.sleep(2)
        logger.log("Door opened!")
    else:
        logger.log("Door already opened!")
        alarm.alert(constants.ALARM_SUCCESS)

def close_door():
    global is_loading
    global is_door_open
    
    if(is_door_open == True):
        logger.log("Door closing...")
        is_loading = True
        led_loading.blink()
                
        # todo: rotate motor
                
        led_loading.stop_blinking()
        led_door_open.turn_off()
        is_loading = False
        alarm.alert(constants.DOOR_LOCKED)
        is_door_open = False
        time.sleep(2)
        logger.log("Door closed!")
    else:
        logger.log("Door already closed!")
        alarm.alert(constants.ALARM_ALREADY_PROCESSED)

def reset_system():
    global is_loading
    global is_door_open
    
    is_loading = True
    alarm.alert(constants.ALARM_LOADING)
    led_loading.blink()
    # todo: reset system
    led_loading.stop_blinking()
    is_loading = True

if __name__ == '__main__':
    logger.log("App started..")
    led_power.turn_on()

    while True:
        if button_open.value() and not is_loading:
            open_door()
        elif button_close.value() and not is_loading:
            close_door()
        elif button_reset.value() and not is_loading:
            reset_system()   
        else:
            card_id = scan_rfid()
            if(type(scan_rfid)=="str"):
                print("card detected")


logger.close()