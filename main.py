from machine import Pin, Timer
import time
from buzzer import Buzzer
import constants
from led import Led
from log import Logger
from mfrc522 import MFRC522

is_door_open = False
is_loading = False

button_open = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_close = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_reset = Pin(14, Pin.IN, Pin.PULL_DOWN)

led_power = Led(13)
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
            rfid_card = int.from_bytes(bytes(card_id), byteorder='little', signed=False)
            return str(rfid_card)
    return False
 
def open_door():
    pass

def close_door():
    pass

def reset_system():
    pass

if __name__ == '__main__':
    led_power.turn_on()  
    logger.log("App started..")
    while True:
        if button_open.value() and not is_loading:
            if (is_door_open == False):
                logger.log("Door opening..")
                is_loading = True
                led_loading.blink()
                
                open_door()
                
                led_loading.stop_blinking()
                led_door_open.turn_on()
                is_loading = False
                alarm.alert(constants.DOOR_UNLOCKED)
                is_door_open = True
                time.sleep(2)
                logger.log("Door opened!")
            else:
                logger.log("Door already opened!")
                alarm.alert(constants.ALARM_ALREADY_PROCESSED)
        elif button_close.value() and not is_loading:
            if(is_door_open == True):
                logger.log("Door closing...")
                is_loading = True
                led_loading.blink()
                
                close_door()
                
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
        elif button_reset.value() and not is_loading:
            is_loading = True
            alarm.alert(constants.ALARM_LOADING)
            led_loading.blink()
            reset_system()
            led_loading.stop_blinking()
            is_loading = True
            
        else:
            scanned_card_id = scan_rfid()
            if(scanned_card_id):
                print("Detected Card : "+ str(scanned_card_id))
                # TODO
                pass

logger.close()